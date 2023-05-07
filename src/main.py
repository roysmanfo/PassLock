from user import User
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import getpass
import base64
import sys
import json
import os
import argparse

class Color:
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BLUE = "\033[0;34m"
    CYAN = "\033[0;36m"
    YELLOW = "\033[1;33m"
    PURPLE = "\033[0;35m"
    RESET = "\033[0m"


col = Color


parser = argparse.ArgumentParser(
    prog='PassLock',
    description='Store your passwords localy in a secure way',
    usage='{ exit, clear, help, list, set, get, del, add } ...',
    exit_on_error=False,
    add_help=False
)
subparser = parser.add_subparsers(dest='command')

general_parser = subparser.add_parser('exit', help='Close the application', exit_on_error=False)
general_parser = subparser.add_parser('clear', help='Clear the screen', exit_on_error=False)
general_parser = subparser.add_parser('help' , help='Display this help message', exit_on_error=False)

list_parser = subparser.add_parser('list', help='List all app names', exit_on_error=False)
list_parser.add_argument('-s', '--sort', action='store_true', help='Sorts the names based on the number of fields')

set_parser = subparser.add_parser('set', help='Add/Update the credentials for the specified app (i.e set github.password password )', exit_on_error=False)
set_parser.add_argument('field', help='field to modify (syntax: app_name.field_name)')
set_parser.add_argument('new_val', help='New value for the specified field')

get_parser = subparser.add_parser('get', help='Get all credentials for the specified app (*case insensitive*)', exit_on_error=False)
get_parser.add_argument('key', help='The app_nane whose the credentials will be shown')

del_parser = subparser.add_parser('del', help='Delete the credentials of the specified field (i.e del github.phone ) or whole app from the password vault', exit_on_error=False)
del_parser.add_argument('key', help='The name of the app/field to delete')

add_parser = subparser.add_parser('add', help='Add the new app/apps to the vault (i.e add github bitcoin work)', exit_on_error=False)
add_parser.add_argument('key', nargs='*', metavar='app', help='app_name to add to the password vault')


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
            args = input()
            args = args.strip().split(' ')
            while args.count('') > 0:
                args.remove('')
            args[0].lower()
            run_command(parser.parse_args(args), USER.key)

            # print(command)
        except KeyboardInterrupt:
            break

    sys.exit(0)


def run_command(args, key: bytes):
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

    if args.command == 'exit':
        sys.exit(0)

    elif args.command == 'list':
        with open(os.path.join('data', 'vault.json'), 'r') as f:
            apps: dict = json.load(f)['Apps']
            
            if len(apps) == 0:
                print(f'{col.YELLOW}No apps registered yet{col.RESET}')
                return
            # Organize apps in a set (app_name, n_fields)
            apps = [(i, len(apps[i].items())) for i in apps]
            
            # Wheather or not we want to sort the apps based on the number of fields
            if args.sort:
                apps = sorted(apps, key=lambda x: x[1], reverse=True)
            
            for app in apps:
                print(f'{app[0]}: {col.CYAN}{app[1]}{col.RESET} fields')

    elif args.command == 'get':
        if not args.key:
            print(f'{col.RED}No app name specified{col.RESET}')
            return
        # elif len(args) > 2:
        #     print(f'{col.RED}Too many arguments specified{col.RESET}')
        #     return
        
        with open(os.path.join('data', 'vault.json'), 'r') as f:
            apps: dict = json.load(f)['Apps']
            args.key: str = args.key.capitalize()
            if args.key not in apps.keys():
                print(f'{col.RED}App not found{col.RESET}')
            else:
                # print('================================================================')
                print(f'\n{col.CYAN}{args.key.upper()}{col.RESET}')
                print('================================================================')
                for _, name in enumerate(apps[args.key].keys()):
                    val = fernet.decrypt(apps[args.key][name]).decode('utf-8')
                    print(f'{name.upper()}: {col.PURPLE}{val}{col.RESET}')
                print('================================================================')
    
    elif args.command == 'set':
        if not args.field or not args.new_val:
            print(f'{col.RED}Not enough arguments specified{col.RESET}')
            return

        elif len(args.field.split('.')) < 2:
            print(f'{col.RED}No field to change specified{col.RESET}')
            return
        
        appname, appfield = args.field.split('.')
        with open(os.path.join('data', 'vault.json'), 'r') as f:
            apps: dict = json.load(f)['Apps']
            appname:str = appname.capitalize()
            appfield:str = appfield.capitalize()

            if appname not in apps.keys():
                print(f'{col.RED}App not found{col.RESET}')
                return

            if appfield not in apps[appname].keys():
                print(f'{col.CYAN}Creating new field {appfield}{col.RESET}')
            
            dict.update(apps[appname], {appfield: fernet.encrypt(" ".join(args.new_val).encode('utf-8')).decode('utf-8')})
            
            update_vault(apps)
            print(f'{col.GREEN}{appname} updated{col.RESET}')

    elif args.command == 'del':
        if not args.key:
            print(f'{col.RED}Not enough arguments specified{col.RESET}')
            return
        # elif len(args) > 2:
        #     print(f'{col.RED}Too many arguments specified{col.RESET}')
        #     return
        
        elif len(args.key.split('.')) < 2:
            with open(os.path.join('data', 'vault.json'), 'r') as f:
                apps: dict = json.load(f)['Apps']

                if args.key.capitalize() not in apps.keys():
                    print(f'{col.RED}App not found{col.RESET}')
                    return
                
                apps.pop(args.key.capitalize())
                update_vault(apps)
                print(f'{col.GREEN}{args.key.capitalize()} removed{col.RESET}')
            return
        
        appname, appfield = args.key.split('.')

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

    elif args.command == 'add':
        if len(args.args) < 1:
            print(f'{col.RED}Not enough arguments specified{col.RESET}')
            return
        with open(os.path.join('data', 'vault.json'), 'r') as f:
            apps: dict = json.load(f)['Apps']
            new_apps = args.args

            for app in new_apps:
                dict.update(apps, {app.capitalize(): {}})

            update_vault(apps)
            print(f'{col.GREEN}{" ".join(new_apps)} added{col.RESET}')
    
    elif args.command == 'clear':
        os.system("clear || cls")

    elif args.command in ['-h', '--help','help']:
        print('''usage: { exit, clear, help, list, set, get, del, add } ...

Store your passwords localy in a secure way

commands:
    exit                Close the application
    clear               Clear the screen
    help                Display this help message
    list                List all app names
    set                 Add/Update the credentials for the specified app (i.e set github.password password )
    get                 Get all credentials for the specified app (*case insensitive*)
    del                 Delete the credentials of the specified field (i.e del github.phone ) or whole app from the password vault
    add                 Add the new app/apps to the vault (i.e add github bitcoin work)
    help                Show this help message
''')



def update_vault(apps: dict):
    with open(os.path.join('data', 'vault.json'), 'r') as f:
        file = json.load(f)
        pm_hash: str = file['PM-hash']
        updated_vault = {
            "PM-hash": pm_hash,
            "Apps": dict(sorted(apps.items()))
        }
        with open(os.path.join('data', 'vault.json'), 'w') as l:
            json.dump(updated_vault, l, indent=4)
    


if __name__ == '__main__':
    main()
