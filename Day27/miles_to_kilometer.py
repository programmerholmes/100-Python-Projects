from tkinter import *

window = Tk()
window.title("Miles to Kilometer Converter")
window.config(padx=20, pady=20)


def miles_to_kilometer():
    temp_miles = float(miles.get())
    km = round(temp_miles * 1.609)
    number.config(text=f"{km}")
    #number["text"] = (f"{km}")


miles = Entry(width=10)
miles.grid(column=1, row=0)

my_miles = Label(text="Miles")
my_miles.grid(column=2, row=0)

my_label = Label(text="is equal to ")
my_label.grid(column=0, row=1)

number = Label(text=0)
number.grid(column=1, row=1)

km = Label(text="Km")
km.grid(column=2, row=1)

calculate = Button(text="Calculate", command=miles_to_kilometer)
calculate.grid(column=1, row=2)

window.mainloop()
