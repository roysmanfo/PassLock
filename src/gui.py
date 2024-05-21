from enum import IntEnum, auto
import tkinter as tk
from typing import Callable
from colors import Colors


class PageEnum(IntEnum):
    LOGIN = auto()
    MAIN  = auto()

def get_geometry() -> str:
    """
    - aspect_ratio  |  16 / 9
    - width         |  75% of screen
    - position      |  center center
    """

    width = int(root.winfo_screenwidth() * .75)
    height = width // 16 * 9
    x = int(root.winfo_screenwidth() / 2 - width / 2 )
    y = int(root.winfo_screenheight() / 2 - height / 2)

    return "%dx%d+%d+%d" % (width, height, x, y)

def set_colors():
    root.configure(bg=Colors.PL_GRAY)    


def setup_window():
    set_colors()
    root.geometry(get_geometry())
    root.title("PassLock")
    root.resizable(False, False)

class Pages:
    current_page: PageEnum

    @staticmethod
    def goto_page(page: PageEnum, *args, **kwargs) -> None:
        match page:
            case PageEnum.LOGIN: Pages.login_page(*args, *kwargs)
            case PageEnum.MAIN: Pages.main_page(*args, *kwargs)
            
            # for now use this as 404, even if this case should not happen
            case _: Pages.login_page(*args, *kwargs)

    @staticmethod
    def login_page(validate_password: Callable[[str], bool]):

        def getpasswd(_):
            passwd = pm.get()
            if validate_password(passwd):
                login_frame.destroy()
                Pages.goto_page(PageEnum.MAIN)

        Pages.current_page = PageEnum.LOGIN


        # login_frame
        login_frame = tk.Frame(root, bg=Colors.PL_GRAY, border=0)
        login_frame.place(relx=.5, rely=.5, anchor=tk.CENTER)
        login_frame.pack(fill="both", expand=True, pady=200)

        # labels
        tk.Label(login_frame, text="PassLock", bg=Colors.PL_GRAY, fg=Colors.PL_PURPLE, font=('Inter', '70', 'bold'), height=1).pack()
        tk.Label(login_frame, text="Enter password manager", bg=Colors.PL_GRAY, fg="#eee", font=('Inter 16 bold'), height=5).pack()

        # login field
        pm = tk.StringVar()
        login_field = tk.Entry(login_frame, font=('monospace 20'), width=35, bg=Colors.PL_LGRAY, border=0, borderwidth=0, fg=Colors.PL_LIGHT, show="•", justify="center", textvariable=pm)
        login_field.bind("<Return>", func=getpasswd)
        login_field.pack()

    @staticmethod
    def main_page():
        Pages.current_page = PageEnum.LOGIN
        tk.Label(root, text="Main Page", bg=Colors.PL_GRAY, fg=Colors.PL_PURPLE, font=('Inter', '70', 'bold'), height=1).pack()



root = tk.Tk()
page: Pages = Pages()
setup_window()
