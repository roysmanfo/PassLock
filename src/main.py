from user import User
from secure import Secure

def generate_password_master(USER: User, SECURE: Secure) -> str:
    print("""
In order to secure your password at best, you have to create a Password Master

A Password Master (PM) is a password you will have to remember and make shure to remember it
as we won't be able to restore or change it if forgotten, for security reasons.   
    
A Password Master (PM) must be at least 8 characters long and contain at least 1 uppercase letter
    """)
    passw: str = input("Your Password Manager:  ")

    while not USER.check_password(passw):
        print("Your password doesn't satisfy some requirements, type another one")
        passw: str = input("Your Password Manager:  ")

    USER.password_master = passw
    pass_hash: bytes = SECURE.encrypt(passw)


def main():
    """
    ### Point of start of the program
    """
    USER = User()
    SECURE = Secure(USER.key)

    if USER.password_master == "":
        generate_password_master(USER, SECURE)