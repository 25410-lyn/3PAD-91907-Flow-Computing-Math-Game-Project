# Name: Fuzail Fazal
# Date: 6 July 2026
# Program: Kalc - Maths Game Login and Menu System
# Purpose: This program lets a user create an account to store scores for a math game.

import tkinter as tk
from tkinter import messagebox
import os
from PIL import Image, ImageTk
import random

# main window measurements
APP_TITLE = "Kalc"
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
FRAME_WIDTH = 600
FRAME_HEIGHT = 470
12345678
# shorter names used later so the window sizes are easier to type
ww = WINDOW_WIDTH
wh = WINDOW_HEIGHT
fw = FRAME_WIDTH
fh = FRAME_HEIGHT

# text file where usernames and passwords are saved and also leaderboard scores
LOGIN_FILE = os.path.join(os.path.dirname(__file__), "Login.txt")
lf = LOGIN_FILE
LEAD_FILE = os.path.join(os.path.dirname(__file__), "Leaderboard.txt")
lef = LEAD_FILE

#Image file
IMAGE_FILE = os.path.join(os.path.dirname(__file__), "bac.png")
tk_logo = None
def load_logo():
    global tk_logo
    try:
        pil_comp_logo = Image.open(IMAGE_FILE)
        resized_pil_logo = pil_comp_logo.resize((100, 100))
        tk_logo = ImageTk.PhotoImage(resized_pil_logo)
    except Exception as e:
        tk_logo = None
        print(f"Warning: could not load logo image {IMAGE_FILE}: {e}")

# username and password limits
MIN_USERNAME_LENGTH = 4
MAX_USERNAME_LENGTH = 20
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 30

# shorter versions of the length constants
minul = MIN_USERNAME_LENGTH
maxul = MAX_USERNAME_LENGTH
minpl = MIN_PASSWORD_LENGTH
maxpl = MAX_PASSWORD_LENGTH

# colours used for the interface
BG_COLOUR = "#2D1B69"
CARD_COLOUR = "white"
MAIN_PURPLE = "#6C5CE7"
GREEN = "#2ECC71"
RED = "#E74C3C"
BLUE = "#3498DB"
ORANGE = "#F39C12"
YELLOW = "#F1C40F"
TEXT_COLOUR = "#2D3436"


# stores the username and password of a player
class Player:
    def __init__(self, username, password):
        self.username = username
        self.password = password


# used to remember who is logged in
current_player = None


def file_check():
    # checks if Login.txt exists, and creates it if it is missing
    if os.path.exists(lf) == False:
        loginFile = open(lf, "w", encoding="utf-8")
        loginFile.close()


def read_logins():
    # reads the saved accounts from Login.txt and stores them in a dictionary
    accs = {}

    file = open(lf, "r", encoding="utf-8")
    for line in file:
        line = line.strip()

        # only reads lines that are formatted correctly with a comma
        if "," in line:
            user, pwd = line.split(",", 1)
            accs[user.strip()] = pwd.strip()

    file.close()
    return accs


def save_acc(player):
    # saves a new account to the login file
    file = open(lf, "a", encoding="utf-8")
    file.write("{},{}\n".format(player.username, player.password))
    file.close()


def user_ok(user):
    # checks that the username follows the rules
    if len(user) < minul:
        messagebox.showerror("Error", "Username must be at least 4 characters.")
        return False

    if len(user) > maxul:
        messagebox.showerror("Error", "Username must be 20 characters or fewer.")
        return False

    if " " in user or "," in user:
        messagebox.showerror("Error", "Username cannot contain spaces or commas.")
        return False

    return True


def pass_ok(pwd):
    # checks that the password follows the rules
    if len(pwd) < minpl:
        messagebox.showerror("Error", "Password must be at least 8 characters.")
        return False

    if len(pwd) > maxpl:
        messagebox.showerror("Error", "Password must be 30 characters or fewer.")
        return False

    if "," in pwd:
        messagebox.showerror("Error", "Password cannot contain commas.")
        return False

    return True


def acc_screen():
    # opens a new window where the user can create an account
    acc_win = tk.Toplevel(root)
    acc_win.title("Create Account")
    acc_win.geometry("400x270")
    acc_win.resizable(False, False)
    acc_win.configure(bg=CARD_COLOUR)

    # title and input boxes for the create account screen
    tk.Label(acc_win, text="Create Account", font=("Helvetica", 18, "bold"), bg=CARD_COLOUR, fg=MAIN_PURPLE).pack(pady=20)
    tk.Label(acc_win, text="Username", bg=CARD_COLOUR).pack()
    new_user_ent = tk.Entry(acc_win, width=30)
    new_user_ent.pack(pady=5)

    tk.Label(acc_win, text="Password", bg=CARD_COLOUR).pack()
    new_pass_ent = tk.Entry(acc_win, width=30, show="*")
    new_pass_ent.pack(pady=5)

    def make_acc():
        # gets the username and password typed by the user
        user = new_user_ent.get().strip()
        pwd = new_pass_ent.get().strip()

        # validates the username and password before saving
        if user_ok(user) == False:
            return

        if pass_ok(pwd) == False:
            return

        accounts = read_logins()

        # stops the user from creating the same username twice
        if user in accounts:
            messagebox.showerror("Error", "Username already exists.")
            return

        # creates and saves the new player account
        newPlayer = Player(user, pwd)
        save_acc(newPlayer)

        messagebox.showinfo("Success", "Account created successfully.")
        acc_win.destroy()

    tk.Button(acc_win, text="Create", width=18, height=2, bg=MAIN_PURPLE, fg="white", relief="flat", command=make_acc).pack(pady=20)


def forgot_screen():
    # opens a window where the user can find their password
    pass_win = tk.Toplevel(root)
    pass_win.title("Forgot Password")
    pass_win.geometry("400x230")
    pass_win.resizable(False, False)
    pass_win.configure(bg=CARD_COLOUR)

    tk.Label(pass_win, text="Forgot Password", font=("Helvetica", 18, "bold"), bg=CARD_COLOUR, fg=MAIN_PURPLE).pack(pady=20)
    tk.Label(pass_win, text="Username", bg=CARD_COLOUR).pack()

    find_user_ent = tk.Entry(pass_win, width=30)
    find_user_ent.pack(pady=5)

    def find_pass():
        # searches the login file for the username
        user = find_user_ent.get().strip()
        accs = read_logins()

        # shows the password if the account exists
        if user in accs:
            messagebox.showinfo("Password Found", "Password: " + accs[user])
        else:
            messagebox.showerror("Error", "Username not found.")

    tk.Button(pass_win, text="Find Password", width=18, height=2, bg=RED, fg="white", relief="flat", command=find_pass).pack(pady=20)


def settings():
    # opens the settings window
    set_win = tk.Toplevel(root)
    set_win.title("Settings")
    set_win.geometry("400x250")
    set_win.resizable(False, False)
    set_win.configure(bg=CARD_COLOUR)

    # gets the current username for display
    if current_player != None:
        user = current_player.username
    else:
        user = "Unknown"

    tk.Label(set_win, text="Settings", font=("Helvetica", 20, "bold"), bg=CARD_COLOUR, fg=MAIN_PURPLE).pack(pady=25)
    tk.Label(set_win, text="Logged in as: " + user, font=("Helvetica", 12), bg=CARD_COLOUR, fg=TEXT_COLOUR).pack(pady=10)


def leaderboard():
    # opens the leaderboard window
    lb_win = tk.Toplevel(root)
    lb_win.title("Leaderboard")
    lb_win.geometry("450x350")
    lb_win.resizable(False, False)
    lb_win.configure(bg=CARD_COLOUR)

    # placeholder text until scores are added later
    tk.Label(lb_win, text="Leaderboard", font=("Helvetica", 20, "bold"), bg=CARD_COLOUR, fg=MAIN_PURPLE).pack(pady=25)
    tk.Label(lb_win, text="Scores will show here later.", font=("Helvetica", 12), bg=CARD_COLOUR, fg=TEXT_COLOUR).pack(pady=20)


def start_quiz(diff):
    # temporary message until the real quiz questions are added
    messagebox.showinfo("Kalc", diff + " difficulty selected.")


def diff_screen():
    # opens the difficulty selection screen
    difwin = tk.Toplevel(root)
    difwin.title("Select Difficulty")
    difwin.geometry("{}x{}".format(ww, wh))
    difwin.resizable(False, False)
    difwin.configure(bg=BG_COLOUR)

    # central white frame
    df = tk.Frame(difwin, bg=CARD_COLOUR, relief="flat", width=700, height=520)
    df.place(relx=0.5, rely=0.5, anchor="center")
    df.pack_propagate(False)

    tk.Label(df, text="Select Difficulty", font=("Helvetica", 22, "bold"), bg=CARD_COLOUR, fg=MAIN_PURPLE, width=30).pack(pady=(30, 30))

    # frame that holds the three difficulty buttons
    cards = tk.Frame(df, bg=CARD_COLOUR)
    cards.pack(pady=10)

    # difficulty buttons
    tk.Button(cards, text="Easy", width=14, height=9, bg=GREEN, fg="white", relief="flat", font=("Helvetica", 13, "bold"), command=lambda: start_quiz("Easy")).grid(row=0, column=0, padx=25)
    tk.Button(cards, text="Medium", width=14, height=9, bg=YELLOW, fg="black", relief="flat", font=("Helvetica", 13, "bold"), command=lambda: start_quiz("Medium")).grid(row=0, column=1, padx=25)
    tk.Button(cards, text="Hard", width=14, height=9, bg=RED, fg="white", relief="flat", font=("Helvetica", 13, "bold"), command=lambda: start_quiz("Hard")).grid(row=0, column=2, padx=25)

    # goes back to the main menu
    tk.Button(df, text="Back", width=14, height=2, bg=MAIN_PURPLE, fg="white", relief="flat", command=difwin.destroy).pack(pady=30)


def menu_screen():
    # hides the login screen after the user logs in
    root.withdraw()

    # creates the main menu window
    menuWin = tk.Toplevel(root)
    menuWin.title("Kalc Main Menu")
    menuWin.geometry("{}x{}".format(ww, wh))
    menuWin.resizable(False, False)
    menuWin.configure(bg=BG_COLOUR)

    # makes sure the whole program closes if the main menu is closed
    menuWin.protocol("WM_DELETE_WINDOW", root.destroy)

    # central menu card
    mf = tk.Frame(menuWin, bg=CARD_COLOUR, relief="flat", width=700, height=520)
    mf.place(relx=0.5, rely=0.5, anchor="center")
    mf.pack_propagate(False)

    # top section for logo and account name
    top = tk.Frame(mf, bg=CARD_COLOUR)
    top.pack(fill="x", padx=35, pady=25)

    # gets current logged in username
    if current_player != None:
        user = current_player.username
    else:
        user = "Unknown"

    # logo and account display boxes
    if tk_logo:
        logo_label = tk.Label(top, image=tk_logo, bg="#eeeeee", width=100, height=40)
        logo_label.image = tk_logo
        logo_label.pack(side="left")
    else:
        tk.Label(top, text="No Logo", bg="#eeeeee", width=10, height=4).pack(side="left")
    tk.Label(top, text="Account\n" + user, font=("Helvetica", 10, "bold"), bg="#eeeeee", fg=TEXT_COLOUR, width=12, height=4).pack(side="right")

    # main title
    tk.Label(mf, text="KALC", font=("Helvetica", 44, "bold"), bg=CARD_COLOUR, fg=MAIN_PURPLE, width=10, height=3).pack(pady=(20, 25))

    # frame for main menu buttons
    btns = tk.Frame(mf, bg=CARD_COLOUR)
    btns.pack(side="bottom", pady=35)

    # main menu buttons
    tk.Button(btns, text="Play", width=13, height=2, bg=GREEN, fg="white", relief="flat", command=diff_screen).grid(row=0, column=0, padx=12)
    tk.Button(btns, text="Leaderboard", width=13, height=2, bg=BLUE, fg="white", relief="flat", command=leaderboard).grid(row=0, column=1, padx=12)
    tk.Button(btns, text="Settings", width=13, height=2, bg=ORANGE, fg="white", relief="flat", command=settings).grid(row=0, column=2, padx=12)
    tk.Button(btns, text="Quit", width=13, height=2, bg=RED, fg="white", relief="flat", command=root.destroy).grid(row=0, column=3, padx=12)


def login():
    # checks the details entered on the login screen
    global current_player

    user = username_entry.get().strip()
    pwd = password_entry.get().strip()

    # stops blank login attempts
    if user == "" or pwd == "":
        messagebox.showerror("Error", "Please enter both username and password.")
        return

    accs = read_logins()

    # checks if the username and password match a saved account
    if user in accs and accs[user] == pwd:
        current_player = Player(user, pwd)
        messagebox.showinfo("Login", "Welcome, " + current_player.username + "!")
        menu_screen()
    else:
        messagebox.showerror("Error", "Invalid username or password.")


def close_game():
    # closes the program from the login screen
    root.destroy()


# checks the login file before the GUI starts
file_check()

# creates the main login window
root = tk.Tk()
root.title(APP_TITLE)
root.geometry("{}x{}".format(ww, wh))
root.resizable(False, False)
root.configure(bg=BG_COLOUR)

# create the logo after the root window exists so Tkinter can manage the image object
load_logo()

# main white login card
main_frame = tk.Frame(root, bg=CARD_COLOUR, relief="flat", width=fw, height=fh)
main_frame.place(relx=0.5, rely=0.5, anchor="center")
main_frame.pack_propagate(False)

# title area
tk.Label(main_frame, text="KALC", font=("Helvetica", 34, "bold"), bg=CARD_COLOUR, fg=MAIN_PURPLE).pack(pady=(35, 5))
tk.Label(main_frame, text="Math Game", font=("Helvetica", 12), bg=CARD_COLOUR, fg=TEXT_COLOUR).pack(pady=(0, 30))

# form area for username and password
form = tk.Frame(main_frame, bg=CARD_COLOUR)
form.pack(pady=10)

tk.Label(form, text="Username:", font=("Helvetica", 12), bg=CARD_COLOUR, fg=TEXT_COLOUR).grid(row=0, column=0, sticky="w", pady=10)
username_entry = tk.Entry(form, width=30, font=("Helvetica", 11))
username_entry.grid(row=0, column=1, pady=10, padx=10)

tk.Label(form, text="Password:", font=("Helvetica", 12), bg=CARD_COLOUR, fg=TEXT_COLOUR).grid(row=1, column=0, sticky="w", pady=10)
password_entry = tk.Entry(form, width=30, font=("Helvetica", 11), show="*")
password_entry.grid(row=1, column=1, pady=10, padx=10)

# login and quit buttons
main_btns = tk.Frame(main_frame, bg=CARD_COLOUR)
main_btns.pack(pady=25)

tk.Button(main_btns, text="Login", width=18, height=2, bg=GREEN, fg="white", relief="flat", command=login).grid(row=0, column=0, padx=10)
tk.Button(main_btns, text="Quit", width=18, height=2, bg=RED, fg="white", relief="flat", command=close_game).grid(row=0, column=1, padx=10)

# bottom buttons for extra login options
bottom = tk.Frame(main_frame, bg=CARD_COLOUR)
bottom.pack(side="bottom", pady=30)

tk.Button(bottom, text="Create Account", width=18, bg=MAIN_PURPLE, fg="white", relief="flat", command=acc_screen).grid(row=0, column=0, padx=10)
tk.Button(bottom, text="Forgot Password", width=18, bg=RED, fg="white", relief="flat", command=forgot_screen).grid(row=0, column=1, padx=10)

# lets the user press Enter to login
root.bind("<Return>", lambda event: login())

# starts the program
root.mainloop()
