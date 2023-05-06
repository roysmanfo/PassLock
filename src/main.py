from user import User
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import getpass
import base64
import sys
import json
import os


class Color:
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BLUE = "\033[0;34m"
    CYAN = "\033[0;36m"
    YELLOW = "\033[1;33m"
    PURPLE = "\033[0;35m"
    RESET = "\033[0m"


col = Color


def generate_key(USER: User) -> bytes:
    """
    ### Allows user to create a new password manager instance
    Returns the key needed to unlock the vault 
    """
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
    USER.create_vault(passw)

    passw = passw.encode()
    salt = b'5df'
    iterations = 100_000
    key_length = 32

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA3_512(),
        length=key_length,
        salt=salt,
        iterations=iterations
    )
    key = base64.urlsafe_b64encode(kdf.derive(passw))
    return key


def login(user: User) -> bytes:
    """
    ### Login and password validation sequence
    Returns the key needed to unlock the vault
    """
    try:
        pm = getpass.getpass("Enter password manager (invisible):  ")
        while not user.validate_key(pm):
            print(f"{col.RED}Not the correct password{col.RESET}")
            pm = getpass.getpass("Enter password manager (invisible):  ")

    except KeyboardInterrupt:
        sys.exit(0)

    # Derive key

    pm = pm.encode()
    salt = b'5df'
    iterations = 100_000
    key_length = 32

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA3_512(),
        length=key_length,
        salt=salt,
        iterations=iterations
    )
    key = base64.urlsafe_b64encode(kdf.derive(pm))
    return key


def main():
    """
    ### Point of start of the program
    """
    USER = User()
    USER.key = generate_key(
        USER) if USER.password_manager == b"" else login(USER)
    print(f"{col.GREEN}Logged sucessfully{col.RESET}")
    while True:
        try:
            print(f"{col.BLUE}PassLock> {col.RESET}", end='')
            command = input()
            command = command.strip().split(' ')
            while command.count('') > 0:
                command.remove('')
            command[0].lower()
            run_command(command, USER.key)

            # print(command)
        except KeyboardInterrupt:
            break

    sys.exit(0)


def run_command(args: list, key: bytes):
    """
    # Examples of outputs from these commmands
    ## `list`

    GitHub: 2 fields
    Google: 3 fields

    ## `get VALUE` case insensitive

    GITHUB
    ================================================================
    Username: Github1234
    Password: mypassword123
    ================================================================

    ## `set KEY NEW` case insensitive
    """

    fernet = Fernet(key)

    if args[0] == 'exit':
        sys.exit(0)

    elif args[0] == 'list':
        with open(os.path.join('data', 'vault.json'), 'r') as f:
            apps: dict = json.load(f)['Apps']
            if len(apps) == 0:
                print(f'{col.YELLOW}No apps registered yet{col.RESET}')
                return

            for app in apps.keys():
                print(f'{app}: {col.CYAN}{len(apps[app].keys())}{col.RESET} fields')

    elif args[0] == 'get':
        if len(args) < 2:
            print(f'{col.RED}No app name specified{col.RESET}')
            return
        elif len(args) > 2:
            print(f'{col.RED}Too many arguments specified{col.RESET}')
            return
        
        with open(os.path.join('data', 'vault.json'), 'r') as f:
            apps: dict = json.load(f)['Apps']
            args[1]: str = args[1].capitalize()
            if args[1] not in apps.keys():
                print(f'{col.RED}App not found{col.RESET}')
            else:
                # print('================================================================')
                print(f'\n{col.CYAN}{args[1].upper()}{col.RESET}')
                print('================================================================')
                for _, name in enumerate(apps[args[1]].keys()):
                    val = fernet.decrypt(apps[args[1]][name]).decode('utf-8')
                    print(f'{name.upper()}: {col.PURPLE}{val}{col.RESET}')
                print('================================================================')
    
    elif args[0] == 'set':
        if len(args) < 3:
            print(f'{col.RED}Not enough arguments specified{col.RESET}')
            return

        elif len(args[1].split('.')) < 2:
            print(f'{col.RED}No field to change specified{col.RESET}')
            return
        
        appname, appfield = args[1].split('.')
        with open(os.path.join('data', 'vault.json'), 'r') as f:
            apps: dict = json.load(f)['Apps']
            appname:str = appname.capitalize()
            appfield:str = appfield.capitalize()

            if appname not in apps.keys():
                print(f'{col.RED}App not found{col.RESET}')
                return

            if appfield not in apps[appname].keys():
                print(f'{col.CYAN}Creating new field {appfield}{col.RESET}')
            
            dict.update(apps[appname], {appfield: fernet.encrypt(" ".join(args[2:]).encode('utf-8')).decode('utf-8')})
            
            update_vault(apps)
            print(f'{col.GREEN}{appname} updated{col.RESET}')

    elif args[0] == 'del':
        if len(args) < 2:
            print(f'{col.RED}Not enough arguments specified{col.RESET}')
            return
        elif len(args) > 2:
            print(f'{col.RED}Too many arguments specified{col.RESET}')
            return
        elif len(args[1].split('.')) < 2:
            print(f'{col.RED}No field to change specified{col.RESET}')
            return
        
        appname, appfield = args[1].split('.')

        with open(os.path.join('data', 'vault.json'), 'r') as f:
            apps: dict = json.load(f)['Apps']
            appname:str = appname.capitalize()
            appfield:str = appfield.capitalize()
            
            if appname not in apps.keys():
                print(f'{col.RED}App not found{col.RESET}')
                return

            if appfield not in apps[appname].keys():
                print(f'{col.RED}Field not found in {appname}{col.RESET}')
                return

            apps[appname].pop(appfield)
            update_vault(apps)
            print(f'{col.GREEN}{appname} updated{col.RESET}')

    elif args[0] == 'add':
        if len(args) < 2:
            print(f'{col.RED}Not enough arguments specified{col.RESET}')
            return
        with open(os.path.join('data', 'vault.json'), 'r') as f:
            apps: dict = json.load(f)['Apps']
            new_apps = args[1:]

            for app in new_apps:
                dict.update(apps, {app.capitalize(): {}})

            update_vault(apps)
            print(f'{col.GREEN}{" ".join(new_apps)} added{col.RESET}')



def update_vault(apps: dict):
    with open(os.path.join('data', 'vault.json'), 'r') as f:
        file = json.load(f)
        pm_hash: str = file['PM-hash']
        updated_vault = {
            "PM-hash": pm_hash,
            "Apps": apps
        }
        with open(os.path.join('data', 'vault.json'), 'w') as l:
            json.dump(updated_vault, l, indent=4)
    


if __name__ == '__main__':
    main()
