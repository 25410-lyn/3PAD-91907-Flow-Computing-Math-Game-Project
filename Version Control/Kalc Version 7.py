# Name: Fuzail Fazal
# Date: 22 July 2026
# Program: Kalc - Maths Game
# Purpose: A multiple choice maths game with accounts, scores and different modes.

import tkinter as tk
from tkinter import messagebox
import os
import random
from datetime import datetime
from fractions import Fraction

try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None

try:
    import pygame
except ImportError:
    pygame = None


# window and game settings
APP_TITLE = "Kalc"
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
FRAME_WIDTH = 600
FRAME_HEIGHT = 470
QUESTION_TOTAL = 10
QUESTION_TIME = 20

ww = WINDOW_WIDTH
wh = WINDOW_HEIGHT
fw = FRAME_WIDTH
fh = FRAME_HEIGHT

# files are stored beside the Python program
BASE_FOLDER = os.path.dirname(os.path.abspath(__file__))
LOGIN_FILE = os.path.join(BASE_FOLDER, "Login.txt")
LEAD_FILE = os.path.join(BASE_FOLDER, "Leaderboard.txt")
IMAGE_FILE = os.path.join(BASE_FOLDER, "bac.png")
MUSIC_FILE = os.path.join(BASE_FOLDER, "Bg_music.mp3")
lf = LOGIN_FILE
lef = LEAD_FILE

# account limits
minul = 4
maxul = 20
minpl = 8
maxpl = 30

# interface colours
BG_COLOUR = "#2D1B69"
CARD_COLOUR = "white"
MAIN_PURPLE = "#6C5CE7"
GREEN = "#2ECC71"
RED = "#E74C3C"
BLUE = "#3498DB"
ORANGE = "#F39C12"
YELLOW = "#F1C40F"
TEXT_COLOUR = "#2D3436"
ANSWER_COLOURS = [RED, BLUE, YELLOW, GREEN]


class Player:
    # stores the details for the player who logged in
    def __init__(self, username, password):
        self.username = username
        self.password = password


current_player = None
tk_logo = None
music_volume = 0.4
music_ready = False


def file_check():
    # creates both text files the first time the game runs
    for filename in (lf, lef):
        if os.path.exists(filename) == False:
            file = open(filename, "w", encoding="utf-8")
            file.close()


def load_logo():
    # loads the optional logo without stopping the game if it is missing
    global tk_logo
    if Image is None or os.path.exists(IMAGE_FILE) == False:
        return
    try:
        picture = Image.open(IMAGE_FILE)
        picture = picture.resize((100, 70))
        tk_logo = ImageTk.PhotoImage(picture)
    except Exception as error:
        print("Logo could not be loaded:", error)


def start_music():
    # starts looping background music when pygame and Bg_music.mp3 are available
    global music_ready
    if pygame is None or os.path.exists(MUSIC_FILE) == False:
        return
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(MUSIC_FILE)
        pygame.mixer.music.set_volume(music_volume)
        pygame.mixer.music.play(-1)
        music_ready = True
    except Exception as error:
        print("Music could not be played:", error)


def change_volume(value):
    # changes the live music volume from the settings slider
    global music_volume
    music_volume = float(value) / 100
    if music_ready:
        pygame.mixer.music.set_volume(music_volume)


def read_logins():
    # reads username,password lines and puts them in a dictionary
    accs = {}
    file = open(lf, "r", encoding="utf-8")
    for line in file:
        line = line.strip()
        if "," in line:
            user, pwd = line.split(",", 1)
            accs[user.strip()] = pwd.strip()
    file.close()
    return accs


def save_acc(player):
    file = open(lf, "a", encoding="utf-8")
    file.write("{},{}\n".format(player.username, player.password))
    file.close()


def user_ok(user):
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
    # account creation window
    acc_win = tk.Toplevel(root)
    acc_win.title("Create Account")
    acc_win.geometry("400x300")
    acc_win.configure(bg=CARD_COLOUR)
    acc_win.resizable(False, False)

    tk.Label(acc_win, text="Create Account", font=("Helvetica", 18, "bold"), bg=CARD_COLOUR, fg=MAIN_PURPLE).pack(pady=20)
    tk.Label(acc_win, text="Username", bg=CARD_COLOUR).pack()
    new_user_ent = tk.Entry(acc_win, width=30)
    new_user_ent.pack(pady=5)
    tk.Label(acc_win, text="Password", bg=CARD_COLOUR).pack()
    new_pass_ent = tk.Entry(acc_win, width=30, show="*")
    new_pass_ent.pack(pady=5)

    def make_acc():
        user = new_user_ent.get().strip()
        pwd = new_pass_ent.get().strip()
        if user_ok(user) == False or pass_ok(pwd) == False:
            return
        if user in read_logins():
            messagebox.showerror("Error", "Username already exists.")
            return
        save_acc(Player(user, pwd))
        messagebox.showinfo("Success", "Account created successfully.")
        acc_win.destroy()

    tk.Button(acc_win, text="Create", width=18, height=2, bg=MAIN_PURPLE, fg="white", relief="flat", command=make_acc).pack(pady=20)


def forgot_screen():
    pass_win = tk.Toplevel(root)
    pass_win.title("Forgot Password")
    pass_win.geometry("400x230")
    pass_win.configure(bg=CARD_COLOUR)
    tk.Label(pass_win, text="Forgot Password", font=("Helvetica", 18, "bold"), bg=CARD_COLOUR, fg=MAIN_PURPLE).pack(pady=20)
    find_user_ent = tk.Entry(pass_win, width=30)
    find_user_ent.pack(pady=10)

    def find_pass():
        user = find_user_ent.get().strip()
        accs = read_logins()
        if user in accs:
            messagebox.showinfo("Password Found", "Password: " + accs[user])
        else:
            messagebox.showerror("Error", "Username not found.")

    tk.Button(pass_win, text="Find Password", bg=RED, fg="white", width=18, height=2, relief="flat", command=find_pass).pack(pady=15)


def settings():
    # settings window with a music volume control
    set_win = tk.Toplevel(root)
    set_win.title("Settings")
    set_win.geometry("430x330")
    set_win.configure(bg=CARD_COLOUR)
    user = current_player.username if current_player else "Unknown"
    tk.Label(set_win, text="Settings", font=("Helvetica", 20, "bold"), bg=CARD_COLOUR, fg=MAIN_PURPLE).pack(pady=25)
    tk.Label(set_win, text="Logged in as: " + user, bg=CARD_COLOUR, fg=TEXT_COLOUR).pack(pady=5)
    tk.Label(set_win, text="Music Volume", font=("Helvetica", 12, "bold"), bg=CARD_COLOUR, fg=TEXT_COLOUR).pack(pady=(25, 5))
    slider = tk.Scale(set_win, from_=0, to=100, orient="horizontal", length=270, bg=CARD_COLOUR, highlightthickness=0, command=change_volume)
    slider.set(int(music_volume * 100))
    slider.pack()
    status = "Music ready" if music_ready else "Add Bg_music.mp3 and install pygame to enable music"
    tk.Label(set_win, text=status, bg=CARD_COLOUR, fg=TEXT_COLOUR).pack(pady=10)


# The functions below make one random question and four answer choices.
def answer_set(correct, nearby):
    choices = [str(correct)]
    random.shuffle(nearby)
    for item in nearby:
        item = str(item)
        if item not in choices:
            choices.append(item)
        if len(choices) == 4:
            break
    number = 1
    while len(choices) < 4:
        extra = str(correct + number) if isinstance(correct, int) else str(number)
        if extra not in choices:
            choices.append(extra)
        number += 1
    random.shuffle(choices)
    return choices


def text_answer_set(correct, nearby):
    # makes four different choices for fraction and calculus questions
    choices = [str(correct)]
    for item in nearby:
        item = str(item)
        if item not in choices:
            choices.append(item)
        if len(choices) == 4:
            break
    random.shuffle(choices)
    return choices


def make_question(mode, diff):
    # difficulty changes the size of the randomly selected numbers
    limits = {"Easy": 10, "Medium": 30, "Hard": 100}
    top = limits[diff]

    if mode == "Addition":
        a, b = random.randint(1, top), random.randint(1, top)
        correct = a + b
        return "{} + {} = ?".format(a, b), answer_set(correct, [correct + 1, correct - 1, correct + 10, correct - 10]), str(correct)

    if mode == "Subtraction":
        a, b = random.randint(1, top), random.randint(1, top)
        if diff != "Hard" and b > a:
            a, b = b, a
        correct = a - b
        return "{} - {} = ?".format(a, b), answer_set(correct, [correct + 1, correct - 1, a + b, b - a]), str(correct)

    if mode == "Multiplication":
        mult_top = {"Easy": 10, "Medium": 15, "Hard": 25}[diff]
        a, b = random.randint(2, mult_top), random.randint(2, mult_top)
        correct = a * b
        return "{} × {} = ?".format(a, b), answer_set(correct, [correct + a, correct - a, a + b, correct + b]), str(correct)

    if mode == "Division":
        divisor = random.randint(2, {"Easy": 10, "Medium": 15, "Hard": 25}[diff])
        correct = random.randint(2, {"Easy": 10, "Medium": 20, "Hard": 40}[diff])
        total = divisor * correct
        return "{} ÷ {} = ?".format(total, divisor), answer_set(correct, [correct + 1, correct - 1, divisor, total]), str(correct)

    if mode == "Algebra":
        x = random.randint(1, {"Easy": 10, "Medium": 20, "Hard": 40}[diff])
        coefficient = 1 if diff == "Easy" else random.randint(2, 8)
        add = random.randint(1, top)
        total = coefficient * x + add
        question = "Solve: {}x + {} = {}".format(coefficient, add, total)
        return question, answer_set(x, [x + 1, x - 1, total - add, add]), str(x)

    if mode == "Fractions":
        den = random.randint(2, {"Easy": 8, "Medium": 12, "Hard": 20}[diff])
        a, b = random.randint(1, den - 1), random.randint(1, den - 1)
        operation = random.choice(["+", "-"])
        result = Fraction(a, den) + Fraction(b, den) if operation == "+" else Fraction(a, den) - Fraction(b, den)
        correct = str(result)
        wrong = [str(Fraction(a + b + 1, den)), str(Fraction(a + b, den + 1)), str(Fraction(abs(a - b) + 1, den)), str(Fraction(a, den))]
        choices = [correct]
        for item in wrong:
            if item not in choices:
                choices.append(item)
            if len(choices) == 4:
                break
        while len(choices) < 4:
            item = str(Fraction(random.randint(1, den * 2), den))
            if item not in choices:
                choices.append(item)
        random.shuffle(choices)
        return "{}/{} {} {}/{} = ?".format(a, den, operation, b, den), choices, correct

    if mode == "Differentiation":
        power = random.randint(2, {"Easy": 3, "Medium": 5, "Hard": 8}[diff])
        coefficient = random.randint(1, {"Easy": 5, "Medium": 9, "Hard": 15}[diff])
        new_coefficient = coefficient * power
        new_power = power - 1
        correct = "{}x^{}".format(new_coefficient, new_power)
        choices = text_answer_set(correct, [
            "{}x^{}".format(coefficient, new_power),
            "{}x^{}".format(new_coefficient, power),
            "{}x^{}".format(coefficient + power, new_power),
            "{}x^{}".format(new_coefficient + 1, new_power),
            "{}x^{}".format(coefficient, power + 1)
        ])
        return "Differentiate: {}x^{}".format(coefficient, power), choices, correct

    # integration uses simple powers and does not include + C in the choices
    power = random.randint(1, {"Easy": 2, "Medium": 4, "Hard": 7}[diff])
    new_power = power + 1
    multiplier = random.randint(1, {"Easy": 4, "Medium": 7, "Hard": 10}[diff])
    coefficient = new_power * multiplier
    correct = "{}x^{} + C".format(multiplier, new_power)
    choices = text_answer_set(correct, [
        "{}x^{} + C".format(coefficient, new_power),
        "{}x^{} + C".format(multiplier, power),
        "{}x^{} + C".format(coefficient * power, max(0, power - 1)),
        "{}x^{} + C".format(multiplier + 1, new_power),
        "{}x^{} + C".format(coefficient, power)
    ])
    return "Integrate: {}x^{}".format(coefficient, power), choices, correct


def save_score(score, mode, diff):
    # stores each finished game for the leaderboard
    user = current_player.username if current_player else "Guest"
    file = open(lef, "a", encoding="utf-8")
    file.write("{},{},{},{},{}\n".format(user, score, mode, diff, datetime.now().strftime("%d/%m/%Y")))
    file.close()


def leaderboard():
    # reads saved games and shows the ten highest scores
    lb_win = tk.Toplevel(root)
    lb_win.title("Leaderboard")
    lb_win.geometry("650x520")
    lb_win.configure(bg=CARD_COLOUR)
    tk.Label(lb_win, text="Leaderboard", font=("Helvetica", 22, "bold"), bg=CARD_COLOUR, fg=MAIN_PURPLE).pack(pady=20)
    rows = []
    file = open(lef, "r", encoding="utf-8")
    for line in file:
        parts = line.strip().split(",")
        if len(parts) == 5:
            try:
                rows.append((int(parts[1]), parts[0], parts[2], parts[3], parts[4]))
            except ValueError:
                pass
    file.close()
    rows.sort(reverse=True)
    heading = "{:<4} {:<15} {:<8} {:<17} {:<8}".format("#", "Player", "Score", "Mode", "Level")
    tk.Label(lb_win, text=heading, font=("Courier", 11, "bold"), bg=CARD_COLOUR, fg=TEXT_COLOUR).pack(anchor="w", padx=30)
    if len(rows) == 0:
        tk.Label(lb_win, text="No scores saved yet.", bg=CARD_COLOUR, fg=TEXT_COLOUR).pack(pady=40)
    for place, row in enumerate(rows[:10], 1):
        score, user, mode, diff, date = row
        text = "{:<4} {:<15} {:<8} {:<17} {:<8}".format(place, user[:14], score, mode[:16], diff)
        tk.Label(lb_win, text=text, font=("Courier", 11), bg=CARD_COLOUR, fg=TEXT_COLOUR).pack(anchor="w", padx=30, pady=5)


def quiz_screen(mode, diff, old_window=None):
    # runs ten multiple choice questions with a countdown timer
    if old_window is not None:
        old_window.destroy()
    quizwin = tk.Toplevel(root)
    quizwin.title("Kalc Quiz")
    quizwin.geometry("{}x{}".format(ww, wh))
    quizwin.configure(bg=BG_COLOUR)
    quizwin.protocol("WM_DELETE_WINDOW", quizwin.destroy)

    state = {"number": 0, "score": 0, "time": QUESTION_TIME, "job": None, "answered": False, "correct": ""}
    topbar = tk.Frame(quizwin, bg=BG_COLOUR)
    topbar.pack(fill="x", padx=80, pady=30)
    progress_label = tk.Label(topbar, text="", font=("Helvetica", 15, "bold"), bg=BG_COLOUR, fg="white")
    progress_label.pack(side="left")
    score_label = tk.Label(topbar, text="Score: 0", font=("Helvetica", 15, "bold"), bg=BG_COLOUR, fg="white")
    score_label.pack(side="right")
    timer_label = tk.Label(quizwin, text="", font=("Helvetica", 24, "bold"), bg=BG_COLOUR, fg="white")
    timer_label.pack()
    question_label = tk.Label(quizwin, text="", font=("Helvetica", 24, "bold"), bg="white", fg=TEXT_COLOUR, wraplength=750, width=34, height=5)
    question_label.pack(pady=35)
    answer_frame = tk.Frame(quizwin, bg=BG_COLOUR)
    answer_frame.pack()
    buttons = []
    feedback = tk.Label(quizwin, text="", font=("Helvetica", 28, "bold"), bg=BG_COLOUR, fg="white")
    feedback.pack(pady=30)

    def finish_game():
        if state["job"]:
            quizwin.after_cancel(state["job"])
        save_score(state["score"], mode, diff)
        again = messagebox.askyesno("Quiz Complete", "Final score: {}\n\nPlay this mode again?".format(state["score"]))
        quizwin.destroy()
        if again:
            quiz_screen(mode, diff)
        # if No is selected, the original main menu is already behind this window

    def next_question():
        if state["number"] >= QUESTION_TOTAL:
            finish_game()
            return
        state["number"] += 1
        state["time"] = QUESTION_TIME
        state["answered"] = False
        question, choices, correct = make_question(mode, diff)
        state["correct"] = correct
        progress_label.config(text="{} - {}     Question {}/{}".format(mode, diff, state["number"], QUESTION_TOTAL))
        question_label.config(text=question, bg="white")
        feedback.config(text="")
        for number, button in enumerate(buttons):
            button.config(text=choices[number], state="normal", bg=ANSWER_COLOURS[number])
        tick()

    def tick():
        timer_label.config(text="Time: {}".format(state["time"]), fg="white" if state["time"] > 5 else YELLOW)
        if state["time"] <= 0:
            choose_answer(None)
        else:
            state["time"] -= 1
            state["job"] = quizwin.after(1000, tick)

    def animate_feedback(correct):
        # flashes the question card to give a Kahoot-style result effect
        colours = [GREEN if correct else RED, "white"] * 3
        for number, colour in enumerate(colours):
            quizwin.after(number * 110, lambda c=colour: question_label.config(bg=c))

    def choose_answer(choice):
        if state["answered"]:
            return
        state["answered"] = True
        if state["job"]:
            quizwin.after_cancel(state["job"])
        for button in buttons:
            button.config(state="disabled")
        correct = choice == state["correct"]
        if correct:
            points = 500 + state["time"] * 25
            state["score"] += points
            feedback.config(text="CORRECT!  +{}".format(points), fg=GREEN)
        elif choice is None:
            feedback.config(text="TIME UP!  Answer: " + state["correct"], fg=RED)
        else:
            feedback.config(text="INCORRECT!  Answer: " + state["correct"], fg=RED)
        score_label.config(text="Score: {}".format(state["score"]))
        animate_feedback(correct)
        quizwin.after(1800, next_question)

    for index in range(4):
        button = tk.Button(answer_frame, text="", width=28, height=5, font=("Helvetica", 14, "bold"), fg="white", relief="flat")
        button.grid(row=index // 2, column=index % 2, padx=15, pady=15)
        button.config(command=lambda b=button: choose_answer(b.cget("text")))
        buttons.append(button)

    next_question()


def diff_screen(mode, old_window=None):
    # difficulty is selected after the maths mode
    if old_window is not None:
        old_window.destroy()
    difwin = tk.Toplevel(root)
    difwin.title("Select Difficulty")
    difwin.geometry("{}x{}".format(ww, wh))
    difwin.configure(bg=BG_COLOUR)
    card = tk.Frame(difwin, bg=CARD_COLOUR, width=700, height=520)
    card.place(relx=0.5, rely=0.5, anchor="center")
    card.pack_propagate(False)
    tk.Label(card, text=mode + " Difficulty", font=("Helvetica", 23, "bold"), bg=CARD_COLOUR, fg=MAIN_PURPLE).pack(pady=45)
    buttons = tk.Frame(card, bg=CARD_COLOUR)
    buttons.pack(pady=20)
    tk.Button(buttons, text="Easy", width=14, height=7, bg=GREEN, fg="white", relief="flat", font=("Helvetica", 13, "bold"), command=lambda: quiz_screen(mode, "Easy", difwin)).grid(row=0, column=0, padx=20)
    tk.Button(buttons, text="Medium", width=14, height=7, bg=YELLOW, fg="black", relief="flat", font=("Helvetica", 13, "bold"), command=lambda: quiz_screen(mode, "Medium", difwin)).grid(row=0, column=1, padx=20)
    tk.Button(buttons, text="Hard", width=14, height=7, bg=RED, fg="white", relief="flat", font=("Helvetica", 13, "bold"), command=lambda: quiz_screen(mode, "Hard", difwin)).grid(row=0, column=2, padx=20)
    tk.Button(card, text="Back", width=14, height=2, bg=MAIN_PURPLE, fg="white", relief="flat", command=lambda: mode_screen(difwin)).pack(pady=35)


def mode_screen(old_window=None):
    # shows all eight types of questions before difficulty is chosen
    if old_window is not None:
        old_window.destroy()
    modewin = tk.Toplevel(root)
    modewin.title("Select Mode")
    modewin.geometry("{}x{}".format(ww, wh))
    modewin.configure(bg=BG_COLOUR)
    card = tk.Frame(modewin, bg=CARD_COLOUR, width=800, height=650)
    card.place(relx=0.5, rely=0.5, anchor="center")
    card.pack_propagate(False)
    tk.Label(card, text="Select a Maths Mode", font=("Helvetica", 24, "bold"), bg=CARD_COLOUR, fg=MAIN_PURPLE).pack(pady=35)
    holder = tk.Frame(card, bg=CARD_COLOUR)
    holder.pack()
    modes = ["Algebra", "Addition", "Subtraction", "Division", "Multiplication", "Fractions", "Differentiation", "Integration"]
    colours = [MAIN_PURPLE, GREEN, RED, BLUE, ORANGE, YELLOW, MAIN_PURPLE, BLUE]
    for index, mode in enumerate(modes):
        fg = "black" if mode == "Fractions" else "white"
        button = tk.Button(holder, text=mode, width=18, height=4, bg=colours[index], fg=fg, relief="flat", font=("Helvetica", 12, "bold"), command=lambda m=mode: diff_screen(m, modewin))
        button.grid(row=index // 4, column=index % 4, padx=10, pady=12)
    tk.Button(card, text="Back", width=14, height=2, bg=MAIN_PURPLE, fg="white", relief="flat", command=modewin.destroy).pack(pady=35)


def menu_screen():
    # main menu shown after login
    root.withdraw()
    menu_win = tk.Toplevel(root)
    menu_win.title("Kalc Main Menu")
    menu_win.geometry("{}x{}".format(ww, wh))
    menu_win.configure(bg=BG_COLOUR)
    menu_win.protocol("WM_DELETE_WINDOW", root.destroy)
    card = tk.Frame(menu_win, bg=CARD_COLOUR, width=720, height=560)
    card.place(relx=0.5, rely=0.5, anchor="center")
    card.pack_propagate(False)
    top = tk.Frame(card, bg=CARD_COLOUR)
    top.pack(fill="x", padx=35, pady=25)
    if tk_logo:
        label = tk.Label(top, image=tk_logo, bg="#eeeeee")
        label.image = tk_logo
        label.pack(side="left")
    else:
        tk.Label(top, text="KALC", bg="#eeeeee", width=10, height=4).pack(side="left")
    user = current_player.username if current_player else "Unknown"
    tk.Label(top, text="Account\n" + user, font=("Helvetica", 10, "bold"), bg="#eeeeee", fg=TEXT_COLOUR, width=12, height=4).pack(side="right")
    tk.Label(card, text="KALC", font=("Helvetica", 44, "bold"), bg=CARD_COLOUR, fg=MAIN_PURPLE).pack(pady=45)
    buttons = tk.Frame(card, bg=CARD_COLOUR)
    buttons.pack(side="bottom", pady=40)
    tk.Button(buttons, text="Play", width=13, height=2, bg=GREEN, fg="white", relief="flat", command=mode_screen).grid(row=0, column=0, padx=10)
    tk.Button(buttons, text="Leaderboard", width=13, height=2, bg=BLUE, fg="white", relief="flat", command=leaderboard).grid(row=0, column=1, padx=10)
    tk.Button(buttons, text="Settings", width=13, height=2, bg=ORANGE, fg="white", relief="flat", command=settings).grid(row=0, column=2, padx=10)
    tk.Button(buttons, text="Quit", width=13, height=2, bg=RED, fg="white", relief="flat", command=root.destroy).grid(row=0, column=3, padx=10)


def login():
    global current_player
    user = username_entry.get().strip()
    pwd = password_entry.get().strip()
    if user == "" or pwd == "":
        messagebox.showerror("Error", "Please enter both username and password.")
        return
    accs = read_logins()
    if user in accs and accs[user] == pwd:
        current_player = Player(user, pwd)
        messagebox.showinfo("Login", "Welcome, " + user + "!")
        menu_screen()
    else:
        messagebox.showerror("Error", "Invalid username or password.")


def close_game():
    root.destroy()


# program setup and login screen
file_check()
root = tk.Tk()
root.title(APP_TITLE)
root.geometry("{}x{}".format(ww, wh))
root.resizable(False, False)
root.configure(bg=BG_COLOUR)
load_logo()
start_music()

main_frame = tk.Frame(root, bg=CARD_COLOUR, width=fw, height=fh)
main_frame.place(relx=0.5, rely=0.5, anchor="center")
main_frame.pack_propagate(False)
tk.Label(main_frame, text="KALC", font=("Helvetica", 34, "bold"), bg=CARD_COLOUR, fg=MAIN_PURPLE).pack(pady=(35, 5))
tk.Label(main_frame, text="Math Game", font=("Helvetica", 12), bg=CARD_COLOUR, fg=TEXT_COLOUR).pack(pady=(0, 30))
form = tk.Frame(main_frame, bg=CARD_COLOUR)
form.pack(pady=10)
tk.Label(form, text="Username:", font=("Helvetica", 12), bg=CARD_COLOUR, fg=TEXT_COLOUR).grid(row=0, column=0, sticky="w", pady=10)
username_entry = tk.Entry(form, width=30, font=("Helvetica", 11))
username_entry.grid(row=0, column=1, pady=10, padx=10)
tk.Label(form, text="Password:", font=("Helvetica", 12), bg=CARD_COLOUR, fg=TEXT_COLOUR).grid(row=1, column=0, sticky="w", pady=10)
password_entry = tk.Entry(form, width=30, font=("Helvetica", 11), show="*")
password_entry.grid(row=1, column=1, pady=10, padx=10)
main_btns = tk.Frame(main_frame, bg=CARD_COLOUR)
main_btns.pack(pady=25)
tk.Button(main_btns, text="Login", width=18, height=2, bg=GREEN, fg="white", relief="flat", command=login).grid(row=0, column=0, padx=10)
tk.Button(main_btns, text="Quit", width=18, height=2, bg=RED, fg="white", relief="flat", command=close_game).grid(row=0, column=1, padx=10)
bottom = tk.Frame(main_frame, bg=CARD_COLOUR)
bottom.pack(side="bottom", pady=30)
tk.Button(bottom, text="Create Account", width=18, bg=MAIN_PURPLE, fg="white", relief="flat", command=acc_screen).grid(row=0, column=0, padx=10)
tk.Button(bottom, text="Forgot Password", width=18, bg=RED, fg="white", relief="flat", command=forgot_screen).grid(row=0, column=1, padx=10)
root.bind("<Return>", lambda event: login())
root.mainloop()
