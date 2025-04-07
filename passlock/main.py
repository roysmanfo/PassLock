import sys
from argparse import ArgumentError

from passlock import login, command 
from passlock.user import User
from passlock.colors import col
from passlock.parser import get_parser

def main():
    """
    ### Point of start of the program
    """
    USER = User()
    USER.key = login.generate_key(USER) if USER.password_manager == b"" else login.login(USER)
    print(f"{col.GREEN}Logged sucessfully{col.RESET}")
    parser = get_parser()
    command.envars.init(user=USER, key=USER.key)
    
    # completely erase the key from memory
    USER.erase_key()

    # There is no need to keep this costant in memory
    # Once everything is set up
    del USER

    args = sys.argv[1:] if (use_sys := len(sys.argv) > 1) else []
    while True:
        try:
            if not use_sys:
                print(f"{col.BLUE}PassLock> {col.RESET}", end='')
                args = input()
                args = args.strip().split(' ')
                while args.count('') > 0:
                    args.remove('')
                args[0].lower()

            parsed_args = parser.parse_args(args)
            if "-h" not in args and "--help" not in args:
                command.run_command(parsed_args)

            if use_sys:
                break
        
        except KeyboardInterrupt:
            print()

        except ArgumentError as e:
            error = e.__str__()

            if error.startswith("argument command: i"):
                error = 'I' + e.__str__().removeprefix('argument command: i')

            elif error.startswith("Invalid choice:"):
                err = error[error.index("'"):error.index("' (choose from")+1].strip()
                error = f"invalid command: {err}"

            print(f'{col.RED}{error}{col.RESET}')
        
        except Exception as e:
            #? has the vault been altered?
            print(f'{col.RED}Err: the vault may have been altered{col.RESET}')
            print(f'{col.RED}{e} {col.RESET}')
            sys.exit(1)
        
        finally:
            # may resolve some parsing issues
            args = []

    sys.exit(0)

if __name__ == '__main__':
    main()
