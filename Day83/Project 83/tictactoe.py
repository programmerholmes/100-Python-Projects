def display_board(board):
    print("\n  " + board[0][0] + " | " + board[0][1] + " | " + board[0][2])
    print(" ---+---+---")
    print("  " + board[1][0] + " | " + board[1][1] + " | " + board[1][2])
    print(" ---+---+---")
    print("  " + board[2][0] + " | " + board[2][1] + " | " + board[2][2] + "\n")

# Initialise an empty board
board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]

def play_game():
    current_player = 'X'
    game_running = True
    # ... (functions for board, win check, etc. defined here or imported)

    while game_running:
        display_board(board)

        x_and_o_input = input("Enter your turn: ")
        if 1 <= int(x_and_o_input) <= 9:
            if x_and_o_input == "1":
                if board[0][0] == " ":
                    board[0][0] = current_player
                    if current_player == "X":
                        current_player = "O"
                    else:
                        current_player = "X"
                else:
                    print("Block taken, try a different square!")
            elif x_and_o_input == "2":
                if board[0][1] == " ":
                    board[0][1] = current_player
                    if current_player == "X":
                        current_player = "O"
                    else:
                        current_player = "X"
                else:
                    print("Block taken, try a different square!")
            elif x_and_o_input == "3":
                if board[0][2] == " ":
                    board[0][2] = current_player
                    if current_player == "X":
                        current_player = "O"
                    else:
                        current_player = "X"
                else:
                    print("Block taken, try a different square!")
            elif x_and_o_input == "4":
                if board[1][0] == " ":
                    board[1][0] = current_player
                    if current_player == "X":
                        current_player = "O"
                    else:
                        current_player = "X"
                else:
                    print("Block taken, try a different square!")
            elif x_and_o_input == "5":
                if board[1][1] == " ":
                    board[1][1] = current_player
                    if current_player == "X":
                        current_player = "O"
                    else:
                        current_player = "X"
                else:
                    print("Block taken, try a different square!")
            elif x_and_o_input == "6":
                if board[1][2] == " ":
                    board[1][2] = current_player
                    if current_player == "X":
                        current_player = "O"
                    else:
                        current_player = "X"
                else:
                    print("Block taken, try a different square!")
            elif x_and_o_input == "7":
                if board[2][0] == " ":
                    board[2][0] = current_player
                    if current_player == "X":
                        current_player = "O"
                    else:
                        current_player = "X"
                else:
                    print("Block taken, try a different square!")
            elif x_and_o_input == "8":
                if board[2][1] == " ":
                    board[2][1] = current_player
                    if current_player == "X":
                        current_player = "O"
                    else:
                        current_player = "X"
                else:
                    print("Block taken, try a different square!")
            elif x_and_o_input == "9":
                if board[2][2] == " ":
                    board[2][2] = current_player
                    if current_player == "X":
                        current_player = "O"
                    else:
                        current_player = "X"
                else:
                    print("Block taken, try a different square!")
        else:
            print("Invalid entry, try again!")


        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] == "X":
                print("X wins!")
                game_running = False
            elif board[i][0] == board[i][1] == board[i][2] == "O":
                print("O wins!")
                game_running = False
            elif board[0][i] == board[1][i] == board[2][i] == "X":
                print("X wins!")
                game_running = False
            elif board[0][i] == board[1][i] == board[2][i] == "O":
                print("O wins!")
                game_running = False

        if board[0][0] == board[1][1] == board[2][2] == "X":
            print("X wins!")
            game_running = False
        elif board[0][0] == board[1][1] == board[2][2] == "O":
            print("O wins!")
            game_running = False
        elif board[0][2] == board[1][1] == board[2][0] == "X":
            print("X wins!")
            game_running = False
        elif board[0][2] == board[1][1] == board[2][0] == "O":
            print("O wins!")
            game_running = False

        if game_running:
            if not any(" " in row for row in board):
                print("It's a draw!")
                game_running = False

    display_board(board)
play_game()