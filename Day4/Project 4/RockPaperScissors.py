import random

rock = ('''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
''')

paper = ('''
     _______
---'    ____)____
           ______)
          _______)
         _______)
---.__________)
''')

scissors = ('''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
''')

computer = ["rock", "paper", "scissors"]
they = random.choice(computer)

me = input("Choose your option: Type 0 for Rock, 1 for Paper, 2 for Scissors: \n").lower()

if me == "0" and they == "rock":
    print(f"you chose rock\n{rock} \n The computer chose rock{rock}\n It's a draw.")

elif me == "1" and they == "paper":
    print(f"you chose paper\n{paper} \n The computer chose paper{paper}\n It's a draw.")

elif me == "2" and they == "scissors":
    print(f"you chose scissors\n{scissors} \n The computer chose scissors{scissors}\n It's a draw.")

elif me == "0" and they == "paper":
    print(f"you chose rock\n{rock} \n The computer chose paper{paper}\n Computer won.")

elif me == "0" and they == "scissors":
    print(f"you chose rock\n{rock} \n The computer chose scissors{scissors}\n You won.")

elif me == "1" and they == "rock":
    print(f"you chose paper\n{paper} \n The computer chose rock{rock}\n You won.")

elif me == "1" and they == "scissors":
    print(f"you chose paper\n{paper} \n The computer chose scissors{scissors}\n Computer won.")

elif me == "2" and they == "rock":
    print(f"you chose scissors\n{scissors} \n The computer chose rock{rock}\n Computer won.")

elif me == "2" and they == "paper":
    print(f"you chose scissors\n{scissors} \n The computer chose paper{paper}\n You won.")

else:
    print("No possible combo")
