from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
next_word = {}
words = {}

try:
    data = pandas.read_csv("data/known_words.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    words = data.to_dict(orient="records")
else:
    words = data.to_dict(orient="records")


def next_data():
    global next_word, timer
    window.after_cancel(timer)
    next_word = random.choice(words)
    canvas.itemconfig(card_word, text=next_word["French"], fill="black")
    canvas.itemconfig(language_title, text="French", fill="black")
    canvas.itemconfig(background_image, image=img)
    timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_word, text=next_word["English"], fill="white")
    canvas.itemconfig(language_title, text="English", fill="white")
    canvas.itemconfig(background_image, image=back_background_image)


def known_words():
    words.remove(next_word)
    data = pandas.DataFrame(words)
    data.to_csv("data/known_words.csv", index=False)
    next_data()


window = Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
img = PhotoImage(file="images/card_front.png")
back_background_image = PhotoImage(file="images/card_back.png")
background_image = canvas.create_image(400, 263, image=img)
language_title = canvas.create_text(400, 150, text="Title", font=("Arial", 24, "italic"))
card_word = canvas.create_text(400, 250, text="Word", font=("Arial", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

left_img = PhotoImage(file="images/wrong.png")
left_button = Button(image=left_img, highlightthickness=0, command=next_data)
left_button.grid(row=1, column=0)

right_img = PhotoImage(file="images/right.png")
right_button = Button(image=right_img, highlightthickness=0, command=known_words)
right_button.grid(row=1, column=1)

next_data()

window.mainloop()
