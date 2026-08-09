import tkinter as tk
from tkinter import messagebox

APP_TITLE = "Kalc"
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
FRAME_WIDTH = 450
FRAME_HEIGHT = 350
ww = WINDOW_WIDTH
wh = WINDOW_HEIGHT
fw = FRAME_WIDTH
fh = FRAME_HEIGHT

def login() -> None:
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if username == "" or password == "":
        messagebox.showerror("Error", "Please enter both username and password.")
        return

    messagebox.showinfo("Login", f"Welcome, {username}!")

def quit_program() -> None:
    root.destroy()

root = tk.Tk()
root.title(APP_TITLE)
root.geometry(f"{ww}x{wh}")
root.resizable(False, False)
root.configure(bg="#d9d9d9")

main_frame = tk.Frame(
    root,
    bg="white",
    relief="solid",
    borderwidth=1,
    width=fw,
    height=fh,
)
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

tk.Button(button_frame,text="Quit",width=15,bg="red",fg="white",command=quit_program).grid(row=0, column=1, padx=10)

root.mainloop()
