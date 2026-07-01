import turtle
import pandas
FONT = ("Courier", 24, "normal")
screen = turtle.Screen()
screen.title("U.S. States Game")

image = "Blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)
#turtle.screensize()
screen.screensize(10, 5000)
print(turtle.screensize())
screen.screensize(10, 5000)
turtle.resizemode("auto")


country = pandas.read_csv("50_states.csv")
print(country)
print(country["state"])
country_list = country["state"].to_list()
print(country_list)
print(type(country_list))

guessed_states = []
count = 0
name = turtle.Turtle()
not_end_of_game = True
while not_end_of_game:
    answer_state = screen.textinput(title=f"{count}/50 Guess the State", prompt="What's another state's name?").title()
    if answer_state in country_list:
        print(answer_state)
        data = country[country["state"] == answer_state]
        print(data)
        data_x = data["x"].to_list()
        data_y = data["y"].to_list()
        xcor = data_x[0]
        ycor = data_y[0]
        print(xcor)
        print(ycor)

        name.penup()
        name.hideturtle()
        name.goto(xcor, ycor)
        name.write(answer_state)

        if answer_state not in guessed_states:
            guessed_states.append(answer_state)
            count = count + 1

            if count == 50:
                print("YOU WIN!!")
                turtle.write("YOU GOT THEM ALL", align="center", font=FONT)
                not_end_of_game = False

    elif answer_state == "Exit":
        not_end_of_game = False



#states_to_learn.csv
missing_state = []
for state in country_list:
    if state not in guessed_states:
        missing_state.append(state)
print(missing_state)
data = pandas.DataFrame(missing_state)
data.to_csv("states_to_learn.csv")

# OR
# missing_state = [state for state in country_list if state not in guessed_states]


def get_mouse_click_coor(x, y):
    print(x, y)


turtle.onscreenclick(get_mouse_click_coor)

turtle.mainloop()
