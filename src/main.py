from user import User
from cryptography.fernet import Fernet
import getpass
import base64


def generate_key(USER: User) -> bytes:
    """
    ### Allows user to create a new password manager instance
    Returns the key needed to unlock the vault 
    """
    print("""
In order to secure your password at best, you have to create a Password Master

A Password Master (PM) is a password you will have to remember and make sure to remember it
as we won't be able to restore or change it if forgotten, for security reasons.

A Password Master (PM) must be at least 8 characters long (max 32) and contain at least 1 uppercase letter
    """)
    passw: str = getpass.getpass("Your Password Manager:  ")

    while not USER.check_password(passw) or len(passw) > 32:
        print("Your password doesn't satisfy some requirements, type another one")
        passw: str = getpass.getpass("Your Password Manager:  ")

    # Create padding
    for _ in range(len(passw), 32):
        passw += "="

    USER.create_vault(passw)
    fernet = Fernet(base64.urlsafe_b64encode(passw.encode()))
    key = fernet.generate_key()
    return key


def login(user: User) -> bytes:
    """
    ### Login and password validation sequence
    Returns the key needed to unlock the vault
    """
    pm = getpass.getpass("Enter password manager (invisible):  ")
    while not user.validate_key(pm):
        print("Not the correct password")
        pm = getpass.getpass("Enter password manager (invisible):  ")

    # Create padding
    for _ in range(len(pm), 32):
        pm += "="

    fernet = Fernet(base64.urlsafe_b64encode(pm.encode()))
    return fernet.generate_key()


def main():
    """
    ### Point of start of the program
    """
    USER = User()
    USER.key = generate_key(
        USER) if USER.password_manager == b"" else login(USER)
    print("Logged sucessfully")

if __name__ == '__main__':
    main()
