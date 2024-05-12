from vault import vault
import gui



def main():
    """
    ### Point of start of the program
    """
    # USER = User(vault.path)
    # USER.key = login.generate_key(USER) if USER.password_manager == b"" else login.login(USER)
    
    gui.root.mainloop()
if __name__ == '__main__':
    main()
    try:
        vault.connection.close()
    except:
        pass