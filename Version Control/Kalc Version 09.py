# Name: Fuzail Fazal
# Date: 6 July 2026
# Changes made: Added the redesigned maths mode selection screen.

import tkinter as tk
from tkinter import messagebox
import os
import random
import time
from fractions import Fraction

# tries to import pillow for the logo image
try:
    from PIL import Image, ImageTk
    PIL_OK = True
except:
    PIL_OK = False
    Image = None
    ImageTk = None

# tries to import pygame for background music
try:
    import pygame
    MUSIC_OK = True
except:
    pygame = None
    MUSIC_OK = False

# main window measurements
APP_TITLE = "Kalc"
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 1000
FRAME_WIDTH = 600
FRAME_HEIGHT = 470

# shorter names used later so the window sizes are easier to type
ww = WINDOW_WIDTH
wh = WINDOW_HEIGHT
fw = FRAME_WIDTH
fh = FRAME_HEIGHT

# text files where accounts and scores are saved
LOGIN_FILE = os.path.join(os.path.dirname(__file__), "Login.txt")
lf = LOGIN_FILE
LEAD_FILE = os.path.join(os.path.dirname(__file__), "Leaderboard.txt")
lef = LEAD_FILE

# image and music files
IMAGE_FILE = os.path.join(os.path.dirname(__file__), "bac.png")
MUSIC_FILE = os.path.join(os.path.dirname(__file__), "music.mp3")

tk_logo = None
music_loaded = False
music_volume = 0.30

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

# fonts are kept here so every screen has the same style
TITLE_FONT = ("Segoe UI", 28, "bold")
HEADING_FONT = ("Segoe UI", 18, "bold")
SUBHEADING_FONT = ("Segoe UI", 12, "bold")
BODY_FONT = ("Segoe UI", 11)
SMALL_FONT = ("Segoe UI", 9)

# maths modes used in the game
GAME_MODES = ["Algebra", "Addition", "Subtraction", "Division", "Multiplication", "Fractions", "Differentiation", "Integration"]

# level and xp settings
XP_PER_LEVEL = 100
DIFF_TIME = {"Easy": 30, "Medium": 20, "Hard": 15}
DIFF_XP = {"Easy": 10, "Medium": 15, "Hard": 20}


# stores the username and password of a player
class Player:
    def __init__(self, username, password):
        self.username = username
        self.password = password


# used to remember who is logged in
current_player = None


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
    text = text.replace("Ã—", "*").replace("Ã·", "/")
    text = text.replace("^", "**")
    return text


def answer_is_valid(text, mode):
    # checks the type and format of the answer before it is marked
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
        return abs(float(user) - float(correct)) < 0.000001
    if mode == "Fractions":
        return Fraction(user) == Fraction(correct)
    return user == correct


def load_logo():
    # loads the logo image if bac.png exists
    global tk_logo

    if PIL_OK == False:
        tk_logo = None
        print("Warning: Pillow is not installed, so the logo cannot be loaded.")
        return

    try:
        pil_comp_logo = Image.open(IMAGE_FILE)
        resized_pil_logo = pil_comp_logo.resize((100, 100))
        tk_logo = ImageTk.PhotoImage(resized_pil_logo)
    except Exception as e:
        tk_logo = None
        print("Warning: could not load logo image {}: {}".format(IMAGE_FILE, e))


def start_music():
    # starts background music if pygame and music.mp3 are available
    global music_loaded

    if MUSIC_OK == False:
        music_loaded = False
        print("Warning: pygame is not installed, so music is turned off.")
        return

    if os.path.exists(MUSIC_FILE) == False:
        music_loaded = False
        print("Warning: music.mp3 was not found, so music is turned off.")
        return

    try:
        pygame.mixer.init()
        pygame.mixer.music.load(MUSIC_FILE)
        pygame.mixer.music.set_volume(music_volume)
        pygame.mixer.music.play(-1)
        music_loaded = True
    except Exception as e:
        music_loaded = False
        print("Warning: music could not start: {}".format(e))


def change_volume(value):
    # changes the background music volume from the settings slider
    global music_volume

    music_volume = float(value) / 100

    if MUSIC_OK and music_loaded:
        pygame.mixer.music.set_volume(music_volume)


def file_check():
    # checks if Login.txt exists, and creates it if it is missing
    if os.path.exists(lf) == False:
        loginFile = open(lf, "w", encoding="utf-8")
        loginFile.close()

    # checks if Leaderboard.txt exists, and creates it if it is missing
    if os.path.exists(lef) == False:
        leadFile = open(lef, "w", encoding="utf-8")
        leadFile.close()


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


def blank_stats():
    # creates blank stats for one game mode
    return {"xp": 0, "answered": 0, "correct": 0, "time": 0}


def make_user_stats(stats, user):
    # makes sure a user has every mode saved in the leaderboard data
    if user not in stats:
        stats[user] = {}

    for mode in GAME_MODES:
        if mode not in stats[user]:
            stats[user][mode] = blank_stats()


def read_leads():
    # reads cumulative leaderboard stats from Leaderboard.txt
    stats = {}

    file = open(lef, "r", encoding="utf-8")
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
                    print("Bad leaderboard line skipped:", line)

    file.close()
    return stats


def write_leads(stats):
    # rewrites Leaderboard.txt with the new cumulative totals
    file = open(lef, "w", encoding="utf-8")

    for user in stats:
        make_user_stats(stats, user)

        for mode in GAME_MODES:
            xp = stats[user][mode]["xp"]
            answered = stats[user][mode]["answered"]
            correct = stats[user][mode]["correct"]
            play_time = stats[user][mode]["time"]
            file.write("{},{},{},{},{},{}\n".format(user, mode, xp, answered, correct, play_time))

    file.close()


def save_quiz_result(mode, xp_gained, questions_answered, correct_answers, play_seconds):
    # adds the latest quiz result to the user's total data
    if current_player == None:
        return

    user = current_player.username
    stats = read_leads()
    make_user_stats(stats, user)

    stats[user][mode]["xp"] += xp_gained
    stats[user][mode]["answered"] += questions_answered
    stats[user][mode]["correct"] += correct_answers
    stats[user][mode]["time"] += play_seconds

    write_leads(stats)


def get_accuracy(correct, answered):
    # works out accuracy as a percentage
    if answered == 0:
        return 0

    return round((correct / answered) * 100, 1)


def get_level(total_xp):
    # gives the player one level every 100 xp
    return (total_xp // XP_PER_LEVEL) + 1


def time_text(seconds):
    # changes seconds into minutes and seconds
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


def get_range(diff):
    # gives different number ranges for each difficulty
    if diff == "Easy":
        return 1, 10
    elif diff == "Medium":
        return 5, 30
    else:
        return 10, 60


def make_choices(correct, wrongs):
    # makes four multiple choice answers with the correct answer included
    correct = str(correct)
    choices = [correct]

    for wrong in wrongs:
        wrong = str(wrong)
        if wrong not in choices:
            choices.append(wrong)
        if len(choices) == 4:
            break

    # fills missing answers if there were duplicates
    while len(choices) < 4:
        fake = str(random.randint(-50, 150))
        if fake not in choices:
            choices.append(fake)

    random.shuffle(choices)
    return choices


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
    wrongs = [ans + random.randint(1, 5), ans - random.randint(1, 5), a * b, ans + 10]
    return {"question": "{} + {} = ?".format(a, b), "answer": str(ans), "choices": make_choices(ans, wrongs)}


def make_subtraction(diff):
    # creates a subtraction question
    low, high = get_range(diff)
    a = random.randint(low, high)
    b = random.randint(low, high)

    if b > a:
        a, b = b, a

    ans = a - b
    wrongs = [ans + random.randint(1, 5), ans - random.randint(1, 5), a + b, ans + 10]
    return {"question": "{} - {} = ?".format(a, b), "answer": str(ans), "choices": make_choices(ans, wrongs)}


def make_multiplication(diff):
    # creates a multiplication question
    if diff == "Easy":
        a = random.randint(2, 10)
        b = random.randint(2, 10)
    elif diff == "Medium":
        a = random.randint(4, 15)
        b = random.randint(4, 15)
    else:
        a = random.randint(8, 25)
        b = random.randint(8, 20)

    ans = a * b
    wrongs = [ans + a, ans - b, ans + random.randint(2, 12), a + b]
    return {"question": "{} Ã— {} = ?".format(a, b), "answer": str(ans), "choices": make_choices(ans, wrongs)}


def make_division(diff):
    # creates a division question with a whole number answer
    if diff == "Easy":
        b = random.randint(2, 10)
        ans = random.randint(2, 10)
    elif diff == "Medium":
        b = random.randint(3, 15)
        ans = random.randint(3, 20)
    else:
        b = random.randint(4, 25)
        ans = random.randint(5, 30)

    a = b * ans
    wrongs = [ans + 1, ans - 1, ans + b, b]
    return {"question": "{} Ã· {} = ?".format(a, b), "answer": str(ans), "choices": make_choices(ans, wrongs)}


def make_algebra(diff):
    # creates a simple solve for x algebra question
    if diff == "Easy":
        a = random.randint(2, 5)
        x = random.randint(1, 10)
        b = random.randint(1, 10)
    elif diff == "Medium":
        a = random.randint(3, 9)
        x = random.randint(2, 15)
        b = random.randint(5, 20)
    else:
        a = random.randint(5, 12)
        x = random.randint(-10, 20)
        b = random.randint(-20, 30)

    c = (a * x) + b
    ans = x
    wrongs = [x + 1, x - 1, x + 2, -x]
    return {"question": "Solve for x: {}x + {} = {}".format(a, b, c), "answer": str(ans), "choices": make_choices(ans, wrongs)}


def make_fractions(diff):
    # creates a fraction question
    if diff == "Easy":
        max_num = 5
        max_den = 8
        op = random.choice(["+", "-"])
    elif diff == "Medium":
        max_num = 8
        max_den = 12
        op = random.choice(["+", "-", "Ã—"])
    else:
        max_num = 12
        max_den = 15
        op = random.choice(["+", "-", "Ã—", "Ã·"])

    f1 = Fraction(random.randint(1, max_num), random.randint(2, max_den))
    f2 = Fraction(random.randint(1, max_num), random.randint(2, max_den))

    if op == "+":
        ans = f1 + f2
    elif op == "-":
        ans = f1 - f2
    elif op == "Ã—":
        ans = f1 * f2
    else:
        ans = f1 / f2

    wrongs = [ans + 1, ans - 1, ans + Fraction(1, 2), ans - Fraction(1, 2)]
    return {"question": "{} {} {} = ?".format(f1, op, f2), "answer": str(ans), "choices": make_choices(ans, wrongs)}


def make_differentiation(diff):
    # creates a basic differentiation question
    if diff == "Easy":
        coef = random.randint(1, 6)
        power = random.randint(2, 4)
    elif diff == "Medium":
        coef = random.randint(2, 10)
        power = random.randint(2, 6)
    else:
        coef = random.randint(3, 15)
        power = random.randint(3, 8)

    ans_coef = coef * power
    ans_power = power - 1
    correct = term_text(ans_coef, ans_power)
    wrongs = [term_text(ans_coef, power), term_text(coef, ans_power), term_text(ans_coef + 1, ans_power), term_text(ans_coef, ans_power + 1)]
    return {"question": "Differentiate: {}".format(term_text(coef, power)), "answer": correct, "choices": make_choices(correct, wrongs)}


def make_integration(diff):
    # creates a basic integration question where the answer has + C
    if diff == "Easy":
        ans_coef = random.randint(1, 5)
        ans_power = random.randint(2, 4)
    elif diff == "Medium":
        ans_coef = random.randint(2, 8)
        ans_power = random.randint(2, 6)
    else:
        ans_coef = random.randint(3, 12)
        ans_power = random.randint(3, 8)

    start_coef = ans_coef * ans_power
    start_power = ans_power - 1
    correct = term_text(ans_coef, ans_power) + " + C"
    wrongs = [term_text(start_coef, ans_power) + " + C", term_text(ans_coef, start_power) + " + C", term_text(ans_coef + 1, ans_power) + " + C", term_text(ans_coef, ans_power + 1) + " + C"]
    return {"question": "Integrate: {}".format(term_text(start_coef, start_power)), "answer": correct, "choices": make_choices(correct, wrongs)}


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
    set_win.geometry("450x350")
    set_win.resizable(False, False)
    set_win.configure(bg=CARD_COLOUR)

    # gets the current username for display
    if current_player != None:
        user = current_player.username
    else:
        user = "Unknown"

    tk.Label(set_win, text="Settings", font=("Helvetica", 20, "bold"), bg=CARD_COLOUR, fg=MAIN_PURPLE).pack(pady=(25, 10))
    tk.Label(set_win, text="Logged in as: " + user, font=("Helvetica", 12), bg=CARD_COLOUR, fg=TEXT_COLOUR).pack(pady=10)

    # music volume slider
    tk.Label(set_win, text="Background Music Volume", font=("Helvetica", 12, "bold"), bg=CARD_COLOUR, fg=TEXT_COLOUR).pack(pady=(20, 5))
    vol = tk.Scale(set_win, from_=0, to=100, orient="horizontal", length=250, bg=CARD_COLOUR, fg=TEXT_COLOUR, command=change_volume)
    vol.set(int(music_volume * 100))
    vol.pack()

    if music_loaded:
        music_text = "Music is playing from music.mp3"
    else:
        music_text = "No music loaded. Add music.mp3 to the same folder."

    tk.Label(set_win, text=music_text, font=("Helvetica", 10), bg=CARD_COLOUR, fg=TEXT_COLOUR).pack(pady=15)


def leaderboard():
    # opens the leaderboard window and shows cumulative xp rankings
    lb_win = tk.Toplevel(root)
    lb_win.title("Leaderboard")
    lb_win.geometry("720x650")
    lb_win.resizable(False, False)
    lb_win.configure(bg=CARD_COLOUR)

    tk.Label(lb_win, text="Leaderboard", font=("Helvetica", 22, "bold"), bg=CARD_COLOUR, fg=MAIN_PURPLE).pack(pady=(20, 5))
    tk.Label(lb_win, text="Rankings are based on total accumulated XP", font=("Helvetica", 11), bg=CARD_COLOUR, fg=TEXT_COLOUR).pack(pady=(0, 15))

    mode_frame = tk.Frame(lb_win, bg=CARD_COLOUR)
    mode_frame.pack(pady=5)

    board_box = tk.Text(lb_win, width=76, height=22, font=("Courier", 10), bg="#F5F5F5", fg=TEXT_COLOUR)
    board_box.pack(pady=15)

    def show_board(mode):
        # changes the leaderboard depending on the selected mode
        board_box.config(state="normal")
        board_box.delete("1.0", "end")

        stats = read_leads()
        rows = []

        for user in stats:
            make_user_stats(stats, user)

            if mode == "Overall":
                xp = 0
                answered = 0
                correct = 0

                for m in GAME_MODES:
                    xp += stats[user][m]["xp"]
                    answered += stats[user][m]["answered"]
                    correct += stats[user][m]["correct"]
            else:
                xp = stats[user][mode]["xp"]
                answered = stats[user][mode]["answered"]
                correct = stats[user][mode]["correct"]

            acc = get_accuracy(correct, answered)

            if xp > 0:
                rows.append([xp, user, answered, correct, acc])

        rows.sort(reverse=True)

        board_box.insert("end", "{} Leaderboard\n".format(mode))
        board_box.insert("end", "-" * 68 + "\n")
        board_box.insert("end", "{:<6}{:<18}{:<10}{:<12}{:<10}\n".format("Rank", "User", "XP", "Answered", "Accuracy"))
        board_box.insert("end", "-" * 68 + "\n")

        if len(rows) == 0:
            board_box.insert("end", "No scores have been saved for this mode yet.")
        else:
            rank = 1
            for row in rows:
                xp = row[0]
                user = row[1]
                answered = row[2]
                acc = row[4]
                board_box.insert("end", "{:<6}{:<18}{:<10}{:<12}{:<10}\n".format(rank, user, xp, answered, str(acc) + "%"))
                rank += 1

        board_box.config(state="disabled")

    all_modes = ["Overall"] + GAME_MODES

    for i in range(len(all_modes)):
        mode = all_modes[i]
        tk.Button(mode_frame, text=mode, width=16, height=2, bg=MAIN_PURPLE, fg="white", relief="flat", command=lambda m=mode: show_board(m)).grid(row=i // 3, column=i % 3, padx=5, pady=5)

    show_board("Overall")


def profile_screen():
    # opens the profile window and shows account data
    prof_win = tk.Toplevel(root)
    prof_win.title("Profile")
    prof_win.geometry("720x650")
    prof_win.resizable(False, False)
    prof_win.configure(bg=CARD_COLOUR)

    if current_player != None:
        user = current_player.username
    else:
        user = "Unknown"

    stats = read_leads()
    make_user_stats(stats, user)

    total_xp = 0
    total_answered = 0
    total_correct = 0
    total_time = 0

    for mode in GAME_MODES:
        total_xp += stats[user][mode]["xp"]
        total_answered += stats[user][mode]["answered"]
        total_correct += stats[user][mode]["correct"]
        total_time += stats[user][mode]["time"]

    level = get_level(total_xp)
    accuracy = get_accuracy(total_correct, total_answered)
    next_level_xp = XP_PER_LEVEL - (total_xp % XP_PER_LEVEL)

    tk.Label(prof_win, text="Profile", font=("Helvetica", 24, "bold"), bg=CARD_COLOUR, fg=MAIN_PURPLE).pack(pady=(20, 5))
    tk.Label(prof_win, text="Account: " + user, font=("Helvetica", 14, "bold"), bg=CARD_COLOUR, fg=TEXT_COLOUR).pack(pady=(0, 15))

    top_stats = tk.Frame(prof_win, bg=CARD_COLOUR)
    top_stats.pack(pady=10)

    tk.Label(top_stats, text="Level\n" + str(level), font=("Helvetica", 14, "bold"), bg=LIGHT_GREY, fg=TEXT_COLOUR, width=14, height=3).grid(row=0, column=0, padx=8)
    tk.Label(top_stats, text="Total XP\n" + str(total_xp), font=("Helvetica", 14, "bold"), bg=LIGHT_GREY, fg=TEXT_COLOUR, width=14, height=3).grid(row=0, column=1, padx=8)
    tk.Label(top_stats, text="Accuracy\n" + str(accuracy) + "%", font=("Helvetica", 14, "bold"), bg=LIGHT_GREY, fg=TEXT_COLOUR, width=14, height=3).grid(row=0, column=2, padx=8)
    tk.Label(top_stats, text="Questions\n" + str(total_answered), font=("Helvetica", 14, "bold"), bg=LIGHT_GREY, fg=TEXT_COLOUR, width=14, height=3).grid(row=0, column=3, padx=8)

    tk.Label(prof_win, text="Playtime: " + time_text(total_time), font=("Helvetica", 12), bg=CARD_COLOUR, fg=TEXT_COLOUR).pack(pady=5)
    tk.Label(prof_win, text="XP until next level: " + str(next_level_xp), font=("Helvetica", 12), bg=CARD_COLOUR, fg=TEXT_COLOUR).pack(pady=5)

    data_box = tk.Text(prof_win, width=78, height=20, font=("Courier", 10), bg="#F5F5F5", fg=TEXT_COLOUR)
    data_box.pack(pady=20)

    data_box.insert("end", "Mode Data\n")
    data_box.insert("end", "-" * 70 + "\n")
    data_box.insert("end", "{:<18}{:<10}{:<12}{:<10}{:<12}\n".format("Mode", "XP", "Answered", "Correct", "Accuracy"))
    data_box.insert("end", "-" * 70 + "\n")

    for mode in GAME_MODES:
        xp = stats[user][mode]["xp"]
        answered = stats[user][mode]["answered"]
        correct = stats[user][mode]["correct"]
        acc = get_accuracy(correct, answered)
        data_box.insert("end", "{:<18}{:<10}{:<12}{:<10}{:<12}\n".format(mode, xp, answered, correct, str(acc) + "%"))

    data_box.config(state="disabled")
    tk.Button(prof_win, text="Close", width=14, height=2, bg=MAIN_PURPLE, fg="white", relief="flat", command=prof_win.destroy).pack(pady=5)


def start_quiz(mode, diff):
    # starts the kahoot style quiz screen
    quiz_win = tk.Toplevel(root)
    quiz_win.title(mode + " Quiz")
    quiz_win.geometry("{}x{}".format(ww, wh))
    quiz_win.resizable(False, False)
    quiz_win.configure(bg=BG_COLOUR)

    # creates 10 random questions for the chosen mode and difficulty
    questions = []
    for i in range(10):
        questions.append(make_question(mode, diff))

    # stores quiz progress while the quiz is running
    state = {"qnum": 0, "correct": 0, "answered": 0, "xp": 0, "time_left": DIFF_TIME[diff], "timer_id": None, "start_time": time.time(), "locked": False}

    qframe = tk.Frame(quiz_win, bg=CARD_COLOUR, relief="flat", width=760, height=720)
    qframe.place(relx=0.5, rely=0.5, anchor="center")
    qframe.pack_propagate(False)

    top_line = tk.Label(qframe, text=mode + " - " + diff, font=("Helvetica", 20, "bold"), bg=CARD_COLOUR, fg=MAIN_PURPLE)
    top_line.pack(pady=(25, 5))

    score_line = tk.Label(qframe, text="Question 1/10 XP: 0", font=("Helvetica", 12, "bold"), bg=CARD_COLOUR, fg=TEXT_COLOUR)
    score_line.pack(pady=5)

    timer_line = tk.Label(qframe, text="Time: " + str(DIFF_TIME[diff]), font=("Helvetica", 18, "bold"), bg=CARD_COLOUR, fg=RED)
    timer_line.pack(pady=10)

    question_label = tk.Label(qframe, text="", font=("Helvetica", 22, "bold"), bg=CARD_COLOUR, fg=TEXT_COLOUR, wraplength=650, height=3)
    question_label.pack(pady=25)

    ans_frame = tk.Frame(qframe, bg=CARD_COLOUR)
    ans_frame.pack(pady=10)

    feedback_label = tk.Label(qframe, text="", font=("Helvetica", 18, "bold"), bg=CARD_COLOUR, fg=TEXT_COLOUR)
    feedback_label.pack(pady=20)

    answer_buttons = []
    btn_colours = [GREEN, BLUE, ORANGE, RED]

    def stop_timer():
        # stops the countdown if it is running
        if state["timer_id"] != None:
            try:
                quiz_win.after_cancel(state["timer_id"])
            except:
                pass
            state["timer_id"] = None

    def close_quiz():
        # closes the quiz window safely
        stop_timer()
        quiz_win.destroy()

    def timer_tick():
        # counts down the time for each question
        if state["locked"]:
            return

        timer_line.config(text="Time: " + str(state["time_left"]))

        if state["time_left"] <= 0:
            check_answer(None)
        else:
            state["time_left"] -= 1
            state["timer_id"] = quiz_win.after(1000, timer_tick)

    def flash(colour, times):
        # small colour flash animation for correct and incorrect answers
        if times <= 0:
            qframe.config(bg=CARD_COLOUR)
            feedback_label.config(bg=CARD_COLOUR)
            return

        qframe.config(bg=colour)
        feedback_label.config(bg=colour)
        quiz_win.after(120, lambda: flash(CARD_COLOUR, times - 1))

    def end_quiz():
        # saves the final score and shows the end screen
        stop_timer()

        play_seconds = int(time.time() - state["start_time"])
        save_quiz_result(mode, state["xp"], state["answered"], state["correct"], play_seconds)

        for btn in answer_buttons:
            btn.grid_forget()

        question_label.config(text="Quiz Finished!")
        timer_line.config(text="")
        score_line.config(text="Final Result")
        feedback_label.config(text="Correct: {}/10 XP gained: {} Time: {}".format(state["correct"], state["xp"], time_text(play_seconds)), fg=TEXT_COLOUR)

        tk.Button(qframe, text="Back to Modes", width=18, height=2, bg=MAIN_PURPLE, fg="white", relief="flat", command=lambda: [quiz_win.destroy(), mode_screen()]).pack(pady=10)
        tk.Button(qframe, text="Leaderboard", width=18, height=2, bg=BLUE, fg="white", relief="flat", command=leaderboard).pack(pady=5)
        tk.Button(qframe, text="Profile", width=18, height=2, bg=ORANGE, fg="white", relief="flat", command=profile_screen).pack(pady=5)

    def next_question():
        # moves to the next question or finishes the quiz
        state["qnum"] += 1

        if state["qnum"] >= len(questions):
            end_quiz()
        else:
            show_question()

    def check_answer(choice):
        # checks if the selected multiple choice answer is correct
        if state["locked"]:
            return

        state["locked"] = True
        stop_timer()
        q = questions[state["qnum"]]
        state["answered"] += 1

        for btn in answer_buttons:
            btn.config(state="disabled")

        if choice == q["answer"]:
            state["correct"] += 1
            state["xp"] += DIFF_XP[diff]
            feedback_label.config(text="Correct! +{} XP".format(DIFF_XP[diff]), fg=GREEN)
            flash(GREEN, 4)
        elif choice == None:
            feedback_label.config(text="Time up! Correct answer: " + q["answer"], fg=RED)
            flash(RED, 4)
        else:
            feedback_label.config(text="Incorrect! Correct answer: " + q["answer"], fg=RED)
            flash(RED, 4)

        score_line.config(text="Question {}/10 XP: {}".format(state["qnum"] + 1, state["xp"]))
        quiz_win.after(1400, next_question)

    def show_question():
        # displays the current question and answers
        state["locked"] = False
        state["time_left"] = DIFF_TIME[diff]
        q = questions[state["qnum"]]

        score_line.config(text="Question {}/10 XP: {}".format(state["qnum"] + 1, state["xp"]))
        feedback_label.config(text="", bg=CARD_COLOUR)
        qframe.config(bg=CARD_COLOUR)
        question_label.config(text=q["question"])

        for i in range(4):
            answer = q["choices"][i]
            answer_buttons[i].config(text=answer, bg=btn_colours[i], state="normal", command=lambda a=answer: check_answer(a))

        timer_tick()

    for i in range(4):
        btn = tk.Button(ans_frame, text="", width=28, height=4, bg=btn_colours[i], fg="white", relief="flat", font=("Helvetica", 13, "bold"))
        btn.grid(row=i // 2, column=i % 2, padx=15, pady=15)
        answer_buttons.append(btn)

    tk.Button(qframe, text="Quit Quiz", width=14, height=2, bg=RED, fg="white", relief="flat", command=close_quiz).pack(pady=5)
    quiz_win.protocol("WM_DELETE_WINDOW", close_quiz)
    show_question()


def diff_screen(mode):
    # opens the difficulty selection screen after a mode is chosen
    difwin = tk.Toplevel(root)
    difwin.title("Select Difficulty")
    difwin.geometry("{}x{}".format(ww, wh))
    difwin.resizable(False, False)
    difwin.configure(bg=BG_COLOUR)

    # central white frame
    df = tk.Frame(difwin, bg=CARD_COLOUR, relief="flat", width=700, height=520)
    df.place(relx=0.5, rely=0.5, anchor="center")
    df.pack_propagate(False)

    tk.Label(df, text=mode + " Difficulty", font=("Helvetica", 22, "bold"), bg=CARD_COLOUR, fg=MAIN_PURPLE, width=30).pack(pady=(30, 10))
    tk.Label(df, text="Choose how hard you want the questions to be", font=("Helvetica", 11), bg=CARD_COLOUR, fg=TEXT_COLOUR).pack(pady=(0, 25))

    # frame that holds the three difficulty buttons
    cards = tk.Frame(df, bg=CARD_COLOUR)
    cards.pack(pady=10)

    # difficulty buttons
    tk.Button(cards, text="Easy", width=14, height=9, bg=GREEN, fg="white", relief="flat", font=("Helvetica", 13, "bold"), command=lambda: [difwin.destroy(), start_quiz(mode, "Easy")]).grid(row=0, column=0, padx=25)
    tk.Button(cards, text="Medium", width=14, height=9, bg=YELLOW, fg="black", relief="flat", font=("Helvetica", 13, "bold"), command=lambda: [difwin.destroy(), start_quiz(mode, "Medium")]).grid(row=0, column=1, padx=25)
    tk.Button(cards, text="Hard", width=14, height=9, bg=RED, fg="white", relief="flat", font=("Helvetica", 13, "bold"), command=lambda: [difwin.destroy(), start_quiz(mode, "Hard")]).grid(row=0, column=2, padx=25)

    def back_to_modes():
        # goes back to the mode screen
        difwin.destroy()
        mode_screen()

    tk.Button(df, text="Back", width=14, height=2, bg=MAIN_PURPLE, fg="white", relief="flat", command=back_to_modes).pack(pady=30)


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


# -------------------------------------------------------------------
# -------------------------------------------------------------------


def mode_screen():
    # modern two-row mode grid
    win = tk.Toplevel(root)
    win.title("Kalc | Select Mode")
    win.geometry("1000x760")
    win.resizable(False, False)
    win.configure(bg=PALE_PURPLE)
    page_header(win, "Choose a mode", "Which maths skill would you like to practise?",
                win.destroy)

    grid = tk.Frame(win, bg=PALE_PURPLE)
    grid.pack(expand=True, padx=55, pady=35)
    colours = [MAIN_PURPLE, GREEN, RED, BLUE, ORANGE, "#D6A900",
               "#7D4CC2", "#238B8B"]
    symbols = ["x", "+", "âˆ’", "Ã·", "Ã—", "Â½", "d/dx", "âˆ«"]

    def choose(mode):
        win.destroy()
        diff_screen(mode)

    for i, mode in enumerate(GAME_MODES):
        card = tk.Frame(grid, bg="white", highlightbackground=CARD_BORDER,
                        highlightthickness=1, width=205, height=205)
        card.grid(row=i // 4, column=i % 4, padx=10, pady=10)
        card.pack_propagate(False)
        tk.Label(card, text=symbols[i], font=("Segoe UI", 36, "bold"),
                 bg="white", fg=colours[i]).pack(pady=(25, 5))
        tk.Label(card, text=mode, font=SUBHEADING_FONT, bg="white",
                 fg=TEXT_COLOUR).pack()
        modern_button(card, "Choose", lambda m=mode: choose(m),
                      colours[i], 13, 1).pack(pady=18)


def menu_screen():
    # modern home dashboard
    root.withdraw()
    win = tk.Toplevel(root)
    win.title("Kalc | Main Menu")
    win.geometry("1000x760")
    win.resizable(False, False)
    win.configure(bg=PALE_PURPLE)
    win.protocol("WM_DELETE_WINDOW", root.destroy)

    user = current_player.username if current_player else "Unknown"
    header = page_header(win, "KALC", "Learn, practise and improve")
    modern_button(header, user, profile_screen, MAIN_PURPLE, 14, 1).pack(
        side="right", padx=30, pady=28)

    hero = tk.Frame(win, bg=DEEP_PURPLE, height=205)
    hero.pack(fill="x", padx=48, pady=(35, 22))
    hero.pack_propagate(False)
    tk.Label(hero, text="Ready for your next challenge?", font=TITLE_FONT,
             bg=DEEP_PURPLE, fg="white").pack(anchor="w", padx=38, pady=(35, 5))
    tk.Label(hero, text="Choose from eight maths modes and build your XP.",
             font=BODY_FONT, bg=DEEP_PURPLE, fg="#DCD1F4").pack(
                 anchor="w", padx=38)
    modern_button(hero, "Play now  â†’", mode_screen, GREEN, 16, 2).pack(
        anchor="w", padx=38, pady=22)

    actions = tk.Frame(win, bg=PALE_PURPLE)
    actions.pack(fill="both", expand=True, padx=40)
    options = [("Leaderboard", "Compare cumulative XP rankings", BLUE, leaderboard),
               ("Profile", "View accuracy, playtime and progress", MAIN_PURPLE, profile_screen),
               ("Settings", "Adjust your background music", ORANGE, settings),
               ("Quit", "Close Kalc safely", RED, root.destroy)]
    for i, item in enumerate(options):
        title, desc, colour, command = item
        card = tk.Frame(actions, bg="white", highlightbackground=CARD_BORDER,
                        highlightthickness=1, width=215, height=210)
        card.grid(row=0, column=i, padx=8, pady=8)
        card.pack_propagate(False)
        tk.Label(card, text=title, font=HEADING_FONT, bg="white",
                 fg=colour).pack(pady=(27, 8))
        tk.Label(card, text=desc, font=SMALL_FONT, bg="white",
                 fg=MUTED_TEXT, wraplength=170).pack()
        modern_button(card, "Open", command, colour, 13, 1).pack(pady=24)


# checks the login and leaderboard files before the GUI starts
file_check()

# creates the main login window
root = tk.Tk()
root.title(APP_TITLE)
root.geometry("{}x{}".format(ww, wh))
root.resizable(False, False)
root.configure(bg=DEEP_PURPLE)

# loads the logo and starts the music after the root window exists
load_logo()
start_music()

# main white login card
main_frame = tk.Frame(root, bg=CARD_COLOUR, relief="flat", width=620, height=610,
                      highlightbackground=CARD_BORDER, highlightthickness=1)
main_frame.place(relx=0.5, rely=0.5, anchor="center")
main_frame.pack_propagate(False)

# title area
tk.Label(main_frame, text="KALC", font=("Segoe UI", 42, "bold"),
         bg=CARD_COLOUR, fg=HEADER_PURPLE).pack(pady=(45, 2))
tk.Label(main_frame, text="Build confidence. Earn XP. Master maths.",
         font=BODY_FONT, bg=CARD_COLOUR, fg=MUTED_TEXT).pack(pady=(0, 30))

# form area for username and password
form = tk.Frame(main_frame, bg=CARD_COLOUR)
form.pack(pady=10)

tk.Label(form, text="Username", font=SUBHEADING_FONT, bg=CARD_COLOUR,
         fg=TEXT_COLOUR).grid(row=0, column=0, sticky="w", pady=(4, 6))
username_entry = tk.Entry(form, width=35, font=("Segoe UI", 13), relief="flat",
                          bg=ENTRY_COLOUR, fg=TEXT_COLOUR)
username_entry.grid(row=1, column=0, ipady=10, pady=(0, 18))

tk.Label(form, text="Password", font=SUBHEADING_FONT, bg=CARD_COLOUR,
         fg=TEXT_COLOUR).grid(row=2, column=0, sticky="w", pady=(4, 6))
password_entry = tk.Entry(form, width=35, font=("Segoe UI", 13), show="*",
                          relief="flat", bg=ENTRY_COLOUR, fg=TEXT_COLOUR)
password_entry.grid(row=3, column=0, ipady=10, pady=(0, 8))

# login and quit buttons
main_btns = tk.Frame(main_frame, bg=CARD_COLOUR)
main_btns.pack(pady=18)

modern_button(main_btns, "Log in", login, GREEN, 18, 2).grid(row=0, column=0, padx=7)
modern_button(main_btns, "Quit", close_game, RED, 18, 2).grid(row=0, column=1, padx=7)

# bottom buttons for extra login options
bottom = tk.Frame(main_frame, bg=CARD_COLOUR)
bottom.pack(side="bottom", pady=35)

modern_button(bottom, "Create account", acc_screen, MAIN_PURPLE, 18, 1).grid(
    row=0, column=0, padx=7)
modern_button(bottom, "Forgot password", forgot_screen, BLUE, 18, 1).grid(
    row=0, column=1, padx=7)

# lets the user press Enter to login
root.bind("<Return>", lambda event: login())

# starts the program
root.mainloop()
