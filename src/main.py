import sys, os
from argparse import ArgumentError

from user import User
import login
import command
from colors import col
from parser import get_parser

VAULT_PATH = os.path.join(os.path.dirname(__file__), "data", "vault.json")

def main():
    """
    ### Point of start of the program
    """
    USER = User(VAULT_PATH)
    USER.key = login.generate_key(USER) if USER.password_manager == b"" else login.login(USER)
    print(f"{col.GREEN}Logged sucessfully{col.RESET}")
    parser = get_parser()
    command.envars.init(user=USER, key=USER.key)
    
    # completely erase the key from memory
    USER.erase_key()

    # There is no need to keep this costant in memory
    # Once everything is set up
    del USER

    while True:
        try:
            args = sys.argv[1:] if (use_sys := len(sys.argv) > 1) else None
            if not use_sys:
                print(f"{col.BLUE}PassLock> {col.RESET}", end='')
                args = input()
                args = args.strip().split(' ')
                while args.count('') > 0:
                    args.remove('')
                args[0].lower()
            command.run_command(args=parser.parse_args(args))

            if use_sys:
                break
        
        except KeyboardInterrupt:
            print()

        except ArgumentError as e:
            error = 'I' + e.__str__().removeprefix('argument command: i')
            print(f'{col.RED}{error}{col.RESET}')
        
        except Exception as e:
            #? has the vault been altered?
            print(f'{col.RED}Err: the vault may have been altered{col.RESET}')
            print(f'{col.RED}{e} {col.RESET}')
            sys.exit(1)

    sys.exit(0)

if __name__ == '__main__':
    main()
