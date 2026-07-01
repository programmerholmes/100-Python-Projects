############### Blackjack Project #####################

#Difficulty Normal 😎: Use all Hints below to complete the project.
#Difficulty Hard 🤔: Use only Hints 1, 2, 3 to complete the project.
#Difficulty Extra Hard 😭: Only use Hints 1 & 2 to complete the project.
#Difficulty Expert 🤯: Only use Hint 1 to complete the project.

############### Our Blackjack House Rules #####################

## The deck is unlimited in size.
## There are no jokers.
## The Jack/Queen/King all count as 10.
## The the Ace can count as 11 or 1.
## Use the following list as the deck of cards:
## cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
## The cards in the list have equal probability of being drawn.
## Cards are not removed from the deck as they are drawn.
## The computer is the dealer.

##################### Hints #####################

#Hint 1: Go to this website and try out the Blackjack game:
#   https://games.washingtonpost.com/games/blackjack/
#Then try out the completed Blackjack project here:
#   http://blackjack-final.appbrewery.repl.run

#Hint 2: Read this breakdown of program requirements:
#   http://listmoz.com/view/6h34DJpvJBFVRlZfJvxF
#Then try to create your own flowchart for the program.

#Hint 3: Download and read this flow chart I've created:
#   https://drive.google.com/uc?export=download&id=1rDkiHCrhaf9eX7u7yjM1qwSuyEk-rPnt

#Hint 4: Create a deal_card() function that uses the List below to *return* a random card.
#11 is the Ace.
#cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]

#Hint 5: Deal the user and computer 2 cards each using deal_card() and append().
#user_cards = []
#computer_cards = []

#Hint 6: Create a function called calculate_score() that takes a List of cards as input
#and returns the score.
#Look up the sum() function to help you do this.

#Hint 7: Inside calculate_score() check for a blackjack (a hand with only 2 cards: ace + 10) and return 0 instead of the actual score. 0 will represent a blackjack in our game.

#Hint 8: Inside calculate_score() check for an 11 (ace). If the score is already over 21, remove the 11 and replace it with a 1. You might need to look up append() and remove().

#Hint 9: Call calculate_score(). If the computer or the user has a blackjack (0) or if the user's score is over 21, then the game ends.

#Hint 10: If the game has not ended, ask the user if they want to draw another card. If yes, then use the deal_card() function to add another card to the user_cards List. If no, then the game has ended.

#Hint 11: The score will need to be rechecked with every new card drawn and the checks in Hint 9 need to be repeated until the game ends.

#Hint 12: Once the user is done, it's time to let the computer play. The computer should keep drawing cards as long as it has a score less than 17.

#Hint 13: Create a function called compare() and pass in the user_score and computer_score. If the computer and user both have the same score, then it's a draw. If the computer has a blackjack (0), then the user loses. If the user has a blackjack (0), then the user wins. If the user_score is over 21, then the user loses. If the computer_score is over 21, then the computer loses. If none of the above, then the player with the highest score wins.

#Hint 14: Ask the user if they want to restart the game. If they answer yes, clear the console and start a new game of blackjack and show the logo from art.py.

def game():

    from art import logo
    import random
    print(logo)

    def deal_card():

            cards = [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
            store = random.choice(cards)
            return store

    def calculate_score(list_of_cards):
        if list_of_cards[0] == 11 and list_of_cards[1] == 10 or list_of_cards[0] == 10 and list_of_cards[1] == 11:
            return 0
        else:
            total = sum(list_of_cards)
            if 11 in list_of_cards and total > 21:
                list_of_cards.remove(11)
                list_of_cards.append(1)
                total = sum(list_of_cards)
            return total

    def compare(user_score, computer_score):
        if user_score == computer_score:
            return "Draw 🙃"
        elif computer_score == 0:
            return "Lose, opponent has Blackjack 😱"
        elif user_score == 0:
            return "Win with a Blackjack 😎"
        elif user_score > 21:
            return "You went over. You lose 😭"
        elif computer_score > 21:
            return "Opponent went over. You win 😁"
        elif user_score > computer_score:
            return "You win 😃"
        else:
            return "You lose 😤"

    user_cards = []
    computer_cards = []
    for i in range(0, 2):
        user_cards.append(deal_card())
        computer_cards.append(deal_card())
    print(f"{user_cards} Current score: {sum(user_cards)}")
    # print(computer_cards)
    print(f"Computer's first card: {computer_cards[0]}")


    flag = True
    while flag == True:
        user_sum = calculate_score(user_cards)
        computer_sum = calculate_score(computer_cards)
        if user_sum == 0 and computer_sum == 0:
            print("It's a draw!")
        elif user_sum == 0 or computer_sum > 21 or user_sum == 21:
            print("You won!!!")
            flag = False
        elif computer_sum == 0 or user_sum > 21 or computer_sum == 21:
            print("Computer won!!!")
            flag = False
        else:
            another = input("Do you want to draw another card? Type 'y' for yes and 'n' for no: ").lower()
            if another == 'y':
                user_cards.append(deal_card())
                print(user_cards)
            elif another == 'n':
                if computer_sum < 17:
                    while computer_sum < 17:
                        computer_cards.append(deal_card())
                        computer_sum = calculate_score(computer_cards)
                        print(computer_cards)
                if computer_sum > 16:
                    print(compare(user_sum, computer_sum))
                flag = False

    print(user_sum)
    print(computer_sum)

    ask = input("Do you want to restart the game? Type '1' for yes and '0' for no: ")
    if ask == '1':
        game()
    elif ask == '0':
        print("Good Night")
    else:
        print("Invalid command")

game()