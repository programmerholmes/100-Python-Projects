from logo import logo
import os

print(logo)

bidding = {}

flag = False
while flag != True:
    name = input("Enter your name: ")
    bid = int(input("Enter your bid: "))


    bidding[name] = bid

    ask = input("Is there another person who wants to bid? ").lower()
    if ask == "yes":
        os.system('cls')
    else:

        score = 0
        for bid in bidding:
            if bidding[bid] > score:
                score = bidding[bid]
                name = bid
        flag = True



print(f"{name} has the highest bid of ${score}")

