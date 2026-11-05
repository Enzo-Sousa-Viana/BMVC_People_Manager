import hashlib
import hmac
import json
import secrets
from pathlib import Path

from app.models.user_account import UserAccount
from app.models.pessoa import Pessoa


class DataRecord:
    """Persistência JSON dos usuários e das pessoas cadastradas."""

    def __init__(self):
        self.db_dir = Path(__file__).resolve().parent / "db"
        self.db_dir.mkdir(parents=True, exist_ok=True)
        self.users_file = self.db_dir / "user_accounts.json"
        self.people_file = self.db_dir / "pessoas.json"
        self.authenticated_users = {}

        self.users = self._load_users()
        self.people = self._load_people()

    @staticmethod
    def _password_hash(password, salt):
        return hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            120_000
        ).hex()

    def _load_users(self):
        if not self.users_file.exists():
            salt = secrets.token_hex(16)
            default_user = UserAccount(
                username="admin",
                salt=salt,
                password_hash=self._password_hash("admin123", salt)
            )
            self._save_json(self.users_file, [vars(default_user)])
            return [default_user]

        data = self._read_json(self.users_file, [])
        users = [UserAccount(**item) for item in data]
        if not users:
            salt = secrets.token_hex(16)
            default_user = UserAccount(
                username="admin",
                salt=salt,
                password_hash=self._password_hash("admin123", salt)
            )
            users = [default_user]
            self._save_json(self.users_file, [vars(default_user)])
        return users

    def _load_people(self):
        data = self._read_json(self.people_file, [])
        return [Pessoa(**item) for item in data]

    @staticmethod
    def _read_json(path, fallback):
        try:
            with path.open("r", encoding="utf-8") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return fallback

    @staticmethod
    def _save_json(path, data):
        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def check_user(self, username, password):
        for user in self.users:
            if user.username == username:
                candidate = self._password_hash(password, user.salt)
                if hmac.compare_digest(candidate, user.password_hash):
                    session_id = secrets.token_urlsafe(32)
                    self.authenticated_users[session_id] = user.username
                    return session_id
        return None

    def get_current_user(self, session_id):
        if not session_id:
            return None
        return self.authenticated_users.get(session_id)

    def logout(self, session_id):
        if session_id:
            self.authenticated_users.pop(session_id, None)

    def create_pessoa(self, nome, idade):
        next_id = max((p.id for p in self.people), default=0) + 1
        pessoa = Pessoa(id=next_id, nome=nome, idade=idade)
        self.people.append(pessoa)
        self._save_json(self.people_file, [vars(p) for p in self.people])
        return vars(pessoa)

    def list_pessoas(self):
        return [vars(p) for p in self.people]

    def update_pessoa(self, pessoa_id, nome, idade):
        for pessoa in self.people:
            if pessoa.id == pessoa_id:
                pessoa.nome = nome
                pessoa.idade = idade
                self._save_json(self.people_file, [vars(p) for p in self.people])
                return vars(pessoa)
        return None

    def delete_pessoa(self, pessoa_id):
        for pessoa in self.people:
            if pessoa.id == pessoa_id:
                self.people.remove(pessoa)
                self._save_json(self.people_file, [vars(p) for p in self.people])
                return True
        return False
