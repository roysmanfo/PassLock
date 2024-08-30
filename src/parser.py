import sys as _sys
import argparse
from collections.abc import Sequence

class Parser(argparse.ArgumentParser):

    def parse_args(self, args: Sequence[str] | None = None, namespace: None = None ) -> argparse.Namespace:
        try: 
            return super().parse_args(args, namespace)
        except:
            if "-h" not in args and "--help" not in args:
                raise
                
    def error(self, message):
        if message:
            self._print_message(message, _sys.stderr)
            print()

    def exit(self, status: int | None = None, message: str | None = None):
        # Check if the help message has been shown
        if not message and not status:
            return
        if message:
            self._print_message(message, _sys.stderr)
            print()

def get_parser() -> Parser:
    parser = Parser(
        prog='PassLock',
        description='Store your passwords localy in a secure way',
        usage='',
        exit_on_error=False,
        add_help=False
    )
    subparser = parser.add_subparsers(dest='command')

    subparser.add_parser('exit', description='Close the application', exit_on_error=False)
    subparser.add_parser('clear', description='Clear the screen', exit_on_error=False)
    subparser.add_parser('help' , description='Display this help message', exit_on_error=False)
    subparser.add_parser('chpass' , description='Change the password manager', exit_on_error=False)

    list_parser = subparser.add_parser('list', description='List all app names', exit_on_error=False)
    list_parser.add_argument('-s', '--sort', action='store_true', help='Sorts the names based on the number of fields')
    list_parser.add_argument('-f', '--files', action='store_true', help='list the files stored in the secure_storage')

    ls_parser = subparser.add_parser('ls', description='List all app names', exit_on_error=False)
    ls_parser.add_argument('-s', '--sort', action='store_true', help='Sorts the names based on the number of fields')
    ls_parser.add_argument('-f', '--files', action='store_true', help='list the files stored in the secure_storage')

    set_parser = subparser.add_parser('set', description='Add/Update the credentials for the specified app (i.e set github.password password )', exit_on_error=False)
    set_parser.add_argument('field', help='field to modify (syntax: app_name.field_name)')
    set_parser.add_argument('new_val', nargs='*', help='New value for the specified field')

    get_parser = subparser.add_parser('get', description='Get all credentials for the specified app (*case insensitive*)', exit_on_error=False)
    get_parser.add_argument('key', help='The app_nane whose the credentials will be shown')

    del_parser = subparser.add_parser('del', description='Delete the credentials of the specified app/field (i.e `del github.phone` or `del github`) from the password vault', exit_on_error=False)
    del_parser.add_argument('key', nargs='*', help='The name of the app/field to delete')

    rm_parser = subparser.add_parser('rm', description='Delete the credentials of the specified app/field (i.e `rm github.phone` or `rm github`) from the password vault', exit_on_error=False)
    rm_parser.add_argument('key', nargs='*', help='The name of the app/field to delete')

    add_parser = subparser.add_parser('add', description='Add the new app/apps to the vault (i.e add github bitcoin work)', exit_on_error=False)
    add_parser.add_argument('key', nargs='*', metavar='app', help='app_name/app_field to add to the password vault')

    rename_parser = subparser.add_parser('rename', description='Rename a key or a field (i.e `rename work.code passkey` or `rename work job`)', exit_on_error=False)
    rename_parser.add_argument('key', metavar='app', help='app_name/app_field to rename in the password vault')
    rename_parser.add_argument('new_val', help='New value for the specified field')

    rnm_parser = subparser.add_parser('rnm', description='Rename a key or a field (i.e `rename work.code passkey` or `rename work job`)', exit_on_error=False)
    rnm_parser.add_argument('key', metavar='app', help='app_name/app_field to rename in the password vault')
    rnm_parser.add_argument('new_val', help='New value for the specified field')

    sethint_parser = subparser.add_parser('sethint', description='Set a hint for when you forget the password master (i.e sethint your dog\'s name)', exit_on_error=False)
    sethint_parser.add_argument('hint', nargs='*',  help='hint (can be a sentence) for when you forget the password master')

    fenc_parser = subparser.add_parser('fenc', description='File Encryption: encrypt 1 or more text file (i.e. fenc file1.txt path/to/file2.txt)', exit_on_error=False)
    fenc_parser.add_argument('files', nargs='+', help='space separated file paths')
    fenc_parser.add_argument("-s", '--save', action='store_true', help='save the encrypted version of the file in the vault')
    fenc_parser.add_argument("-rm", '--remove', action='store_true', help='once the files have been stored in the vault delete the original')

    fdec_parser = subparser.add_parser('fdec', description='File Decryption: decrypt 1 or more text file (i.e. fdec file1.txt path/to/file2.txt)', exit_on_error=False)
    fdec_parser.add_argument('files', nargs='+', help='space separated file paths')
    fdec_parser.add_argument('-s', "--secure-storage", action="store_true", help='this file comes from the secure storage (by default saves the decrypted vestion in the current directory)')
    fdec_parser.add_argument('-rm', "--remove", action="store_true", help='once the files have been decrypted in the vault delete the original')
    fdec_parser.add_argument('-o', dest="output", metavar="outdir", help='the directory where to save the decrypted version of the file (dafault: same of the file )')

    return parser
