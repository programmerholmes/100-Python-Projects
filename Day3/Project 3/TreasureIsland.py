print('''*******************************************************************************
          |                   |                  |                     |
 _________|________________.=""_;=.______________|_____________________|_______
|                   |  ,-"_,=""     `"=.|                  |
|___________________|__"=._o`"-._        `"=.______________|___________________
          |                `"=._o`"=._      _`"=._                     |
 _________|_____________________:=._o "=._."_.-="'"=.__________________|_______
|                   |    __.--" , ; `"=._o." ,-"""-._ ".   |
|___________________|_._"  ,. .` ` `` ,  `"-._"-._   ". '__|___________________
          |           |o`"=._` , "` `; .". ,  "-._"-._; ;              |
 _________|___________| ;`-.o`"=._; ." ` '`."\` . "-._ /_______________|_______
|                   | |o;    `"-.o`"=._``  '` " ,__.--o;   |
|___________________|_| ;     (#) `-.o `"=.`_.--"_o.-; ;___|___________________
____/______/______/___|o;._    "      `".o|o_.--"    ;o;____/______/______/____
/______/______/______/_"=._o--._        ; | ;        ; ;/______/______/______/_
____/______/______/______/__"=._o--._   ;o|o;     _._;o;____/______/______/____
/______/______/______/______/____"=._o._; | ;_.--"o.--"_/______/______/______/_
____/______/______/______/______/_____"=.o|o_.--""___/______/______/______/____
/______/______/______/______/______/______/______/______/______/______/[TomekK]
*******************************************************************************''')
print("Welcome to Treasure Island")
print("Your mission is to find the treasure")

direction = input("You're at a crossroad. Would you like to go right or left? \n").lower()

if direction == "left":
    chance = input("You've come to a lake.Do you want to swim or wait for the boat? Type swim or wait! \n").lower()
    if chance == "wait":
        door = input("You've arrived to island safely. There are 3 doors in the house. Which door would you like to open next. Red, Blue, Yellow? \n").lower()
        if door == "yellow":
            print("You win! You've found the treasure")
        elif door == "red":
            print("Game over. Burned by fire!")
        elif door == "blue":
            print("Game over. Eaten by beasts!")
        else:
            print("Game over.")
    else:
        print("Game over. Attacked by a trout!")

else:
    print("Game over. You fell into a hole!")