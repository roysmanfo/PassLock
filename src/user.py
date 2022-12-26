
class User(object):
    def __init__(self, password_master: str = ""):
        self.password_master = password_master
        self.logged = self.is_logged()
        self.key = ""


    def is_logged() -> bool:
        pass

    def generate_password_master(self):
        with open("./data/password_master.key", "w") as password:
            password.write(self.password_master)