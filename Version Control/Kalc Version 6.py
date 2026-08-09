# ===== Importing modules =====

import tkinter as tk
from tkinter import *
from tkinter import messagebox
import os
from PIL import Image, ImageTk
import random





TXT_FILE = os.path.join(os.path.dirname(__file__), "Login.txt")
LEAD_FILE = os.path.join(os.path.dirname(__file__), "Leaderboard.txt")
IMAGE_FILE = os.path.join(os.path.dirname(__file__), "abc.png")
pil_comp_logo = Image.open(IMAGE_FILE)
resized_logo = pil_comp_logo.resize((100, 100))


root = None
current_user = ""
score = 0
question_number = 0
difficulty = ""


print(os.getcwd())
def file_exist():
    """Create the login file if it does not exist."""
    if not os.path.exists(TXT_FILE):
        with open(TXT_FILE, "w", encoding="utf-8") as f:
            f.write("student,student123\n")


def load_info():
    """Load usernames and passwords from the text file."""
    creds = {}

    with open(TXT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if "," in line:
                username, password = line.split(",", 1)
                creds[username.strip()] = password.strip()

    return creds


def save_info(username, password):
    """Save a new account."""
    with open(TXT_FILE, "a", encoding="utf-8") as f:
        f.write(f"{username},{password}\n")


# ===== Login =====

def login():
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if username == "" or password == "":
        messagebox.showerror(
            "Error",
            "Please enter both username and password."
        )
        return

    creds = load_info()

    if username in creds and creds[username] == password:
        global current_user

        current_user = username

        messagebox.showinfo("Success",f"Welcome, {username}!")

        root.withdraw()
        show_main_menu()
   
    else:
        messagebox.showerror(
            "Error",
            "Invalid username or password."
        )

def create_acc():
    acc_window = tk.Toplevel(root)
    acc_window.title("Create Account")
    acc_window.geometry("400x250")
    acc_window.resizable(False, False)

    tk.Label(
        acc_window,
        text="Create New Account",
        font=("Helvetica", 16, "bold")
    ).pack(pady=15)

    tk.Label(acc_window, text="Username").pack()
    user_entry = tk.Entry(acc_window, width=30)
    user_entry.pack(pady=5)

    tk.Label(acc_window, text="Password").pack()
    pass_entry = tk.Entry(acc_window, width=30, show="*")
    pass_entry.pack(pady=5)

    def save():
        username = user_entry.get().strip()
        password = pass_entry.get().strip()

        if username == "" or password == "":
            messagebox.showerror(
                "Error",
                "Please fill in all fields."
            )
            return

        creds = load_info()

        if username in creds:
            messagebox.showerror(
                "Error",
                "Username already exists."
            )
            return

        save_info(username, password)

        messagebox.showinfo(
            "Success",
            "Account created successfully."
        )

        acc_window.destroy()

    tk.Button(
        acc_window,
        text="Save",
        width=15,
        command=save
    ).pack(pady=20)


# ===== Forgot Password =====

def forgot_pass():
    pass_window = tk.Toplevel(root)
    pass_window.title("Forgot Password")
    pass_window.geometry("400x200")
    pass_window.resizable(False, False)

    tk.Label(
        pass_window,
        text="Forgot Password",
        font=("Helvetica", 16, "bold")
    ).pack(pady=15)

    tk.Label(pass_window, text="Username").pack()

    user_entry = tk.Entry(pass_window, width=30)
    user_entry.pack(pady=5)

    def find():
        username = user_entry.get().strip()

        creds = load_info()

        if username in creds:
            messagebox.showinfo(
                "Password Found",
                f"Password: {creds[username]}"
            )
        else:
            messagebox.showerror(
                "Error",
                "Username not found."
            )

    tk.Button(
        pass_window,
        text="Find Password",
        width=15,
        command=find
    ).pack(pady=20)

def read_leaderboard():
    if not os.path.exists(LEAD_FILE):
        return "No scores yet."

    with open(LEAD_FILE, "r", encoding="utf-8") as f:
        rows = [row.strip() for row in f if row.strip()]

    if len(rows) <= 1:
        return "No scores yet."

    output = []

    for row in rows[1:]:
        output.append(row.replace(",", " : "))

    return "\n".join(output)

def show_leaderboard():
    win = tk.Toplevel(root)
    win.title("Leaderboard")
    win.geometry("500x400")

    tk.Label(
        win,
        text="Leaderboard",
        font=("Helvetica", 18, "bold")
    ).pack(pady=20)

    text = tk.Text(win, width=40, height=15)
    text.pack()

    text.insert("1.0", read_leaderboard())
    text.config(state="disabled")

def show_settings():
    win = tk.Toplevel(root)
    win.title("Settings")
    win.geometry("400x250")

    tk.Label(
        win,
        text="Settings",
        font=("Helvetica", 18, "bold")
    ).pack(pady=20)

    tk.Label(
        win,
        text=f"Logged in as: {current_user}"
    ).pack(pady=10)

    tk.Label(
        win,
        text="Settings coming soon..."
    ).pack()

def show_main_menu():
    comp = ImageTk.PhotoImage(resized_logo)
    menu = tk.Toplevel(root)

    menu.title("Main Menu")
    menu.geometry("1000x1000")
    menu.configure(bg="#0F0F0F")

    card = tk.Frame(
        menu,
        bg="white",
        width=700,
        height=450
    )

    card.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )

    card.pack_propagate(False)

    top = tk.Frame(card, bg="white")
    top.pack(fill="x", pady=20, padx=20)

    comp_label = Label(top, image=comp, width=100, height=100)
    comp_label.pack(side="left")
    comp_label.image = comp

    tk.Label(
        top,
        text=f"User:\n{current_user}",
        bg="#eeeeee",
        width=12,
        height=4
    ).pack(side="right")

    tk.Label(
        card,
        text="Mathdle",
        font=("Helvetica", 28, "bold"),
        bg="white",
        fg="#6C5CE7"
    ).pack(pady=50)

    tk.Label(
        card,
        text="Mathematical Skill Development Tool",
        font=("Helvetica", 12),
        bg="white"
    ).pack()

    button_frame = tk.Frame(card, bg="white")
    button_frame.pack(side="bottom", pady=40)

    tk.Button(
    button_frame,
    text="Play",
    width=12,
    bg="#2ECC71",
    fg="white",
    command=show_difficulty
).grid(row=0, column=0,padx=10)

    tk.Button(
        button_frame,
        text="Leaderboard",
        width=12,
        bg="#3498DB",
        fg="white",
        command=show_leaderboard
    ).grid(row=0, column=1, padx=10)

    tk.Button(
        button_frame,
        text="Settings",
        width=12,
        bg="#F39C12",
        fg="white",
        command=show_settings
    ).grid(row=0, column=2, padx=10)

    tk.Button(
        button_frame,
        text="Quit",
        width=12,
        bg="#E74C3C",
        fg="white",
        command=root.destroy
    ).grid(row=0, column=3, padx=10)



def show_mode_menu(difficulty):
    modwin = tk.Toplevel(root)
    modwin.title("Mod Menu")
    modwin.geometry("1000x1000")

    if difficulty == "Easy":
        modwin = tk.Toplevel(root)
        modwin.title("Mod Menu")
        modwin.geometry("1000x1000")
        tk.Label(modwin, text="Select which topic you'd like to do first", font=("Helvetica", "bold", ))
        tk.Button() 


    


def start_quiz():
    win = tk.Toplevel(root)
    win.title("Quiz")
    win.geometry("1000x1000")

    tk.Label(
        win,
        text="Begin the Quiz!",
        font=("Helvetica", 20, "bold")
    ).pack(pady=20)

def show_difficulty():
    win = tk.Toplevel(root)

    win.title("Select Difficulty")
    win.geometry("600x600")

    tk.Label(
        win,
        text="Select Difficulty",
        font=("Helvetica", 20, "bold")
    ).pack(pady=20)

    tk.Button(
        win,
        text="Easy",
        width=15,
        height=4,
        bg="green",
        fg="white",
        command=lambda: start_quiz("Easy")
    ).pack(pady=10)

    tk.Button(
        win,
        text="Medium",
        width=15,
        height=4,
        bg="orange",
        fg="white",
        command=lambda: start_quiz("Medium")
    ).pack(pady=10)

    tk.Button(
        win,
        text="Hard",
        width=15,
        height=4,
        bg="red",
        fg="white",
        command=lambda: start_quiz("Hard")
    ).pack(pady=10)

def launch():
    global root
    global username_entry
    global password_entry

    root = tk.Tk()

    root.title("Mathematical Skill Development")
    root.geometry("1000x1000")
    root.resizable(False, False)
    root.configure(bg="#d9d9d9")

    main_frame = tk.Frame(
        root,
        bg="white",
        relief="solid",
        borderwidth=1,
        width=450,
        height=350
    )

    main_frame.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )

    welcome_label = tk.Label(
        main_frame,
        text="Welcome",
        font=("Helvetica", 24, "bold"),
        bg="white"
    )

    welcome_label.pack(pady=(30, 40))

    login_frame = tk.Frame(main_frame,bg="white")

    login_frame.pack(pady=10)

    tk.Label(
        login_frame,text="Username:",font=("Helvetica", 12),bg="white").grid(row=0, column=0, sticky="w", pady=10)

    username_entry = tk.Entry(login_frame,width=25)

    username_entry.grid(row=0,column=1,pady=10)

    tk.Label(login_frame,text="Password:",font=("Helvetica", 12),bg="white").grid(row=1, column=0, sticky="w", pady=10)

    password_entry = tk.Entry(login_frame,width=25,show="*")


    password_entry.grid(row=1,column=1,pady=10)

    tk.Button(main_frame, text="Login",width=20,bg="green",fg="white",command=login).pack(pady=25)

    bottom_frame = tk.Frame(main_frame,bg="white")

    bottom_frame.pack(side="bottom", pady=25)

    tk.Button(bottom_frame,text="Create Account",width=16,command=create_acc, bg = "royal blue", fg="white").grid(row=0, column=0, padx=10)

    tk.Button(bottom_frame, text="Forgot Password", width=16, command=forgot_pass, bg="red",fg="white").grid(row=0, column=1, padx=10)

    root.mainloop()


file_exist()
launch()
show_settings()
