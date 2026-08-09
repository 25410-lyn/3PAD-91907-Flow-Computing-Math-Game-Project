import tkinter as tk
from tkinter import messagebox
import os 

APP_TITLE = "Kalc"
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
FRAME_WIDTH = 600
FRAME_HEIGHT = 400
ww = WINDOW_WIDTH
wh = WINDOW_HEIGHT
fw = FRAME_WIDTH
fh = FRAME_HEIGHT


LOGIN_FILE = "Login.txt"
lf = LOGIN_FILE

MIN_USERNAME_LENGTH = 4
MAX_USERNAME_LENGTH = 20
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 30
minul = MIN_USERNAME_LENGTH
maxul = MAX_USERNAME_LENGTH
minpl = MIN_PASSWORD_LENGTH
maxpl = MAX_PASSWORD_LENGTH

#This program will have to utilise classes, this first class will have things added to it in future versions.
class Login:
    """This class is used to store the account details for a single user, currently."""

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password



current_player = None


def create_login_file() -> None:
    if not os.path.exists(lf):
        with open(lf, "w", encoding="utf-8") as file:
            file.write("")


def load_accounts() -> dict[str, str]:
    accounts = {}

    with open(lf, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if "," not in line:
                continue

            username, password = line.split(",", 1)
            accounts[username.strip()] = password.strip()

    return accounts


def save_account(player: Login) -> None:
    with open(lf, "a", encoding="utf-8") as file:
        file.write(f"{player.username},{player.password}\n")

def validate_username(username: str) -> bool:
    if len(username) < minul:
        messagebox.showerror("Error", "Username must be at least 4 characters.")
        return False

    if len(username) > maxul:
        messagebox.showerror("Error", "Username must be 20 characters or fewer.")
        return False

    if " " in username or "," in username:
        messagebox.showerror("Error", "Username cannot contain spaces or commas.")
        return False

    return True


def validate_password(password: str) -> bool:
    if len(password) < minul:
        messagebox.showerror("Error", "Password must be at least 8 characters.")
        return False

    if len(password) > maxul:
        messagebox.showerror("Error", "Password must be 30 characters or fewer.")
        return False

    if "," in password:
        messagebox.showerror("Error", "Password cannot contain commas.")
        return False

    return True

def create_account_window() -> None:
    account_window = tk.Toplevel(root)
    account_window.title("Create Account")
    account_window.geometry("400x260")
    account_window.resizable(False, False)

    tk.Label(
        account_window,
        text="Create Account",
        font=("Helvetica", 18, "bold"),
    ).pack(pady=20)

    tk.Label(account_window, text="Username").pack()
    new_username_entry = tk.Entry(account_window, width=30)
    new_username_entry.pack(pady=5)

    tk.Label(account_window, text="Password").pack()
    new_password_entry = tk.Entry(account_window, width=30, show="*")
    new_password_entry.pack(pady=5)

    def create_account() -> None:
        username = new_username_entry.get().strip()
        password = new_password_entry.get().strip()

        if not validate_username(username):
            return

        if not validate_password(password):
            return

        accounts = load_accounts()

        if username in accounts:
            messagebox.showerror("Error", "Username already exists.")
            return

        new_player = Login(username, password)
        save_account(new_player)

        messagebox.showinfo("Success", "Account created successfully.")
        account_window.destroy()

    tk.Button(account_window,text="Create",width=16,bg="royal blue",fg="white",command=create_account,).pack(pady=20)

def login() -> None:
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if username == "" or password == "":
        messagebox.showerror("Error", "Please enter both username and password.")
        return
    accounts = load_accounts()

    if username in accounts and accounts[username] == password:
        current_player = Player(username, password)
        messagebox.showinfo("Login", f"Welcome, {current_player.username}!")
        return

def forgot_password_window() -> None:
    password_window = tk.Toplevel(root)
    password_window.title("Forgot Password")
    password_window.geometry("400x220")
    password_window.resizable(False, False)

    tk.Label(
        password_window,
        text="Forgot Password",
        font=("Helvetica", 18, "bold"),
    ).pack(pady=20)

    tk.Label(password_window, text="Username").pack()

    search_username_entry = tk.Entry(password_window, width=30)
    search_username_entry.pack(pady=5)

    def find_password() -> None:
        username = search_username_entry.get().strip()
        accounts = load_accounts()

        if username in accounts:
            messagebox.showinfo("Password Found", f"Password: {accounts[username]}")
            return

        messagebox.showerror("Error", "Username not found.")

    tk.Button(
        password_window,
        text="Find Password",
        width=16,
        bg="red",
        fg="white",
        command=find_password,
    ).pack(pady=20)

def quit_program() -> None:
    root.destroy()

create_login_file()

root = tk.Tk()
root.title(APP_TITLE)
root.geometry(f"{ww}x{wh}")
root.resizable(False, False)
root.configure(bg="#d9d9d9")

main_frame = tk.Frame(root,bg="white",relief="solid",borderwidth=1,width=fw,height=fh,)
main_frame.place(relx=0.5, rely=0.5, anchor="center")
main_frame.pack_propagate(False)

title_label = tk.Label(main_frame,text="Welcome to Kalc",font=("Helvetica", 24, "bold"),bg="white")
title_label.pack(pady=(35, 30))

form_frame = tk.Frame(main_frame, bg="white")
form_frame.pack(pady=10)

tk.Label(form_frame,text="Username:",font=("Helvetica", 12),bg="white",).grid(row=0, column=0, sticky="w", pady=10)

username_entry = tk.Entry(form_frame, width=25)
username_entry.grid(row=0, column=1, pady=10)

tk.Label(form_frame,text="Password:",font=("Helvetica", 12),bg="white",).grid(row=1, column=0, sticky="w", pady=10)

password_entry = tk.Entry(form_frame, width=25, show="*")
password_entry.grid(row=1, column=1, pady=10)

button_frame = tk.Frame(main_frame, bg="white")
button_frame.pack(pady=25)

tk.Button(button_frame,text="Login",width=15,bg="green",fg="white",command=login,).grid(row=0, column=0, padx=10)

bottom_frame = tk.Frame(main_frame, bg="white")
bottom_frame.pack(side="bottom", pady=25)

tk.Button(bottom_frame,text="Create Account",width=16,bg="royal blue",fg="white",command=create_account_window,).grid(row=0, column=0, padx=10)

tk.Button(bottom_frame,text="Forgot Password",width=16,bg="red",fg="white",command=forgot_password_window,).grid(row=0, column=1, padx=10)

tk.Button(button_frame,text="Quit",width=15,bg="red",fg="white",command=quit_program).grid(row=0, column=1, padx=10)

root.mainloop()