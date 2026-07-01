import tkinter


window = tkinter.Tk()
window.title("First GUI")
window.minsize(width=500, height=300)
window.config(padx=20, pady=20)

# Label
my_label = tkinter.Label(text="I am a label", font=("Arial", 24, "bold"))

# updating
my_label["text"] = "New text"
# OR
my_label.config(text="New text")
my_label.config(padx=5, pady=10)

# my_label.pack(side="left")
my_label.pack() # expand=True


# Button

def button_clicked():
    print("I got clicked")
    my_label["text"] = my_input.get()


my_button = tkinter.Button(text="Click me!", command=button_clicked)
my_button.pack()


# Entry
my_input = tkinter.Entry(width=10)
my_input.place(x=0, y=50)
my_input.get()

window.mainloop()
