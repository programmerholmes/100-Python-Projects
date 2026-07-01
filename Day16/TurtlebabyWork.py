
from turtle import Turtle, Screen
import colorsys
import turtle



# timmy = Turtle()
# timmy.shape("turtle")
# timmy.color("DarkSeaGreen4")
# timmy.forward(100)
#
#
# my_screen = Screen()
# my_screen.exitonclick()
# print(my_screen)
#
#
# t = turtle.Turtle()
# s = turtle.Screen()
# s.bgcolor("black")
# t.speed(0)
# n = 36
# h = 0
# for i in range(460):
#     c = colorsys.hsv_to_rgb(h,1,0.9)
#     h += 1/n
#     t.color(c)
#     t.left(145)
#     for j in range(5):
#         t.forward(300)
#         t.left(150)
#
#
# import turtle
# wn = turtle.Screen()
# wn.setup(width=400, height=400)
# red = turtle.Turtle() # Assigning "Red" as name of the turtle
#
# def curve(): # Method to draw curve
#     for i in range(200): # To draw the curve step by step
#         red.right(1)
#         red.forward(1)
#
# def heart():  # Method to draw full Heart
#     red.fillcolor('red')
#     red.begin_fill()
#     red.left(140)
#     red.forward(113)
#     curve() # Left Curve
#     red.left(120)
#     curve() # Right Curve
#     red.forward(112)
#     red.end_fill()
#
# heart()
# red.ht() # Hiding Turtle
# turtle.write('Name1 + Name2 = Perfection ❤️', font=("Bradley Hand ITC", 30, "bold"))
# turtle.done()
# red.hideturtle()
#
# from turtle import *
# import turtle
# wn = turtle.Screen()
# wn.setup(width=1000, height=800)
#
# def my_goto(x, y):
#     penup()
#     goto(x, y)
#     pendown()
#
#
# def eyes():
#     fillcolor("#ffffff")
#     begin_fill()
#
#     tracer(False)
#     a = 2.5
#     for i in range(120):
#         if 0 <= i < 30 or 60 <= i < 90:
#             a -= 0.05
#             lt(3)
#             fd(a)
#         else:
#             a += 0.05
#             lt(3)
#             fd(a)
#     tracer(True)
#     end_fill()
#
#
#
# def beard():
#     my_goto(-32, 135)
#     seth(165)
#     fd(60)
#
#     my_goto(-32, 125)
#     seth(180)
#     fd(60)
#
#     my_goto(-32, 115)
#     seth(193)
#     fd(60)
#
#     my_goto(37, 135)
#     seth(15)
#     fd(60)
#
#     my_goto(37, 125)
#     seth(0)
#     fd(60)
#
#     my_goto(37, 115)
#     seth(-13)
#     fd(60)
#
#
# def mouth():
#     my_goto(5, 148)
#     seth(270)
#     fd(100)
#     seth(0)
#     circle(120, 50)
#     seth(230)
#     circle(-120, 100)
#
#
# def scarf():
#     fillcolor('#e70010')
#     begin_fill()
#     seth(0)
#     fd(200)
#     circle(-5, 90)
#     fd(10)
#     circle(-5, 90)
#     fd(207)
#     circle(-5, 90)
#     fd(10)
#     circle(-5, 90)
#     end_fill()
#
#
# def nose():
#     my_goto(-10, 158)
#     seth(315)
#     fillcolor('#e70010')
#     begin_fill()
#     circle(20)
#     end_fill()
#
#
# def black_eyes():
#     seth(0)
#     my_goto(-20, 195)
#     fillcolor('#000000')
#     begin_fill()
#     circle(13)
#     end_fill()
#
#     pensize(6)
#     my_goto(20, 205)
#     seth(75)
#     circle(-10, 150)
#     pensize(3)
#
#     my_goto(-17, 200)
#     seth(0)
#     fillcolor('#ffffff')
#     begin_fill()
#     circle(5)
#     end_fill()
#     my_goto(0, 0)
#
#
#
#
# def face():
#
#     fd(183)
#     lt(45)
#     fillcolor('#ffffff')
#     begin_fill()
#     circle(120, 100)
#     seth(180)
#     # print(pos())
#     fd(121)
#     pendown()
#     seth(215)
#     circle(120, 100)
#     end_fill()
#     my_goto(63.56,218.24)
#     seth(90)
#     eyes()
#     seth(180)
#     penup()
#     fd(60)
#     pendown()
#     seth(90)
#     eyes()
#     penup()
#     seth(180)
#     fd(64)
#
#
# def head():
#     penup()
#     circle(150, 40)
#     pendown()
#     fillcolor('#00a0de')
#     begin_fill()
#     circle(150, 280)
#     end_fill()
#
#
# def Doraemon():
#     head()
#     scarf()
#     face()
#     black_eyes()
#     nose()
#     mouth()
#     beard()
#     my_goto(0, 0)
#     seth(0)
#     penup()
#     circle(150, 50)
#     pendown()
#     seth(30)
#     fd(40)
#     seth(70)
#     circle(-30, 270)
#
#
#     fillcolor('#00a0de')
#     begin_fill()
#
#     seth(230)
#     fd(80)
#     seth(90)
#     circle(1000, 1)
#     seth(-89)
#     circle(-1000, 10)
#
#     # print(pos())
#
#     seth(180)
#     fd(70)
#     seth(90)
#     circle(30, 180)
#     seth(180)
#     fd(70)
#
#     # print(pos())
#     seth(100)
#     circle(-1000, 9)
#
#     seth(-86)
#     circle(1000, 2)
#     seth(230)
#     fd(40)
#
#     # print(pos())
#
#
#     circle(-30, 230)
#     seth(45)
#     fd(81)
#     seth(0)
#     fd(203)
#     circle(5, 90)
#     fd(10)
#     circle(5, 90)
#     fd(7)
#     seth(40)
#     circle(150, 10)
#     seth(30)
#     fd(40)
#     end_fill()
#
#     seth(70)
#     fillcolor('#ffffff')
#     begin_fill()
#     circle(-30)
#     end_fill()
#
#     my_goto(103.74, -182.59)
#     seth(0)
#     fillcolor('#ffffff')
#     begin_fill()
#     fd(15)
#     circle(-15, 180)
#     fd(90)
#     circle(-15, 180)
#     fd(10)
#     end_fill()
#
#     my_goto(-96.26, -182.59)
#     seth(180)
#     fillcolor('#ffffff')
#     begin_fill()
#     fd(15)
#     circle(15, 180)
#     fd(90)
#     circle(15, 180)
#     fd(10)
#     end_fill()
#
#     my_goto(-133.97, -91.81)
#     seth(50)
#     fillcolor('#ffffff')
#     begin_fill()
#     circle(30)
#     end_fill()
#
#     my_goto(-103.42, 15.09)
#     seth(0)
#     fd(38)
#     seth(230)
#     begin_fill()
#     circle(90, 260)
#     end_fill()
#
#     my_goto(5, -40)
#     seth(0)
#     fd(70)
#     seth(-90)
#     circle(-70, 180)
#     seth(0)
#     fd(70)
#
#     my_goto(-103.42, 15.09)
#     fd(90)
#     seth(70)
#     fillcolor('#ffd200')
#     # print(pos())
#     begin_fill()
#     circle(-20)
#     end_fill()
#     seth(170)
#     fillcolor('#ffd200')
#     begin_fill()
#     circle(-2, 180)
#     seth(10)
#     circle(-100, 22)
#     circle(-2, 180)
#     seth(180-10)
#     circle(100, 22)
#     end_fill()
#     goto(-13.42, 15.09)
#     seth(250)
#     circle(20, 110)
#     seth(90)
#     fd(15)
#     dot(10)
#     my_goto(0, -150)
#
#
#
# if __name__ == '__main__':
#     pensize(3)
#     speed(9)
#     Doraemon()
#     my_goto(100, -300)
#     write('@python.for.fun', font=("Bradley Hand ITC", 30, "bold"))
#     mainloop()
#
#
# import turtle
# import random
#
# wn=turtle.Screen()
# wn.setup(600,600)
# #wn.bgcolor(“white”)
# s=turtle.Turtle()
#
# r=10
# for i in range(200):
#     s.circle(r+i,45)
#     j=random.random()
#     k=random.random()
#     l=random.random()
#     s.pencolor((j,k,l))
# s.penup()
# s.home()
# s.pendown()
#
# m=20
# for i in range(200):
#     s.circle(m+i,45)
#     j=random.random()
#     k=random.random()
#     l=random.random()
#     s.pencolor((j,k,l))
# s.penup()
# s.home()
# s.pendown()
#
# n=30
# for i in range(200):
#     s.circle(n+i,45)
#     j=random.random()
#     k=random.random()
#     l=random.random()
#     s.pencolor((j,k,l))
#
# turtle.done()


from prettytable import PrettyTable
table = PrettyTable()
table.add_column("Pokemon Name", ["Pikachu", "Squirtle", "Charmander"])
table.add_column("Type", ["Electric", "Water", "Fire"])
table.align = "l"
print(table)
