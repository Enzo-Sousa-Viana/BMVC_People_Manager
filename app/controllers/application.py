from bottle import template, request
from app.controllers.datarecord import DataRecord


class Application:
    def __init__(self):
        self.models = DataRecord()
        self.pages = {
            "portal": self.portal,
            "banco": self.banco
        }

    def render(self, page, parameter=None):
        action = self.pages.get(page)
        if action is None:
            return template("app/views/html/helper")
        if parameter is None:
            return action()
        return action(parameter)

    def portal(self, error=None):
        return template("app/views/html/portal", error=error)

    def banco(self, user=None):
        pessoas = self.models.list_pessoas()
        return template(
            "app/views/html/banco",
            user=user,
            pessoas=pessoas
        )

    def authenticate_user(self, username, password):
        return self.models.check_user(username, password)

    def current_user(self):
        session_id = request.get_cookie("session_id")
        return self.models.get_current_user(session_id)

    def logout_user(self):
        session_id = request.get_cookie("session_id")
        self.models.logout(session_id)

    def create_pessoa(self, nome, idade):
        nome = (nome or "").strip()
        if not nome:
            raise ValueError("O nome é obrigatório.")
        try:
            idade = int(idade)
        except (ValueError, TypeError):
            raise ValueError("A idade deve ser um número inteiro.")
        if idade < 0 or idade > 120:
            raise ValueError("Informe uma idade entre 0 e 120.")
        return self.models.create_pessoa(nome, idade)

    def list_pessoas(self):
        return self.models.list_pessoas()

    def update_pessoa(self, pessoa_id, nome, idade):
        nome = (nome or "").strip()
        if not nome:
            raise ValueError("O nome é obrigatório.")
        try:
            idade = int(idade)
        except (ValueError, TypeError):
            raise ValueError("A idade deve ser um número inteiro.")
        if idade < 0 or idade > 120:
            raise ValueError("Informe uma idade entre 0 e 120.")
        return self.models.update_pessoa(pessoa_id, nome, idade)

    def delete_pessoa(self, pessoa_id):
        return self.models.delete_pessoa(pessoa_id)
