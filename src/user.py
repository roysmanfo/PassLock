
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

    def check_password(self, passw: str) -> bool:
        """
        Checks if the Password Master satisfies the minimum password requirements

        - min length : 8
        - all uppercase letters: False
        - all lowercase letters: False
        - min uppercase letters: 1
        """

        if len(passw) < 8:
            return False

        if passw.upper() == passw or passw.lower() == passw:
            return False
            
        return True 

