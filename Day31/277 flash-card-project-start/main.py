from tkinter import *
import pandas
import random
BACKGROUND_COLOR = "#B1DDC6"
current = {}
listed = {}
try:
    data = pandas.read_csv("data/words_to_learn")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    listed = original_data.to_dict(orient="records")
else:
    listed = data.to_dict(orient="records")


window = Tk()
window.title("Flashy")
window.config(padx=20, pady=20, bg=BACKGROUND_COLOR)



def next_card():
    global current, flip_timer
    window.after_cancel(flip_timer)
    current = random.choice(listed)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current["French"], fill="black")
    canvas.itemconfig(canvas_change_image, image=card_front)
    flip_timer = window.after(3000, func=image_update)


def image_update():
    canvas.itemconfig(canvas_change_image, image=card_back)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current["English"], fill="white")


def is_known():
    listed.remove(current)
    data = pandas.DataFrame(listed)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


flip_timer = window.after(3000, func=image_update)


canvas = Canvas(width=800, height=530, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
canvas_change_image = canvas.create_image(400, 265, image=card_front)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 265, text="", font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)


wrong_image = PhotoImage(file="images/wrong.png")
cross = Button(image=wrong_image, highlightthickness=0, command=next_card)
cross.grid(column=0, row=1)

right_image = PhotoImage(file="images/right.png")
tick = Button(image=right_image, highlightthickness=0, command=is_known)
tick.grid(column=1, row=1)

next_card()

window.mainloop()
