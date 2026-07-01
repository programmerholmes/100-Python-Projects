import tkinter


window = tkinter.Tk()
window.title("First GUI USING GRID")
window.minsize(width=500, height=300)
window.config(padx=20, pady=20)

# Label
my_label = tkinter.Label(text="I am a label", font=("Arial", 24, "bold"))

# updating
my_label["text"] = "New text"
# OR
my_label.config(text="New text")


# my_label.pack(side="left")
my_label.grid(column=0, row=0)


# Button

def button_clicked():
    print("I got clicked")
    my_label["text"] = my_input.get()


my_button = tkinter.Button(text="Click me!", command=button_clicked)
my_button.grid(column=1, row=1)

# New Button
new_button = tkinter.Button(text="New Button")
new_button.grid(column=2, row=0)

# Entry
my_input = tkinter.Entry(width=10)
my_input.grid(column=3, row=2)
my_input.get()

window.mainloop()