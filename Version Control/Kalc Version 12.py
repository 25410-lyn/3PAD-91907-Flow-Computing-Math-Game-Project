# Name: Fuzail Fazal
# Date: 16 July 2026
# Changes: Added Validation for all mode answers.

import tkinter as tk
from tkinter import messagebox
import os
import random
import time
from fractions import Fraction
 
 
try:
    from PIL import Image, ImageTk
    PIL_OK = True
except:
    PIL_OK = False
    Image = None
    ImageTk = None
 
APP_TITLE = "Kalc"
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 600
FRAME_WIDTH = 600
FRAME_HEIGHT = 470
 
WINDOW_WIDTH = WINDOW_WIDTH
WINDOW_HEIGHT = WINDOW_HEIGHT
FRAME_WIDTH = FRAME_WIDTH
FRAME_HEIGHT = FRAME_HEIGHT
 
LOGIN_FILE = os.path.join(os.path.dirname(__file__), "Login.txt")
LEAD_FILE = os.path.join(os.path.dirname(__file__), "Leaderboard.txt")
 
IMAGE_FILE = os.path.join(os.path.dirname(__file__), "bac.png")
tk_logo = None

# username and password limits
MIN_USERNAME_LENGTH = 4
MAX_USERNAME_LENGTH = 20
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 30
 
minul = MIN_USERNAME_LENGTH
maxul = MAX_USERNAME_LENGTH
minpl = MIN_PASSWORD_LENGTH
maxpl = MAX_PASSWORD_LENGTH
 
BG_COLOUR = "#2D1B69"
CARD_COLOUR = "white"
MAIN_PURPLE = "#6C5CE7"
GREEN = "#2ECC71"
RED = "#E74C3C"
BLUE = "#3498DB"
ORANGE = "#F39C12"
YELLOW = "#F1C40F"
TEXT_COLOUR = "#2D3436"
LIGHT_GREY = "#eeeeee"
DEEP_PURPLE = "#170A3A"
HEADER_PURPLE = "#4B168C"
SOFT_PURPLE = "#EEE8FF"
PALE_PURPLE = "#F7F4FF"
CARD_BORDER = "#D9D0F2"
MUTED_TEXT = "#6F6780"
ENTRY_COLOUR = "#F1EEF7"
SUCCESS_BG = "#DDF8E7"
ERROR_BG = "#FFE0E5"
 
TITLE_FONT = ("Segoe UI", 28, "bold")
HEADING_FONT = ("Segoe UI", 18, "bold")
SUBHEADING_FONT = ("Segoe UI", 12, "bold")
BODY_FONT = ("Segoe UI", 11)
SMALL_FONT = ("Segoe UI", 9)
 
GAME_MODES = ["Algebra", "Addition", "Subtraction", "Division", "Multiplication", "Fractions", "Differentiation", "Integration"]

QUESTIONS_PER_QUIZ = 10
TIMER_INTERVAL = 1000
FEEDBACK_DELAY = 1400
LEVEL_BAR_WIDTH = 820
DIFF_TIME = {"Beginner": 30, "Advanced": 20, "Expert": 15}
DIFF_XP = {"Beginner": 10, "Advanced": 15, "Expert": 20}
ANSWER_TOLERANCE = 0.001


class Player:
    def __init__(self, username, password):
        self.username = username
        self.password = password
 
 
class QuizResult:
    def __init__(self, mode, xp_gained, questions_answered,
                 correct_answers, play_seconds):
        self.mode = mode
        self.xp_gained = xp_gained
        self.questions_answered = questions_answered
        self.correct_answers = correct_answers
        self.play_seconds = play_seconds
 
 
current_player = None

def fit_window(window, width, height):
    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()
    x = max((screen_w - width) // 2, 0)
    y = max((screen_h - height) // 2, 0)
    window.geometry("{}x{}+{}+{}".format(width, height, x, y))

 
 
def modern_button(parent, text, command, colour=MAIN_PURPLE, width=16, height=2):
    # makes buttons look consistent and adds a simple hover effect
    btn = tk.Button(parent, text=text, command=command, bg=colour, fg="white",
                    activebackground=colour, activeforeground="white",
                    font=SUBHEADING_FONT, width=width, height=height,
                    relief="flat", bd=0, cursor="hand2")
    btn.bind("<Enter>", lambda event: btn.config(relief="raised"))
    btn.bind("<Leave>", lambda event: btn.config(relief="flat"))
    return btn
 
 
def page_header(parent, title, subtitle="", back_command=None):
    # shared purple header used at the top of the larger screens
    header = tk.Frame(parent, bg=HEADER_PURPLE, height=105)
    header.pack(fill="x")
    header.pack_propagate(False)
 
    title_box = tk.Frame(header, bg=HEADER_PURPLE)
    title_box.pack(side="left", padx=42, pady=17)
    tk.Label(title_box, text=title, font=TITLE_FONT, bg=HEADER_PURPLE,
             fg="white").pack(anchor="w")
    if subtitle != "":
        tk.Label(title_box, text=subtitle, font=BODY_FONT, bg=HEADER_PURPLE,
                 fg="#DCD1F4").pack(anchor="w")
 
    if back_command != None:
        modern_button(header, "Back", back_command, ORANGE, 10, 1).pack(
            side="right", padx=35, pady=28)
    return header
 
 
def stat_card(parent, title, value, colour=SOFT_PURPLE):
    # small card used by the profile and quiz screens
    card = tk.Frame(parent, bg=colour, highlightbackground=CARD_BORDER,
                    highlightthickness=1, width=190, height=92)
    card.pack_propagate(False)
    tk.Label(card, text=title, font=SMALL_FONT, bg=colour,
             fg=MUTED_TEXT).pack(anchor="w", padx=16, pady=(13, 0))
    tk.Label(card, text=value, font=("Segoe UI", 18, "bold"), bg=colour,
             fg=TEXT_COLOUR).pack(anchor="w", padx=16)
    return card
 
 
def clean_answer(text):
    # removes harmless formatting differences before comparing written answers
    text = text.strip().lower()
    text = text.replace(" ", "")
    text = text.replace("×", "*").replace("÷", "/")
    text = text.replace("^", "**")
    return text
 
 
def answer_is_valid(text, mode):
    cleaned = clean_answer(text)
 
    if cleaned == "":
        return False, "Please enter an answer before pressing Submit."
 
    if mode in ["Addition", "Subtraction", "Division", "Multiplication", "Algebra"]:
        try:
            float(cleaned)
            return True, ""
        except:
            return False, "Enter a number only, for example 12 or -4."
 
    if mode == "Fractions":
        try:
            Fraction(cleaned)
            return True, ""
        except:
            return False, "Enter a whole number or fraction, for example 2 or 3/4."
 
    # calculus answers contain x terms, powers and an optional + C
    allowed = "0123456789x+-*/.c()"
    for char in cleaned:
        if char not in allowed:
            return False, "Use numbers, x, powers and + C only."
    if "x" not in cleaned:
        return False, "Your answer needs an x term, for example 6x^2."
    return True, ""
 
 
def answers_match(user_answer, correct_answer, mode):
    # compares an answer after validation and normalisation
    user = clean_answer(user_answer)
    correct = clean_answer(correct_answer)
 
    if mode in ["Addition", "Subtraction", "Division", "Multiplication", "Algebra"]:
        return abs(float(user) - float(correct)) < ANSWER_TOLERANCE
    if mode == "Fractions":
        return Fraction(user) == Fraction(correct)
    return user == correct
 
 
def load_logo():
    # loads the logo image if bac.png exists
    global tk_logo
 
    if PIL_OK == False:
        tk_logo = None
        return
 
    try:
        pil_comp_logo = Image.open(IMAGE_FILE)
        resized_pil_logo = pil_comp_logo.resize((100, 100))
        tk_logo = ImageTk.PhotoImage(resized_pil_logo)
    except Exception:
        tk_logo = None
 
def file_check():
    if os.path.exists(LOGIN_FILE) == False:
        loginFile = open(LOGIN_FILE, "w", encoding="utf-8")
        loginFile.close()
 
    if os.path.exists(LEAD_FILE) == False:
        leadFile = open(LEAD_FILE, "w", encoding="utf-8")
        leadFile.close()
 
 
def read_logins():
    accs = {}
 
    file = open(LOGIN_FILE, "r", encoding="utf-8")
    for line in file:
        line = line.strip()
 
        if "," in line:
            user, pwd = line.split(",", 1)
            accs[user.strip()] = pwd.strip()
 
    file.close()
    return accs
 
 
def save_acc(player):
    # saves a new account to the login file
    file = open(LOGIN_FILE, "a", encoding="utf-8")
    file.write("{},{}\n".format(player.username, player.password))
    file.close()
 
 
def blank_stats():
    # creates blank stats for one game mode
    return {"xp": 0, "answered": 0, "correct": 0, "time": 0}
 
 
def make_user_stats(stats, user):
    if user not in stats:
        stats[user] = {}
 
    for mode in GAME_MODES:
        if mode not in stats[user]:
            stats[user][mode] = blank_stats()
 
 
def read_leads():
    # reads cumulative leaderboard stats from Leaderboard.txt
    stats = {}
 
    file = open(LEAD_FILE, "r", encoding="utf-8")
    for line in file:
        line = line.strip()
        parts = line.split(",")
 
        if len(parts) == 6:
            user = parts[0].strip()
            mode = parts[1].strip()
 
            if mode in GAME_MODES:
                try:
                    xp = int(parts[2])
                    answered = int(parts[3])
                    correct = int(parts[4])
                    play_time = int(parts[5])
 
                    make_user_stats(stats, user)
                    stats[user][mode]["xp"] = xp
                    stats[user][mode]["answered"] = answered
                    stats[user][mode]["correct"] = correct
                    stats[user][mode]["time"] = play_time
                except:
                    pass
 
    file.close()
    return stats
 
 
def write_leads(stats):
    # rewrites Leaderboard.txt with the new cumulative totals
    file = open(LEAD_FILE, "w", encoding="utf-8")
 
    for user in stats:
        make_user_stats(stats, user)
 
        for mode in GAME_MODES:
            xp = stats[user][mode]["xp"]
            answered = stats[user][mode]["answered"]
            correct = stats[user][mode]["correct"]
            play_time = stats[user][mode]["time"]
            file.write("{},{},{},{},{},{}\n".format(user, mode, xp, answered, correct, play_time))
 
    file.close()
 
 
def save_quiz_result(result):
    if current_player == None:
        return
 
    user = current_player.username
    stats = read_leads()
    make_user_stats(stats, user)
 
    stats[user][result.mode]["xp"] += result.xp_gained
    stats[user][result.mode]["answered"] += result.questions_answered
    stats[user][result.mode]["correct"] += result.correct_answers
    stats[user][result.mode]["time"] += result.play_seconds
 
    write_leads(stats)
 
 
def get_accuracy(correct, answered):
    if answered == 0:
        return 0
 
    return round((correct / answered) * 100, 1)
 
def time_text(seconds):
    mins = seconds // 60
    secs = seconds % 60
    return "{}m {}s".format(mins, secs)
 
 
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
 
    else:
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
 
    else:
        return True
 
 
def get_range(diff):
    # gives different number ranges for each difficulty
    if diff == "Beginner":
        return 1, 10
    elif diff == "Advanced":
        return 5, 30
    else:
        return 10, 60
 
 
def term_text(coef, power):
    # formats algebra terms such as 3x^2
    if power == 0:
        return str(coef)
 
    if power == 1:
        if coef == 1:
            return "x"
        elif coef == -1:
            return "-x"
        else:
            return str(coef) + "x"
 
    if coef == 1:
        return "x^" + str(power)
    elif coef == -1:
        return "-x^" + str(power)
    else:
        return str(coef) + "x^" + str(power)
 
 
def make_addition(diff):
    # creates an addition question
    low, high = get_range(diff)
    a = random.randint(low, high)
    b = random.randint(low, high)
    ans = a + b
    return {"question": "{} + {} = ?".format(a, b), "answer": str(ans)}
 
 
def make_subtraction(diff):
    low, high = get_range(diff)
    a = random.randint(low, high)
    b = random.randint(low, high)
 
    if b > a:
        a, b = b, a
 
    ans = a - b
    return {"question": "{} - {} = ?".format(a, b), "answer": str(ans)}
 
 
def make_multiplication(diff):
    if diff == "Beginner":
        a = random.randint(2, 10)
        b = random.randint(2, 10)
    elif diff == "Advanced":
        a = random.randint(4, 15)
        b = random.randint(4, 15)
    else:
        a = random.randint(8, 25)
        b = random.randint(8, 20)
 
    ans = a * b
    return {"question": "{} × {} = ?".format(a, b), "answer": str(ans)}
 
 
def make_division(diff):
    if diff == "Beginner":
        b = random.randint(2, 10)
        ans = random.randint(2, 10)
    elif diff == "Advanced":
        b = random.randint(3, 15)
        ans = random.randint(3, 20)
    else:
        b = random.randint(4, 25)
        ans = random.randint(5, 30)
 
    a = b * ans
    return {"question": "{} ÷ {} = ?".format(a, b), "answer": str(ans)}
 
 
def make_algebra(diff):
    if diff == "Beginner":
        a = random.randint(2, 5)
        x = random.randint(1, 10)
        b = random.randint(1, 10)
    elif diff == "Advanced":
        a = random.randint(3, 9)
        x = random.randint(2, 15)
        b = random.randint(5, 20)
    else:
        a = random.randint(5, 12)
        x = random.randint(-10, 20)
        b = random.randint(-20, 30)
 
    c = (a * x) + b
    ans = x
    return {"question": "Solve for x: {}x + {} = {}".format(a, b, c), "answer": str(ans)}
 
 
def make_fractions(diff):
    if diff == "Beginner":
        max_num = 5
        max_den = 8
        op = random.choice(["+", "-"])
    elif diff == "Advanced":
        max_num = 8
        max_den = 12
        op = random.choice(["+", "-", "×"])
    else:
        max_num = 12
        max_den = 15
        op = random.choice(["+", "-", "×", "÷"])
 
    f1 = Fraction(random.randint(1, max_num), random.randint(2, max_den))
    f2 = Fraction(random.randint(1, max_num), random.randint(2, max_den))
 
    if op == "+":
        ans = f1 + f2
    elif op == "-":
        ans = f1 - f2
    elif op == "×":
        ans = f1 * f2
    else:
        ans = f1 / f2
 
    return {"question": "{} {} {} = ?".format(f1, op, f2), "answer": str(ans)}
 
 
def make_differentiation(diff):
    if diff == "Beginner":
        coef = random.randint(1, 6)
        power = random.randint(2, 4)
    elif diff == "Advanced":
        coef = random.randint(2, 10)
        power = random.randint(2, 6)
    else:
        coef = random.randint(3, 15)
        power = random.randint(3, 8)
 
    ans_coef = coef * power
    ans_power = power - 1
    correct = term_text(ans_coef, ans_power)
    return {"question": "Differentiate: {}".format(term_text(coef, power)), "answer": correct}
 
 
def make_integration(diff):
    if diff == "Beginner":
        ans_coef = random.randint(1, 5)
        ans_power = random.randint(2, 4)
    elif diff == "Advanced":
        ans_coef = random.randint(2, 8)
        ans_power = random.randint(2, 6)
    else:
        ans_coef = random.randint(3, 12)
        ans_power = random.randint(3, 8)
 
    start_coef = ans_coef * ans_power
    start_power = ans_power - 1
    correct = term_text(ans_coef, ans_power) + " + C"
    return {"question": "Integrate: {}".format(term_text(start_coef, start_power)), "answer": correct}
 
 
def make_question(mode, diff):
    # sends the program to the correct question generator
    if mode == "Algebra":
        return make_algebra(diff)
    elif mode == "Addition":
        return make_addition(diff)
    elif mode == "Subtraction":
        return make_subtraction(diff)
    elif mode == "Division":
        return make_division(diff)
    elif mode == "Multiplication":
        return make_multiplication(diff)
    elif mode == "Fractions":
        return make_fractions(diff)
    elif mode == "Differentiation":
        return make_differentiation(diff)
    else:
        return make_integration(diff)


def acc_screen():
    # opens a window where the user can create an account
    acc_win = tk.Toplevel(root)
    acc_win.title("Create Account")
    fit_window(acc_win, 400, 270)
    acc_win.resizable(False, False)
    acc_win.configure(bg=CARD_COLOUR)

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

        if user_ok(user) == False:
            return

        if pass_ok(pwd) == False:
            return

        accounts = read_logins()
        if user in accounts:
            messagebox.showerror("Error", "Username already exists.")
            return

        new_player = Player(user, pwd)
        save_acc(new_player)
        messagebox.showinfo("Success", "Account created successfully.")
        acc_win.destroy()

    tk.Button(acc_win, text="Create", width=18, height=2, bg=MAIN_PURPLE, fg="white", relief="flat", command=make_acc).pack(pady=20)


def forgot_screen():
    # opens a window where the user can find their password
    pass_win = tk.Toplevel(root)
    pass_win.title("Forgot Password")
    fit_window(pass_win, 400, 230)
    pass_win.resizable(False, False)
    pass_win.configure(bg=CARD_COLOUR)

    tk.Label(pass_win, text="Forgot Password", font=("Helvetica", 18, "bold"), bg=CARD_COLOUR, fg=MAIN_PURPLE).pack(pady=20)
    tk.Label(pass_win, text="Username", bg=CARD_COLOUR).pack()
    find_user_ent = tk.Entry(pass_win, width=30)
    find_user_ent.pack(pady=5)

    def find_pass():
        user = find_user_ent.get().strip()
        accs = read_logins()

        if user in accs:
            messagebox.showinfo("Password Found", "Password: " + accs[user])
        else:
            messagebox.showerror("Error", "Username not found.")

    tk.Button(pass_win, text="Find Password", width=18, height=2, bg=RED, fg="white", relief="flat", command=find_pass).pack(pady=20)


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
        messagebox.showinfo("Login", "Welcome, " + current_player.username + "!")
        menu_screen()
    else:
        messagebox.showerror("Error", "Invalid username or password.")
 
 
def close_game():
    root.destroy()
 
def leaderboard():
    # card-based cumulative XP leaderboard
    win = tk.Toplevel(root)
    win.title("Kalc | Leaderboard")
    fit_window(win, 920, 760)
    win.resizable(False, False)
    win.configure(bg=PALE_PURPLE)
    page_header(win, "Leaderboard", "Cumulative XP rankings", win.destroy)
 
    selected = tk.StringVar(value="Overall")
    tabs = tk.Frame(win, bg=PALE_PURPLE)
    tabs.pack(fill="x", padx=35, pady=(22, 12))
 
    board = tk.Frame(win, bg="white", highlightbackground=CARD_BORDER,
                     highlightthickness=1)
    board.pack(fill="both", expand=True, padx=35, pady=(0, 28))
 
    def show_board(mode):
        selected.set(mode)
        for item in board.winfo_children():
            item.destroy()
 
        heading = tk.Frame(board, bg=SOFT_PURPLE, height=48)
        heading.pack(fill="x")
        headings = [("Rank", 8), ("Player", 24), ("XP", 12),
                    ("Questions", 14), ("Accuracy", 14)]
        for text, width in headings:
            tk.Label(heading, text=text, width=width, font=SUBHEADING_FONT,
                     bg=SOFT_PURPLE, fg=TEXT_COLOUR).pack(side="left", pady=13)
 
        stats = read_leads()
        rows = []
        for user in stats:
            make_user_stats(stats, user)
            modes = GAME_MODES if mode == "Overall" else [mode]
            xp = sum(stats[user][m]["xp"] for m in modes)
            answered = sum(stats[user][m]["answered"] for m in modes)
            correct = sum(stats[user][m]["correct"] for m in modes)
            if xp > 0 or answered > 0:
                rows.append((xp, user, answered, get_accuracy(correct, answered)))
        rows.sort(reverse=True)
 
        if len(rows) == 0:
            tk.Label(board, text="No results have been saved for this mode yet.",
                     font=BODY_FONT, bg="white", fg=MUTED_TEXT).pack(pady=80)
            return
 
        for place, row in enumerate(rows[:10], 1):
            xp, user, answered, accuracy = row
            mine = current_player and user == current_player.username
            colour = "#FFF4CE" if mine else ("#FAF8FF" if place % 2 == 0 else "white")
            line = tk.Frame(board, bg=colour, height=48)
            line.pack(fill="x")
            values = [str(place), user, str(xp), str(answered), str(accuracy) + "%"]
            widths = [8, 24, 12, 14, 14]
            for value, width in zip(values, widths):
                tk.Label(line, text=value, width=width, font=BODY_FONT,
                         bg=colour, fg=TEXT_COLOUR).pack(side="left", pady=13)
 
    for i, mode in enumerate(["Overall"] + GAME_MODES):
        tk.Button(tabs, text=mode, font=SMALL_FONT, relief="flat", bd=0,
                  cursor="hand2", bg="white", fg=HEADER_PURPLE,
                  activebackground=SOFT_PURPLE,
                  command=lambda m=mode: show_board(m)).grid(
                      row=i // 5, column=i % 5, padx=4, pady=4, ipadx=10, ipady=7)
    show_board("Overall")
 


def start_quiz(mode, diff):
    # Runs the quiz with a typed answer box instead of multiple choice buttons.
    win = tk.Toplevel(root)
    win.title("Kalc | {} Quiz".format(mode))
    win.geometry("1000x760")
    win.resizable(False, False)
    win.configure(bg=PALE_PURPLE)
    start_music()

    questions = [make_question(mode, diff) for i in range(10)]
    state = {"qnum": 0, "correct": 0, "answered": 0, "xp": 0,
             "time_left": DIFF_TIME[diff], "timer_id": None,
             "start_time": time.time(), "locked": False}

    header = page_header(win, mode + diff, "Type your answer below")
    modern_button(header, "Quit", win.destroy, ORANGE, 9, 1).pack(
        side="right", padx=30, pady=28)

    stats_bar = tk.Frame(win, bg=PALE_PURPLE)
    stats_bar.pack(fill="x", padx=55, pady=18)
    question_stat = stat_card(stats_bar, "QUESTION", "1 / 10")
    question_stat.pack(side="left", padx=6)
    correct_stat = stat_card(stats_bar, "CORRECT", "0")
    correct_stat.pack(side="left", padx=6)
    timer_stat = stat_card(stats_bar, "TIME LEFT", str(DIFF_TIME[diff]), "#FFF4CE")
    timer_stat.pack(side="left", padx=6)
    xp_stat = stat_card(stats_bar, "SESSION XP", "0")
    xp_stat.pack(side="right", padx=6)

    progress = tk.Canvas(win, width=870, height=18, bg=PALE_PURPLE,
                         highlightthickness=0)
    progress.pack()

    feedback = tk.Label(win, text="Enter your answer and press Submit",
                        font=SUBHEADING_FONT, bg=SOFT_PURPLE,
                        fg=HEADER_PURPLE, height=2)
    feedback.pack(fill="x", padx=62, pady=(12, 16))

    question_card = tk.Frame(win, bg=DEEP_PURPLE, height=160)
    question_card.pack(fill="x", padx=62)
    question_card.pack_propagate(False)
    question_label = tk.Label(question_card, text="", font=("Segoe UI", 25, "bold"),
                              bg=DEEP_PURPLE, fg="white", wraplength=800)
    question_label.pack(expand=True)

    answer_row = tk.Frame(win, bg=PALE_PURPLE)
    answer_row.pack(fill="x", padx=62, pady=20)
    tk.Label(answer_row, text="Your answer", font=SUBHEADING_FONT,
             bg=PALE_PURPLE, fg=TEXT_COLOUR).pack(anchor="w")
    answer_entry = tk.Entry(answer_row, font=("Segoe UI", 18), relief="flat",
                            bg=ENTRY_COLOUR, fg=TEXT_COLOUR,
                            insertbackground=HEADER_PURPLE)
    answer_entry.pack(fill="x", ipady=12, pady=(7, 4))
    hint = tk.Label(answer_row, text="", font=SMALL_FONT,
                    bg=PALE_PURPLE, fg=MUTED_TEXT)
    hint.pack(anchor="w")

    submit = modern_button(win, "Submit answer", lambda: check_answer(),
                           MAIN_PURPLE, 34, 2)
    submit.pack()

    def stop_timer():
        if state["timer_id"] != None:
            try:
                win.after_cancel(state["timer_id"])
            except:
                pass
            state["timer_id"] = None

    def close_quiz():
        stop_timer()
        stop_music()
        win.destroy()

    def tick():
        if state["locked"]:
            return
        timer_stat.winfo_children()[1].config(text=str(state["time_left"]))
        if state["time_left"] <= 0:
            mark_answer(None)
        else:
            state["time_left"] -= 1
            state["timer_id"] = win.after(1000, tick)

    def end_quiz():
        stop_timer()
        seconds = int(time.time() - state["start_time"])
        quiz_result = QuizResult(mode, state["xp"], state["answered"],
                                 state["correct"], seconds)
        save_quiz_result(quiz_result)
        stop_music()
        for widget in win.winfo_children():
            if widget != header:
                widget.destroy()
        result = tk.Frame(win, bg="white", highlightbackground=CARD_BORDER,
                          highlightthickness=1)
        result.pack(expand=True, fill="both", padx=150, pady=70)
        tk.Label(result, text="Quiz complete!", font=TITLE_FONT, bg="white",
                 fg=HEADER_PURPLE).pack(pady=(55, 8))
        tk.Label(result, text="{}/10 correct".format(state["correct"]),
                 font=("Segoe UI", 30, "bold"), bg="white",
                 fg=TEXT_COLOUR).pack(pady=10)
        tk.Label(result, text="You earned {} XP in {}".format(
            state["xp"], time_text(seconds)), font=BODY_FONT,
            bg="white", fg=MUTED_TEXT).pack(pady=8)
        modern_button(result, "Back to modes",
                      lambda: [stop_music(), win.destroy(), mode_screen()],
                      MAIN_PURPLE, 20, 2).pack(pady=(30, 8))
        modern_button(result, "View profile", profile_screen,
                      BLUE, 20, 2).pack(pady=8)

    def next_question():
        state["qnum"] += 1
        if state["qnum"] == 10:
            end_quiz()
        else:
            show_question()

    def mark_answer(value):
        if state["locked"]:
            return
        state["locked"] = True
        stop_timer()
        q = questions[state["qnum"]]
        state["answered"] += 1
        submit.config(state="disabled")
        answer_entry.config(state="disabled")

        if value != None and answers_match(value, q["answer"], mode):
            state["correct"] += 1
            state["xp"] += DIFF_XP[diff]
            feedback.config(text="Correct!  +{} XP".format(DIFF_XP[diff]),
                            bg=SUCCESS_BG, fg="#167A3B")
            question_card.config(bg="#167A3B")
            question_label.config(bg="#167A3B")
        elif value == None:
            feedback.config(text="Time up the answer was " + q["answer"],
                            bg=ERROR_BG, fg="#A51E39")
        else:
            feedback.config(text="Not quite the answer was " + q["answer"],
                            bg=ERROR_BG, fg="#A51E39")
            question_card.config(bg="#8E1538")
            question_label.config(bg="#8E1538")
        win.after(1500, next_question)

    def check_answer():
        if state["locked"]:
            return
        value = answer_entry.get()
        valid, problem = answer_is_valid(value, mode)
        if valid == False:
            hint.config(text=problem, fg=RED)
            answer_entry.config(bg=ERROR_BG)
            answer_entry.focus_set()
            win.bell()
            return
        hint.config(text="", fg=MUTED_TEXT)
        answer_entry.config(bg=ENTRY_COLOUR)
        mark_answer(value)

    def show_question():
        stop_timer()
        state["locked"] = False
        state["time_left"] = DIFF_TIME[diff]
        q = questions[state["qnum"]]
        question_label.config(text=q["question"], bg=DEEP_PURPLE)
        question_card.config(bg=DEEP_PURPLE)
        feedback.config(text="Enter your answer and press Submit",
                        bg=SOFT_PURPLE, fg=HEADER_PURPLE)
        answer_entry.config(state="normal", bg=ENTRY_COLOUR)
        answer_entry.delete(0, "end")
        answer_entry.focus_set()
        submit.config(state="normal")
        question_stat.winfo_children()[1].config(
            text="{} / 10".format(state["qnum"] + 1))
        correct_stat.winfo_children()[1].config(text=str(state["correct"]))
        xp_stat.winfo_children()[1].config(text=str(state["xp"]))
        progress.delete("all")
        progress.create_rectangle(0, 2, 870, 16, fill=DEEP_PURPLE, outline="")
        progress.create_rectangle(0, 2, 87 * state["qnum"], 16,
                                  fill=ORANGE, outline="")
        tick()

    win.bind("<Return>", lambda event: check_answer())
    win.protocol("WM_DELETE_WINDOW", close_quiz)
    show_question()

def mode_screen():
    win = tk.Toplevel(root)
    win.title("Kalc | Select Mode")
    fit_window(win, 1000, 760)
    win.resizable(False, False)
    win.configure(bg=PALE_PURPLE)
    page_header(win, "Choose a mode", "Which maths skill would you like to practise?",win.destroy)
 
    grid = tk.Frame(win, bg=PALE_PURPLE)
    grid.pack(expand=True, padx=55, pady=35)
    colours = [MAIN_PURPLE, GREEN, RED, BLUE, ORANGE, "#D6A900","#7D4CC2", "#238B8B"]
    symbols = ["x=?", "+", "-", "÷", "×", "x/y", "d/dx", "∫"]
 
    def choose(mode):
        win.destroy()
        diff_screen(mode)
 
    for i, mode in enumerate(GAME_MODES):
        card = tk.Frame(grid, bg="white", highlightbackground=CARD_BORDER,highlightthickness=1, width=205, height=205)
        card.grid(row=i // 4, column=i % 4, padx=10, pady=10)
        card.pack_propagate(False)
        tk.Label(card, text=symbols[i], font=("Segoe UI", 36, "bold"),bg="white", fg=colours[i]).pack(pady=(25, 5))
        tk.Label(card, text=mode, font=SUBHEADING_FONT, bg="white",fg=TEXT_COLOUR).pack()
        modern_button(card, "Choose", lambda m=mode: choose(m),colours[i], 13, 1).pack(pady=18)
 
 
def diff_screen(mode):
    win = tk.Toplevel(root)
    win.title("Kalc | Select Difficulty")
    fit_window(win, 1000, 700)
    win.resizable(False, False)
    win.configure(bg=PALE_PURPLE)
    page_header(win, mode, "Choose a difficulty level",lambda: [win.destroy(), mode_screen()])
 
    cards = tk.Frame(win, bg=PALE_PURPLE)
    cards.pack(expand=True)
    info = [("Beginner", GREEN, "Relaxed pace", "30 seconds", "10 XP"),("Advanced", "#D6A900", "A balanced challenge", "20 seconds", "15 XP"),("Expert", RED, "Fast and demanding", "15 seconds", "20 XP")]
    for i, item in enumerate(info):
        name, colour, desc, timer, xp = item
        card = tk.Frame(cards, bg="white", highlightbackground=colour,highlightthickness=3, width=250, height=330)
        card.grid(row=0, column=i, padx=18)
        card.pack_propagate(False)
        tk.Label(card, text=name, font=("Segoe UI", 24, "bold"),bg="white", fg=colour).pack(pady=(38, 8))
        tk.Label(card, text=desc, font=BODY_FONT, bg="white",fg=MUTED_TEXT).pack()
        tk.Label(card, text=timer + " per question", font=SUBHEADING_FONT,bg="white", fg=TEXT_COLOUR).pack(pady=(35, 6))
        tk.Label(card, text=xp + " per correct answer", font=BODY_FONT,bg="white", fg=TEXT_COLOUR).pack()
        modern_button(card, "Start quiz",lambda d=name: [win.destroy(), start_quiz(mode, d)],colour, 16, 2).pack(pady=42)
 
 
def menu_screen():
    root.withdraw()
    win = tk.Toplevel(root)
    win.title("Kalc | Main Menu")
    fit_window(win, 1000, 760)
    win.resizable(False, False)
    win.configure(bg=PALE_PURPLE)
    win.protocol("WM_DELETE_WINDOW", root.destroy)
 
    user = current_player.username if current_player else "Unknown"
    header = page_header(win, "KALC")
    modern_button(header, user, MAIN_PURPLE).pack(side="right", padx=30, pady=28)
 
    hero = tk.Frame(win, bg=DEEP_PURPLE, height=205)
    hero.pack(fill="x", padx=48, pady=(35, 22))
    hero.pack_propagate(False)
    tk.Label(hero, text="Ready for your next challenge?", font=TITLE_FONT,bg=DEEP_PURPLE, fg="white").pack(anchor="w", padx=38, pady=(35, 5))
    tk.Label(hero, text="Choose from eight mode and slowly build up your skills.",font=BODY_FONT, bg=DEEP_PURPLE, fg="#DCD1F4").pack(anchor="w", padx=38)
    modern_button(hero, "Play now", mode_screen, GREEN, 16, 2).pack(anchor="w", padx=38, pady=22)
 
    actions = tk.Frame(win, bg=PALE_PURPLE)
    actions.pack(fill="both", expand=True, padx=40)
    options = [("Leaderboard", "Compare XP rankings", BLUE, leaderboard),("Quit", "Close Kalc safely", RED, close_game)]
    for i, item in enumerate(options):
        title, desc, colour, command = item
        card = tk.Frame(actions, bg="white", highlightbackground=CARD_BORDER,highlightthickness=1, width=215, height=210)
        card.grid(row=0, column=i, padx=8, pady=8)
        card.pack_propagate(False)
        tk.Label(card, text=title, font=HEADING_FONT, bg="white",fg=colour).pack(pady=(27, 8))
        tk.Label(card, text=desc, font=SMALL_FONT, bg="white",fg=MUTED_TEXT, wraplength=170).pack()
        modern_button(card, "Close", command, colour, 13, 1).pack(pady=24)
 
 
def main():
    global root, username_entry, password_entry
 
    file_check()
    root = tk.Tk()
    root.title(APP_TITLE)
    fit_window(root, WINDOW_WIDTH, WINDOW_HEIGHT)
    root.resizable(False, False)
    root.configure(bg=DEEP_PURPLE)
    root.protocol("WM_DELETE_WINDOW", close_game)
 
    # The logo is optional, so the program still runs when bac.png is absent.
    load_logo()
    main_frame = tk.Frame(root, bg=CARD_COLOUR, relief="flat", width=620,
                          height=610, highlightbackground=CARD_BORDER,
                          highlightthickness=1)
    main_frame.place(relx=0.5, rely=0.5, anchor="center")
    main_frame.pack_propagate(False)
 
    tk.Label(main_frame, text="KALC", font=("Segoe UI", 42, "bold"),
             bg=CARD_COLOUR, fg=HEADER_PURPLE).pack(pady=(45, 2))
 
    form = tk.Frame(main_frame, bg=CARD_COLOUR)
    form.pack(pady=10)
    tk.Label(form, text="Username", font=SUBHEADING_FONT,
             bg=CARD_COLOUR, fg=TEXT_COLOUR).grid(
                 row=0, column=0, sticky="w", pady=(4, 6))
    username_entry = tk.Entry(form, width=35, font=("Segoe UI", 13),
                              relief="flat", bg=ENTRY_COLOUR, fg=TEXT_COLOUR)
    username_entry.grid(row=1, column=0, ipady=10, pady=(0, 18))
 
    tk.Label(form, text="Password", font=SUBHEADING_FONT,
             bg=CARD_COLOUR, fg=TEXT_COLOUR).grid(
                 row=2, column=0, sticky="w", pady=(4, 6))
    password_entry = tk.Entry(form, width=35, font=("Segoe UI", 13), show="*",
                              relief="flat", bg=ENTRY_COLOUR, fg=TEXT_COLOUR)
    password_entry.grid(row=3, column=0, ipady=10, pady=(0, 8))
 
    main_btns = tk.Frame(main_frame, bg=CARD_COLOUR)
    main_btns.pack(pady=18)
    modern_button(main_btns, "Log in", login, GREEN, 18, 2).grid(
        row=0, column=0, padx=7)
    modern_button(main_btns, "Quit", close_game, RED, 18, 2).grid(
        row=0, column=1, padx=7)
 
    bottom = tk.Frame(main_frame, bg=CARD_COLOUR)
    bottom.pack(side="bottom", pady=35)
    modern_button(bottom, "Create account", acc_screen,
                  MAIN_PURPLE, 18, 1).grid(row=0, column=0, padx=7)
    modern_button(bottom, "Forgot password", forgot_screen,
                  BLUE, 18, 1).grid(row=0, column=1, padx=7)
 
    root.bind("<Return>", lambda event: login())
    root.mainloop()
 
 
if __name__ == "__main__":
    main()