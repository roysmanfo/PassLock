import hashlib
from pathlib import Path
import sys, os, json
from cryptography.fernet import Fernet, InvalidToken
from argparse import ArgumentParser

from passlock import utils, login, conf
from passlock.colors import col
from passlock.utils import update_vault
from passlock.user import User

class EnVars:
    """
    General stuff that every command will use
    """
    def __init__(self):
        self.user: User = None
        self.fernet: Fernet = None
        self.args: ArgumentParser = None

    def init(self, user: User, key: bytes):
        self.user = user
        self.fernet = Fernet(key)

envars = EnVars()


def cmd_list():
    if envars.args.files:
        files = os.listdir(envars.user.vault_storage)

        if len(files) == 0:
            print(f'{col.YELLOW}No files found in secure storage{col.RESET}')
            return
        
        total_size = 0
        for i, file in enumerate(files, start=1):
            f_size = os.stat(os.path.join(envars.user.vault_storage, file)).st_size
            total_size += f_size
            size = utils.format_file_size(f_size)
            
            print("{}{}{} {} {}".format(col.CYAN, f'{i}.'.ljust(4), col.RESET, size.ljust(10), file))

        print(f"\n{len(files)} file" + ("s" if len(files) > 1 else "") , "| total size:",  utils.format_file_size(total_size))
    else:
        with open(envars.user.vault_path, 'r') as f:
            apps: dict = json.load(f)['Apps']
            
            if len(apps) == 0:
                print(f'{col.YELLOW}No apps registered yet{col.RESET}')
                return
            # Organize apps in a set (app_name, n_fields)
            apps = [(envars.fernet.decrypt(i).decode(), len(apps[i].items())) for i in apps]

            # Wheather or not we want to sort the apps based on the number of fields
            if envars.args.sort:
                apps = sorted(apps, key=lambda x: x[1], reverse=True)
            
            for app in apps:
                print(f'{app[0]}: {col.CYAN}{app[1]}{col.RESET} fields')

def cmd_get():
    if not envars.args.key:
        print(f'{col.RED}No app name specified{col.RESET}')
        return
    # elif len(args) > 2:
    #     print(f'{col.RED}Too many arguments specified{col.RESET}')
    #     return
    
    with open(envars.user.vault_path, 'r') as f:
        apps: dict = json.load(f)['Apps']
        envars.args.key = envars.args.key.capitalize()

        keys = [envars.fernet.decrypt(i).decode() for i in apps.keys()]

        if envars.args.key not in keys:
            print(f'{col.RED}App not found{col.RESET}')
        else:

            mapped_keys = {}
            for enc_key in apps.keys():
                dict.update(mapped_keys, {envars.fernet.decrypt(enc_key).decode(): enc_key})


            # print('================================================================')
            print(f'\n{col.CYAN}{envars.args.key.upper()}{col.RESET}')
            print('================================================================')
            for _, name in enumerate(apps[mapped_keys[envars.args.key]].keys()):
                val = envars.fernet.decrypt(apps[mapped_keys[envars.args.key]][name]).decode('utf-8')
                name = envars.fernet.decrypt(name).decode('utf-8')
                print(f'{name.upper()}: {col.PURPLE}{val}{col.RESET}')
            print('================================================================')

def cmd_set():
    if not envars.args.field or not envars.args.new_val:
        print(f'{col.RED}Not enough arguments specified{col.RESET}')
        return

    elif len(envars.args.field.split('.')) < 2:
        print(f'{col.RED}No field to change specified{col.RESET}')
        return
    
    appname, appfield = envars.args.field.split('.')
    with open(envars.user.vault_path, 'r') as f:
        apps: dict = json.load(f)['Apps']

        appname:str = appname.capitalize()
        appfield:str = appfield.capitalize()

        stored_keys = [envars.fernet.decrypt(i).decode() for i in apps.keys()]
        if appname not in stored_keys:
            print(f'{col.RED}App not found{col.RESET}')
            return

        # create a temporary mapping: "key_name" (decrypted) -> key_name (encrypted)
        mapped_keys = {}
        for enc_key in apps.keys():
            dict.update(mapped_keys, {envars.fernet.decrypt(enc_key).decode(): enc_key})

        stored_keys = [envars.fernet.decrypt(i).decode() for i in apps[mapped_keys[appname]].keys()]
        if appfield not in stored_keys:
            print(f'{col.CYAN}Creating new field {appfield}{col.RESET}')
        
        field_name = envars.fernet.encrypt(appfield.encode('utf-8'))
        field_val = " ".join(envars.args.new_val).encode('utf-8')
        apps.update
        dict.update(
            apps[mapped_keys[appname]],
            {
                field_name.decode('utf-8'): envars.fernet.encrypt(field_val).decode('utf-8')
            }
        )
        del mapped_keys
        
        update_vault(envars.user, apps=apps)
        print(f'{col.GREEN}{appname} updated{col.RESET}')

def cmd_del():
    if len(envars.args.key) < 1:
        print(f'{col.RED}Not enough arguments specified{col.RESET}')
        return
    
    # Remove the whole app from the vault
    for appkey in envars.args.key:
        if len(appkey.split('.')) < 2:
            with open(envars.user.vault_path, 'r') as f:
                apps: dict = json.load(f)['Apps']

                keys = [envars.fernet.decrypt(i).decode() for i in apps.keys()]
                mapped_keys = {}
                for enc_key in apps.keys():
                    dict.update(mapped_keys, {envars.fernet.decrypt(enc_key).decode(): enc_key})

                if appkey.capitalize() not in keys:
                    print(f'{col.RED}App not found{col.RESET}')
                    continue
                

                apps.pop(mapped_keys[appkey.capitalize()])
                update_vault(envars.user, apps=apps)
                print(f'{col.GREEN}{appkey.capitalize()} removed{col.RESET}')
            continue
        
        # Remove just a field
        appname, appfield = appkey.split('.')

        with open(envars.user.vault_path, 'r') as f:
            apps: dict = json.load(f)['Apps']
            appname:str = appname.capitalize()
            appfield: str = appfield.capitalize()   
            
            keys = [envars.fernet.decrypt(i).decode() for i in apps.keys()]
            mapped_keys = {}
            for enc_key in apps.keys():
                dict.update(mapped_keys, {envars.fernet.decrypt(enc_key).decode(): enc_key})
            
            if appname not in keys:
                print(f'{col.RED}App not found{col.RESET}')
                continue

            if appfield not in [envars.fernet.decrypt(i).decode() for i in apps[mapped_keys[appname]].keys()]:
                print(f'{col.RED}Field {appfield} not found in {appname}{col.RESET}')
                continue

            apps[mapped_keys[appname]].pop([i for i in apps[mapped_keys[appname]].keys() if envars.fernet.decrypt(i).decode() == appfield][0])

        update_vault(envars.user, apps=apps )
        print(f'{col.GREEN}{appname} updated{col.RESET}')

def cmd_add():
    if len(envars.args.key) < 1:
        print(f'{col.RED}Not enough arguments specified{col.RESET}')
        return
    with open(envars.user.vault_path, 'r') as f:
        apps: dict = json.load(f)['Apps']
        new_apps = [i.capitalize() for i in envars.args.key]
        keys = [envars.fernet.decrypt(i).decode() for i in apps.keys()]

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
            dict.update(apps, {envars.fernet.encrypt(app.capitalize().encode()).decode(): {}})

        update_vault(envars.user, apps=apps )
        print(f'{col.GREEN}{" ".join(new_apps)} added{col.RESET}') if len(new_apps) > 0 else 0

def cmd_rnm():
    # Rename a key or field
    original_key: str = envars.args.key.capitalize()
    new_key: str = envars.args.new_val.capitalize()

    with open(envars.user.vault_path, 'r') as f:
        apps: dict = json.load(f)['Apps']
    keys = [envars.fernet.decrypt(i).decode() for i in apps.keys()]
    mapped_keys = {}
    for enc_key in apps.keys():
        dict.update(mapped_keys, {envars.fernet.decrypt(enc_key).decode(): enc_key})
    
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
    elif new_key in [envars.fernet.decrypt(i).decode() for i in apps]:
        print(f"{col.RED}There is already a field with name {new_key.capitalize()}{col.RESET}")
        return
    
    # Create a new dictionary/field with the updated name and delete the old one
    if len(original_key.split('.')) == 1:
        sub_dict = apps[mapped_keys[original_key]]
        apps[envars.fernet.encrypt(new_key.encode()).decode()] = sub_dict
        del apps[mapped_keys[original_key]]
    else:
        # well you find this hard to read, but it was harder to write,
        # AND I HAD TO DO BOTH 
        appname, fieldname = [i.capitalize() for i in original_key.split('.')]
        mapped_fields = {}
        for enc_key in apps[mapped_keys[appname]].keys():
            dict.update(mapped_fields, {envars.fernet.decrypt(enc_key).decode(): enc_key})
        old_field = mapped_fields[fieldname] # get the old value of the field
        field_val = apps[mapped_keys[appname]][old_field]
        apps[mapped_keys[appname]][envars.fernet.encrypt(new_key.encode()).decode()] = field_val
        del apps[mapped_keys[appname]][mapped_fields[fieldname]]

    update_vault(envars.user, apps=apps)
    print(f"{col.GREEN}Renamed '{original_key}' to '{new_key}'{col.RESET}")

def cmd_chpass():
    new_key, password = login.generate_key(envars.user, from_user=True)
    pm_hash = hashlib.sha512(password.encode()).hexdigest()
    old_fernet = envars.fernet

    with open(envars.user.vault_path, 'r') as f:
        apps: dict = json.load(f)['Apps']
        appfields = [(envars.fernet.decrypt(i).decode(), [[envars.fernet.decrypt(l).decode() for l in k] for k in apps[i].items()]) for i in apps]
        apps = {}

        envars.user.key = new_key
        envars.fernet = Fernet(new_key)

        for app in appfields:
            fields = {}
            for field in app[1]:
                dict.update(fields, {envars.fernet.encrypt(field[0].encode()).decode(): envars.fernet.encrypt(field[1].encode()).decode()})
            dict.update(apps, {envars.fernet.encrypt(app[0].encode()).decode(): fields})

        update_vault(envars.user, pm_hash, apps=apps)
        print(f"{col.GREEN}vault updated{col.GREEN}")
        print(f"updating files in the secure vault (this process may take some time based on the size of the vault)")
        
        # dont forget the files stored in the secure vault
        for file in os.listdir(envars.user.vault_storage):
            with open(file, "rb") as f:
                data = old_fernet.decrypt(f.read())
            with open(file, "wb") as f:
                f.write(envars.fernet.encrypt(data))

        print(f"{col.GREEN}secure storage updated{col.GREEN}")


def cmd_sethint():
    hint = " ".join(envars.args.hint)
        
    if len(envars.args.hint) < 1:
        if input("Do you want to delete the hint [y/n]: ").lower() == "y":
            update_vault(envars.user, hint=hint)
            print(f'{col.GREEN}Hint deleted{col.RESET}')
        else:
            print(f'{col.GREEN}Hint unchanged{col.RESET}')
    else:            
        update_vault(envars.user, hint=hint)
        print(f"{col.GREEN}Hint modified{col.RESET}")

def cmd_fenc():
    try:
        files = utils.path_escape(" ".join(envars.args.files))
    except Exception as e:
        print(f'{col.RED}Err: {e}{col.RESET}')
        return

    # Check for errors in the input
    # don't do anything if there are errors
    for file in files:
        if not file.exists():
            print(f'{col.RED}File `{file}` does not exist{col.RESET}')
            return
        
        if not file.is_file():
            print(f'{col.RED}`{file}` is not a file{col.RESET}')
            return
        
    # Try to overwrite all given files
    for file in files:
        _original = None 
        try:
            with open(file, 'rb') as f:
                if not f.readable():
                    print(f'{col.RED}`{file}` is not readable{col.RESET}')
                    continue
                content = f.read()

            if envars.args.save:
                # save an encrypted copy of the original file in the vault
                _original = file
                file = os.path.join(envars.user.vault_storage, file.name)

            with open(file, 'wb') as f:
                content = envars.fernet.encrypt(content)
                f.write(content)

            if envars.args.save:
                print(f"[{col.GREEN}+{col.RESET}] added `{_original}` to secure storage{col.RESET}")
                if envars.args.remove:

                    if _original.samefile(file):
                        print(f'{col.RED}unable to remove the original file (same file error){col.RESET}')                    
                    else:
                        try:
                            os.remove(_original)
                        except FileNotFoundError:
                            print(f'{col.RED}unable to remove `{file}` (file not found) {col.RESET}')
                        except PermissionError:
                            print(f'{col.RED}unable to remove `{file}` (permission error) {col.RESET}')                    
                        else:
                            print(f'{col.RED}removed{col.RESET} original file')                    
        except PermissionError:
            print(f'{col.RED}Do not have permissions to overwrite file `{file}`{col.RESET}')

def cmd_fdec():
    out_dir: Path = None

    if envars.args.output:
        out_dir = utils.path_escape(envars.args.output)[0].resolve()

        if out_dir.exists() and out_dir.is_reserved():
            print(f'{col.RED}unable to access `{file}` (permission error){col.RESET}')
            return
        
        if not out_dir.is_dir():
            print(f'{col.RED}`{file}` is not a directory{col.RESET}')
            return

        out_dir.mkdir(parents=True, exist_ok=True)

    try:
        files = utils.path_escape(" ".join(envars.args.files))
    except Exception as e:
        print(f'{col.RED}Err: {e}{col.RESET}')
        return

    # Check for errors in the input
    # don't do anything if there are errors
    for file in files:

        if envars.args.secure_storage:
            # this file is in the secure storage
            file = Path(os.path.join(envars.user.vault_storage, file))
        if not file.exists():
            print(f'{col.RED}File `{file}` does not exist{col.RESET}')
            return
        
        if not file.is_file():
            print(f'{col.RED}`{file}` is not a file{col.RESET}')
            return
        
    # Try to decrypt all given files
    for file in files:
        if envars.args.secure_storage:
            # this file is in the secure storage
            file = Path(os.path.join(envars.user.vault_storage, file))
        try:
            with open(file, 'rb') as f:
                if f.readable():
                    content = f.read()
                else:
                    print(f'{col.RED}`{file}` is not readable{col.RESET}')
                    return
            
            out_file = file
            if out_dir:
                out_file = out_dir.joinpath(os.path.basename(file))

            with open(out_file, 'wb') as f:
                content = envars.fernet.decrypt(content)
                f.write(content)
        
            if envars.args.remove and str(out_file) != str(file):
                try:
                    os.remove(file)
                except FileNotFoundError:
                    print(f'{col.RED}unable to remove `{file}` (file not found) {col.RESET}')
                except PermissionError:
                    print(f'{col.RED}unable to remove `{file}` (permission error) {col.RESET}')                    
                else:
                    print(f'{col.RED}removed{col.RESET} original file')  

        except PermissionError:
            print(f'{col.RED}Do not have permissions to overwrite file `{file}`{col.RESET}')
        
        except InvalidToken:
            print(f'{col.RED}unable to decrypt the file `{file}` (may have been altered){col.RESET}')

def cmd_version():
    if not conf.VERSION:
        print(f"{col.RED}config file altered (unable to determine the version){col.RESET}")
        return

    print(conf.VERSION)


def run_command(args: ArgumentParser):
    """
    Acts like a swich statement by triggering the right command
    when the correct input is given
    """

    envars.args = args

    match args.command:
        case 'exit':            sys.exit(0)
        case 'list' | 'ls':     cmd_list()
        case 'get':             cmd_get()
        case 'set':             cmd_set()
        case 'del' | 'rm':      cmd_del()
        case 'add':             cmd_add()
        case 'rename' | 'rnm':  cmd_rnm()
        case 'chpass':          cmd_chpass()
        case 'sethint':         cmd_sethint()
        case 'fenc':            cmd_fenc()
        case 'fdec':            cmd_fdec()
        case 'version':         cmd_version()
        case 'clear':           os.system("cls" if os.name == 'nt' else "clear")
        case '-h'|'--help'|'help': print('''usage: command [options] ...

Store your passwords localy in a secure way

commands:
    exit                Close the application
    clear               Clear the screen
    chpass              Change the password manager.
    fenc                File Encrypt: encrypt 1 or more text file (i.e. fenc file1.txt path/to/file2.txt)
    fdec                File Decrypt: decript 1 or more text file (i.e. fdec file1.txt path/to/file2.txt)
    sethint             Set a hint for when you forget the password master (i.e sethint your dog\'s name)
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
    version             Get the current version
''')
        
        

