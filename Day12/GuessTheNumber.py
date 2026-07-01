from art import logo
import random
print(logo)

print("Welcome to the Number Guessing Game!")
print("I'm thinking of a number between 1 and 100.")


def choose_difficulty():
    difficulty = input("Choose a difficulty. Type 'easy', 'medium' or 'hard': ").lower()
    if difficulty == 'easy':
        attempts = 10
    elif difficulty == 'medium':
        attempts = 7
    elif difficulty == 'hard':
        attempts = 5
    else:
        print("Invalid Entry!")

    return attempts


def check_guess(guess, number, attempts):
    if guess == number:
        print(f"You got it the answer was {number}")
        return -2
    elif guess > number:
        print("Too High!")
        attempts = attempts - 1
        if attempts != 0:
            print("Guess again!")
            return attempts
        return 0
    elif guess < number:
        print("Too low!")
        attempts = attempts - 1
        if attempts != 0:
            print("Guess again!")
            return attempts
        return 0

attempts = choose_difficulty()

number = random.randint(1, 100)

while attempts != 0:
    if attempts == -2:
        break
    elif attempts == 0:
        break
    print(f"You have {attempts} attempts remaining to guess the number!")
    guess = int(input("Make a Guess: "))
    attempts = check_guess(guess, number, attempts)
if attempts == -2:
    print("Congratulations!")
else:
    print("You lose!")