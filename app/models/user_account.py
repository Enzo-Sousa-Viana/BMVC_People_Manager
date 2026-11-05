class UserAccount:
    def __init__(self, username, salt, password_hash):
        self.username = username
        self.salt = salt
        self.password_hash = password_hash
