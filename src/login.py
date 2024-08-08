import sys
import json
import getpass
import getpass

from user import User
from colors import col
import utils

def generate_key(USER: User, from_user: bool = False) -> bytes | tuple[bytes, str]:
    """
    ### Allows user to create a new password manager instance
    Returns the key needed to unlock the vault

    When `from_user` is true, also the plain text password is returned
    """
    if not from_user:
        print("""
In order to secure your password at best, you have to create a Password Master

A Password Master (PM) is a password you will have to remember and make sure to not forget
as we won't be able to restore or change it if forgotten, for security reasons.

A Password Master (PM) must be at least 8 characters long (max 32) and contain at least 1 uppercase letter
    """)
        
    approved = False

    while not approved:
        passw: str = getpass.getpass("Your Password Manager:  ")

        if not USER.check_password(passw) or len(passw) > 32:
            print(
                f"{col.RED}Your password doesn't satisfy some requirements, type another one{col.RESET}")
            passw: str = getpass.getpass("Your Password Manager:  ")

        else:

            passw2 = getpass.getpass("Your Password Manager (again):  ")

            if passw == passw2:
                approved = True
            else:
                print(
                    f"{col.RED}Passwords do not match, insert again the password{col.RESET}")

    # Create key
    if not from_user:
        USER.create_vault(passw, "")    
        return (utils.compute_key(passw=passw, iterations=100_000, key_length=32))
    
    return (utils.compute_key(passw=passw, iterations=100_000, key_length=32), passw)



def login(user: User) -> bytes:
    """
    ### Login and password validation sequence
    Returns the key needed to unlock the vault
    """
    try:
        i = 0
        pm = getpass.getpass("Enter password manager (invisible):  ")
        with open(user.vault_path) as f:
            hint = json.load(f)["Hint"]
        while not user.validate_key(pm):
            print(f"{col.RED}Not the correct password{col.RESET}")
            i+=1
            if i >= 3:
                print(f"{col.RED}You failed login {i} times. Type 'rst' or 'reset' to erase the vault and create another one{col.RESET}")
                print(f"{col.CYAN}Hint:{col.RESET}", hint) if hint != "" else 0
            pm = getpass.getpass("Enter password manager (invisible):  ")
            
            # when resetting the key, access to the existing vault is lost
            # (no way of re-encrypting without the lost key)
            if not user.validate_key(pm) and pm in ['rst', 'reset']:
                return generate_key(user)

    except KeyboardInterrupt:
        sys.exit(0)

    # Derive key
    return utils.compute_key(pm, 100_000, 32)


