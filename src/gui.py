import tkinter as tk
from colors import Colors

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

def validate_password(_):
    print(pm.get())



root = tk.Tk()
set_colors()
root.geometry(get_geometry())
root.title("PassLock")
root.resizable(False, False)


# login_frame
login_frame = tk.Frame(root, bg=Colors.PL_GRAY, border=0)
login_frame.place(relx=.5, rely=.5, anchor=tk.CENTER)
login_frame.pack(fill="both", expand=True, pady=200 )

# labels
tk.Label(login_frame, text="PassLock", bg=Colors.PL_GRAY, fg=Colors.PL_PURPLE, font=('Inter', '70', 'bold'), height=1).pack()
tk.Label(login_frame, text="Enter password manager", bg=Colors.PL_GRAY, fg="#eee", font=('Inter 16 bold'), height=5).pack()

# login field
pm = tk.StringVar()
login_field = tk.Entry(login_frame, font=('monospace 20'), width=35, bg=Colors.PL_LGRAY, border=0, borderwidth=0, fg=Colors.PL_LIGHT, show="•", justify="center", textvariable=pm)
login_field.bind("<Return>", func=validate_password)
login_field.pack()

