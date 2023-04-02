from user import User
from cryptography.fernet import Fernet
import getpass
import base64


def generate_key(USER: User) -> bytes:
    print("""
In order to secure your password at best, you have to create a Password Master

A Password Master (PM) is a password you will have to remember and make sure to remember it
as we won't be able to restore or change it if forgotten, for security reasons.

A Password Master (PM) must be at least 8 characters long (max 32) and contain at least 1 uppercase letter
    """)
    passw: str = input("Your Password Manager:  ")

    while not USER.check_password(passw) or len(passw) > 32:
        print("Your password doesn't satisfy some requirements, type another one")
        passw: str = input("Your Password Manager:  ")

    for _ in range(len(passw), 32):
        passw += "="

    USER.create_vault(passw)
    fernet = Fernet(base64.urlsafe_b64encode(passw.encode()))
    key = fernet.generate_key()
    return key


def main():
    """
    ### Point of start of the program
    """
    USER = User()

    if USER.password_manager == b"":
        USER.key = generate_key(USER)

    else:
        pm = getpass.getpass("Enter password manager (invisible):  ")
        while not USER.validate_key(pm):
            print("Not the correct password")
            pm = getpass.getpass("Enter password manager (invisible):  ")
        for _ in range(len(pm), 32):
            pm += "="
        fernet = Fernet(base64.urlsafe_b64encode(pm.encode()))
        USER.key = fernet.generate_key()

    print("Logged sucessfully")


main()
