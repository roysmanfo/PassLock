import argparse

def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog='PassLock',
        description='Store your passwords localy in a secure way',
        usage='{ exit, clear, help, list, ls, set, get, del, rm, add, rename, rnm } ...',
        exit_on_error=False,
        add_help=False
    )
    subparser = parser.add_subparsers(dest='command')

    general_parser = subparser.add_parser('exit', help='Close the application', exit_on_error=False)
    general_parser = subparser.add_parser('clear', help='Clear the screen', exit_on_error=False)
    general_parser = subparser.add_parser('help' , help='Display this help message', exit_on_error=False)

    list_parser = subparser.add_parser('list', help='List all app names', exit_on_error=False)
    list_parser.add_argument('-s', '--sort', action='store_true', help='Sorts the names based on the number of fields')

    ls_parser = subparser.add_parser('ls', help='List all app names', exit_on_error=False)
    ls_parser.add_argument('-s', '--sort', action='store_true', help='Sorts the names based on the number of fields')

    set_parser = subparser.add_parser('set', help='Add/Update the credentials for the specified app (i.e set github.password password )', exit_on_error=False)
    set_parser.add_argument('field', help='field to modify (syntax: app_name.field_name)')
    set_parser.add_argument('new_val', nargs='*', help='New value for the specified field')

    get_parser = subparser.add_parser('get', help='Get all credentials for the specified app (*case insensitive*)', exit_on_error=False)
    get_parser.add_argument('key', help='The app_nane whose the credentials will be shown')

    del_parser = subparser.add_parser('del', help='Delete the credentials of the specified app/field (i.e `del github.phone` or `del github`) from the password vault', exit_on_error=False)
    del_parser.add_argument('key', nargs='*', help='The name of the app/field to delete')

    rm_parser = subparser.add_parser('rm', help='Delete the credentials of the specified app/field (i.e `rm github.phone` or `rm github`) from the password vault', exit_on_error=False)
    rm_parser.add_argument('key', nargs='*', help='The name of the app/field to delete')

    add_parser = subparser.add_parser('add', help='Add the new app/apps to the vault (i.e add github bitcoin work)', exit_on_error=False)
    add_parser.add_argument('key', nargs='*', metavar='app', help='app_name/app_field to add to the password vault')

    rename_parser = subparser.add_parser('rename', help='Rename a key or a field (i.e `rename work.code passkey` or `rename work job`)', exit_on_error=False)
    rename_parser.add_argument('key', metavar='app', help='app_name/app_field to rename in the password vault')
    rename_parser.add_argument('new_val', help='New value for the specified field')

    rnm_parser = subparser.add_parser('rnm', help='Rename a key or a field (i.e `rename work.code passkey` or `rename work job`)', exit_on_error=False)
    rnm_parser.add_argument('key', metavar='app', help='app_name/app_field to rename in the password vault')
    rnm_parser.add_argument('new_val', help='New value for the specified field')

    return parser