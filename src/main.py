import gui
import auth
from vault import vault


if __name__ == '__main__':

    if vault.empty:
        vault.key = auth.register(vault, "PassLock")

    gui.page.login_page(auth.validate_password)
    gui.root.mainloop()

    try:
        vault.connection.close()
    except:
        pass