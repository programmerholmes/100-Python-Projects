from Game_data import data
from art import logo
from art import vs
import random

print(logo)
score = 0
is_game = True

a = random.choice(data)

b = random.choice(data)

while is_game != False:

    print(f"Compare A: {a['name']}, a {a['description']}, from {a['country']}.")

    print(vs)

    print(f"Compare B: {b['name']}, a {b['description']}, from {b['country']}.")

    choose = input("Who has more followers? Type 'A' or 'B': ")

    if choose == 'a':
        if a["follower_count"] > b["follower_count"]:
            score += 1
            print(f"You're right! Current score: {score}")
            a = b
            b = random.choice(data)
        else:
            print(f"Sorry, that's wrong. Final score: {score}")
            is_game = False

    elif choose == 'b':
        if b["follower_count"] > a["follower_count"]:
            score += 1
            print(f"You're right! Current score: {score}")
            a = b
            b = random.choice(data)
        else:
            print(f"Sorry, that's wrong. Final score: {score}")
            is_game = False
