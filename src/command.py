import hashlib
import sys, os, json
from cryptography.fernet import Fernet
from argparse import ArgumentParser
from pathlib import Path

from colors import col
from utils import update_vault
from user import User


def run_command(args: ArgumentParser, key: bytes, user: User):
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

    elif args.command in ['list', 'ls']:
        with open(user.vault_path, 'r') as f:
            apps: dict = json.load(f)['Apps']
            
            if len(apps) == 0:
                print(f'{col.YELLOW}No apps registered yet{col.RESET}')
                return
            # Organize apps in a set (app_name, n_fields)
            apps = [(fernet.decrypt(i).decode(), len(apps[i].items())) for i in apps]

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
        
        with open(user.vault_path, 'r') as f:
            apps: dict = json.load(f)['Apps']
            args.key: str = args.key.capitalize()

            keys = [fernet.decrypt(i).decode() for i in apps.keys()]

            if args.key not in keys:
                print(f'{col.RED}App not found{col.RESET}')
            else:

                mapped_keys = {}
                for enc_key in apps.keys():
                    dict.update(mapped_keys, {fernet.decrypt(enc_key).decode(): enc_key})


                # print('================================================================')
                print(f'\n{col.CYAN}{args.key.upper()}{col.RESET}')
                print('================================================================')
                for _, name in enumerate(apps[mapped_keys[args.key]].keys()):
                    val = fernet.decrypt(apps[mapped_keys[args.key]][name]).decode('utf-8')
                    name = fernet.decrypt(name).decode('utf-8')
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
        with open(user.vault_path, 'r') as f:
            apps: dict = json.load(f)['Apps']

            appname:str = appname.capitalize()
            appfield:str = appfield.capitalize()

            stored_keys = [fernet.decrypt(i).decode() for i in apps.keys()]
            if appname not in stored_keys:
                print(f'{col.RED}App not found{col.RESET}')
                return

            mapped_keys = {}
            for enc_key in apps.keys():
                dict.update(mapped_keys, {fernet.decrypt(enc_key).decode(): enc_key})

            stored_keys = [fernet.decrypt(i).decode() for i in apps[mapped_keys[appname]].keys()]
            if appfield not in stored_keys:
                print(f'{col.CYAN}Creating new field {appfield}{col.RESET}')
            
            dict.update(apps[mapped_keys[appname]], {fernet.encrypt(appfield.encode()).decode(): fernet.encrypt(" ".join(args.new_val).encode('utf-8')).decode('utf-8')})
            
            update_vault(user, apps=apps)
            print(f'{col.GREEN}{appname} updated{col.RESET}')

    elif args.command in ['del', 'rm']:
        if len(args.key) < 1:
            print(f'{col.RED}Not enough arguments specified{col.RESET}')
            return
        
        # Remove the whole app from the vault
        for appkey in args.key:
            if len(appkey.split('.')) < 2:
                with open(user.vault_path, 'r') as f:
                    apps: dict = json.load(f)['Apps']

                    keys = [fernet.decrypt(i).decode() for i in apps.keys()]
                    mapped_keys = {}
                    for enc_key in apps.keys():
                        dict.update(mapped_keys, {fernet.decrypt(enc_key).decode(): enc_key})

                    if appkey.capitalize() not in keys:
                        print(f'{col.RED}App not found{col.RESET}')
                        continue
                    

                    apps.pop(mapped_keys[appkey.capitalize()])
                    update_vault(user, apps=apps)
                    print(f'{col.GREEN}{appkey.capitalize()} removed{col.RESET}')
                continue
            
            # Remove just a field
            appname, appfield = appkey.split('.')

            with open(user.vault_path, 'r') as f:
                apps: dict = json.load(f)['Apps']
                appname:str = appname.capitalize()
                appfield: str = appfield.capitalize()   
                
                keys = [fernet.decrypt(i).decode() for i in apps.keys()]
                mapped_keys = {}
                for enc_key in apps.keys():
                    dict.update(mapped_keys, {fernet.decrypt(enc_key).decode(): enc_key})
                
                if appname not in keys:
                    print(f'{col.RED}App not found{col.RESET}')
                    continue

                if appfield not in [fernet.decrypt(i).decode() for i in apps[mapped_keys[appname]].keys()]:
                    print(f'{col.RED}Field {appfield} not found in {appname}{col.RESET}')
                    continue

                apps[mapped_keys[appname]].pop([i for i in apps[mapped_keys[appname]].keys() if fernet.decrypt(i).decode() == appfield][0])

            update_vault(user, apps=apps )
            print(f'{col.GREEN}{appname} updated{col.RESET}')

    elif args.command == 'add':
        if len(args.key) < 1:
            print(f'{col.RED}Not enough arguments specified{col.RESET}')
            return
        with open(user.vault_path, 'r') as f:
            apps: dict = json.load(f)['Apps']
            new_apps = [i.capitalize() for i in args.key]
            keys = [fernet.decrypt(i).decode() for i in apps.keys()]

            for i in new_apps:
                if new_apps.count(i) > 1:
                    print(f"{col.RED}App {i} is repeated, only one will be created{col.RESET}")
                    while new_apps.count(i) > 1:
                        new_apps.remove(i)
            for app in new_apps:
                if app in keys:
                    print(f"{col.RED}There is already an app with name {app.capitalize()}{col.RESET}")
                    new_apps.remove(app)

            for app in new_apps:
                if app in keys:
                    new_apps.remove(app)
                    continue
                dict.update(apps, {fernet.encrypt(app.capitalize().encode()).decode(): {}})

            update_vault(user, apps=apps )
            print(f'{col.GREEN}{" ".join(new_apps)} added{col.RESET}') if len(new_apps) > 0 else 0
    
    elif args.command == 'clear':
        os.system("clear || cls")

    elif args.command in ['-h', '--help','help']:
        print('''usage: { exit, clear, help, chpass, list, ls, set, get, del, rm, add, rename, rnm } ...

Store your passwords localy in a secure way

commands:
    exit                Close the application
    clear               Clear the screen
    chpass              Change the password manager.
    sethint     	    Set a hint for when you forget the password master (i.e sethint your dog\'s name)
    help                Display this help message
    list                List all app names
    ls                  List all app names
    set                 Add/Update the credentials for the specified app (i.e set github.password password )
    get                 Get all credentials for the specified app
    del                 Delete the credentials of the specified app/field (i.e `del github.phone` or `del github`) from the password vault
    rm                  Delete the credentials of the specified app/field (i.e `rm github.phone` or `rm github`) from the password vault
    add                 Add the new app/apps to the vault (i.e add github bitcoin work)
    rename              Rename a key or a field (i.e `rename work.code passkey` or `rename work job`)
    rnm                 Rename a key or a field (i.e `rnm work.code passkey` or `rnm work job`)
''')

    elif args.command in ['rename', 'rnm']:
        # Rename a key or field
        original_key: str = args.key.capitalize()
        new_key: str = args.new_val.capitalize()

        with open(user.vault_path, 'r') as f:
            apps: dict = json.load(f)['Apps']
            keys = [fernet.decrypt(i).decode() for i in apps.keys()]
            mapped_keys = {}
            for enc_key in apps.keys():
                dict.update(mapped_keys, {fernet.decrypt(enc_key).decode(): enc_key})
            
            # Check the app name
            if len(original_key.split('.')) == 1:
                if original_key not in keys:
                    print(f'{col.RED}App not found{col.RESET}')
                    return
            elif len(original_key.split('.')) == 2:
                if original_key.split('.')[0] not in keys:
                    print(f'{col.RED}App not found{col.RESET}')
                    return
            else:
                print(f'{col.RED}Syntax error{col.RESET}')
                return
            
            # Check if we want to rename an app or a field
            if len(original_key.split('.')) == 1 and new_key in keys:
                print(f"{col.RED}There is already an app with name {new_key.capitalize()}{col.RESET}")
                return
            elif new_key in [fernet.decrypt(i).decode() for i in apps]:
                print(f"{col.RED}There is already a field with name {new_key.capitalize()}{col.RESET}")
                return
            
            # Create a new dictionary/field with the updated name and delete the old one
            if len(original_key.split('.')) == 1:
                sub_dict = apps[mapped_keys[original_key]]
                apps[fernet.encrypt(new_key.encode()).decode()] = sub_dict
                del apps[mapped_keys[original_key]]
            else:
                appname, fieldname = [i.capitalize() for i in original_key.split('.')]
                mapped_fields = {}
                for enc_key in apps[mapped_keys[appname]].keys():
                    dict.update(mapped_fields, {fernet.decrypt(enc_key).decode(): enc_key})
                old_field = mapped_fields[fieldname] # get the old value of the field
                field_val = apps[mapped_keys[appname]][old_field]
                apps[mapped_keys[appname]][fernet.encrypt(new_key.encode()).decode()] = field_val
                del apps[mapped_keys[appname]][mapped_fields[fieldname]]

            update_vault(user, apps=apps)
            print(f"{col.GREEN}Renamed '{original_key}' to '{new_key}'{col.RESET}")

    elif args.command == 'chpass':
        import login
        new_key, password = login.generate_key(user, from_command_line=True)

        pm_hash = hashlib.sha512(password.encode()).hexdigest()
        
        with open(user.vault_path, 'r') as f:
            apps: dict = json.load(f)['Apps']
            appfields = [(fernet.decrypt(i).decode(), [[fernet.decrypt(l).decode() for l in k] for k in apps[i].items()]) for i in apps]
            apps = {}

            user.key = new_key
            fernet = Fernet(new_key)

            for app in appfields:
                fields = {}
                for field in app[1]:
                    dict.update(fields, {fernet.encrypt(field[0].encode()).decode(): fernet.encrypt(field[1].encode()).decode()})
                dict.update(apps, {fernet.encrypt(app[0].encode()).decode(): fields})

            update_vault(user, pm_hash, apps=apps)
    
    elif args.command == 'sethint':
        hint = " ".join(args.hint)
        
        if len(args.hint) < 1:
            if input("Do you want to delete the hint [y/n]: ").lower() == "y":
                update_vault(user, hint=hint)
                print(f'{col.GREEN}Hint deleted{col.RESET}')
            else:
                print(f'{col.GREEN}Hint unchanged{col.RESET}')
        else:            
            update_vault(user, hint=hint)
            print(f"{col.GREEN}Hint modified{col.RESET}")
