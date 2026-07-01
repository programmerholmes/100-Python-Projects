import os
import sys
import time
import random

# Helps Tkinter find Tcl/Tk on your Python installation.
# This avoids hardcoding your username/path.
base_path = sys.base_prefix

tcl_path = os.path.join(base_path, "tcl", "tcl8.6")
tk_path = os.path.join(base_path, "tcl", "tk8.6")

if os.path.exists(tcl_path):
    os.environ["TCL_LIBRARY"] = tcl_path

if os.path.exists(tk_path):
    os.environ["TK_LIBRARY"] = tk_path

import tkinter as tk


# -----------------------------
# Sample texts for the typing test
# -----------------------------
SAMPLE_TEXTS = [
    "The quick brown fox jumps over the lazy dog.",
    "Python is a powerful programming language that is easy to learn and fun to use.",
    "Typing quickly and accurately takes practice, patience, and concentration.",
    "A good programmer solves problems by breaking them into smaller steps.",
    "Desktop apps can be built in Python using the Tkinter library.",
    "The average typing speed is around forty words per minute.",
    "With enough practice, many people can type close to one hundred words per minute."
]


# -----------------------------
# Global variables
# -----------------------------
start_time = None
timer_running = False
current_sentence = ""
high_score = 0


# -----------------------------
# Functions
# -----------------------------
def start_timer(event=None):
    """
    Starts the timer when the user begins typing.
    """
    global start_time, timer_running

    # Ignore keys like Shift, Ctrl, Alt, etc.
    ignored_keys = {
        "Shift_L", "Shift_R",
        "Control_L", "Control_R",
        "Alt_L", "Alt_R",
        "Caps_Lock", "Tab"
    }

    if event is not None and event.keysym in ignored_keys:
        return

    if start_time is None:
        start_time = time.time()
        timer_running = True
        update_timer()


def update_timer():
    """
    Updates the timer label every second while the test is running.
    """
    if timer_running and start_time is not None:
        elapsed = time.time() - start_time
        timer_label.config(text=f"Time: {elapsed:.1f} seconds")
        window.after(1000, update_timer)


def calculate_accuracy(typed_text, target_text):
    """
    Calculates character-by-character accuracy.
    """
    if not typed_text:
        return 0

    correct_characters = 0

    for typed_char, target_char in zip(typed_text, target_text):
        if typed_char == target_char:
            correct_characters += 1

    total_characters = max(len(typed_text), len(target_text))

    return (correct_characters / total_characters) * 100


def calculate_correct_words(typed_text, target_text):
    """
    Counts how many words are correct and in the correct position.
    """
    typed_words = typed_text.split()
    target_words = target_text.split()

    correct_words = 0

    for typed_word, target_word in zip(typed_words, target_words):
        if typed_word == target_word:
            correct_words += 1

    return correct_words


def finish_test():
    """
    Stops the test and calculates the user's typing speed.
    """
    global timer_running, high_score

    if start_time is None:
        result_label.config(
            text="Start typing first, then click Finished.",
            fg="red"
        )
        return

    timer_running = False

    end_time = time.time()
    time_taken = end_time - start_time

    typed_text = user_input.get("1.0", "end-1c").strip()

    word_count = len(typed_text.split())
    correct_words = calculate_correct_words(typed_text, current_sentence)
    accuracy = calculate_accuracy(typed_text, current_sentence)

    # Avoid division by zero
    time_taken = max(time_taken, 1)

    # Gross WPM: total words typed per minute
    wpm = (word_count / time_taken) * 60

    # Correct WPM: only correctly typed words per minute
    correct_wpm = (correct_words / time_taken) * 60

    if wpm > high_score:
        high_score = int(wpm)

    high_score_label.config(text=f"High Score: {high_score} WPM")

    if wpm < 40:
        message = "Below average. Keep practicing!"
    elif wpm < 70:
        message = "Good job! You are above average."
    elif wpm < 100:
        message = "Great typing speed!"
    else:
        message = "Excellent! You are extremely fast."

    result_label.config(
        text=(
            f"Speed: {wpm:.1f} WPM\n"
            f"Correct Speed: {correct_wpm:.1f} WPM\n"
            f"Words Typed: {word_count}\n"
            f"Correct Words: {correct_words}\n"
            f"Accuracy: {accuracy:.1f}%\n"
            f"{message}"
        ),
        fg="black"
    )

    user_input.config(state="disabled")
    finish_button.config(state="disabled")


def reset_test():
    """
    Starts a new typing test with a new sentence.
    """
    global start_time, timer_running, current_sentence

    start_time = None
    timer_running = False

    current_sentence = random.choice(SAMPLE_TEXTS)
    sentence_var.set(current_sentence)

    user_input.config(state="normal")
    user_input.delete("1.0", "end")
    user_input.focus_set()

    timer_label.config(text="Time: 0.0 seconds")
    result_label.config(text="", fg="black")
    finish_button.config(state="normal")


# -----------------------------
# GUI setup
# -----------------------------
window = tk.Tk()
window.title("Typing Speed Test")
window.geometry("700x600")
window.config(padx=20, pady=20)

# Title
title_label = tk.Label(
    window,
    text="Test Your Typing Speed!",
    font=("Helvetica", 22, "bold")
)
title_label.pack(pady=10)

# Instructions
instruction_label = tk.Label(
    window,
    text="Type the sentence below as quickly and accurately as you can.",
    font=("Helvetica", 12)
)
instruction_label.pack(pady=5)

# Target sentence
sentence_var = tk.StringVar()

sentence_label = tk.Label(
    window,
    textvariable=sentence_var,
    font=("Helvetica", 14),
    wraplength=620,
    justify="center",
    bg="#f0f0f0",
    padx=15,
    pady=15
)
sentence_label.pack(pady=20, fill="x")

# Input area
user_input = tk.Text(
    window,
    width=70,
    height=7,
    font=("Helvetica", 13),
    wrap="word"
)
user_input.pack(pady=10)

# Start timer when user types
user_input.bind("<KeyPress>", start_timer)

# Timer label
timer_label = tk.Label(
    window,
    text="Time: 0.0 seconds",
    font=("Helvetica", 12, "bold")
)
timer_label.pack(pady=5)

# Buttons
button_frame = tk.Frame(window)
button_frame.pack(pady=10)

finish_button = tk.Button(
    button_frame,
    text="Finished!",
    font=("Helvetica", 12),
    width=12,
    command=finish_test
)
finish_button.grid(row=0, column=0, padx=10)

new_test_button = tk.Button(
    button_frame,
    text="New Text",
    font=("Helvetica", 12),
    width=12,
    command=reset_test
)
new_test_button.grid(row=0, column=1, padx=10)

# Result label
result_label = tk.Label(
    window,
    text="",
    font=("Helvetica", 13),
    justify="center"
)
result_label.pack(pady=20)

# High score label
high_score_label = tk.Label(
    window,
    text="High Score: 0 WPM",
    font=("Helvetica", 12, "bold")
)
high_score_label.pack(pady=5)

# Start first test
reset_test()

# Keep the window open
window.mainloop()