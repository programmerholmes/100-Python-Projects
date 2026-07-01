import random


def display_board(board):
    print("\n  " + board[0][0] + " | " + board[0][1] + " | " + board[0][2])
    print(" ---+---+---")
    print("  " + board[1][0] + " | " + board[1][1] + " | " + board[1][2])
    print(" ---+---+---")
    print("  " + board[2][0] + " | " + board[2][1] + " | " + board[2][2] + "\n")


# Initialise an empty board
board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]


def play_game():
    current_player = 'X'  # Human is X
    game_running = True

    while game_running:
        display_board(board)

        # --- STEP 1: GET THE MOVE ---
        if current_player == "X":
            # HUMAN TURN
            x_and_o_input = input("Enter your turn (1-9): ")

            # Validation for numbers
            if not x_and_o_input.isdigit() or not (1 <= int(x_and_o_input) <= 9):
                print("Invalid entry, try again!")
                continue  # Skip the rest of the loop and ask again

            # This dictionary maps your 1-9 input to the actual board coordinates [row][col]
            # It replaces the need for 9 separate "if board[0][0]" checks!
            moves_map = {
                "1": (0, 0), "2": (0, 1), "3": (0, 2),
                "4": (1, 0), "5": (1, 1), "6": (1, 2),
                "7": (2, 0), "8": (2, 1), "9": (2, 2)
            }

            row, col = moves_map[x_and_o_input]

            if board[row][col] == " ":
                board[row][col] = current_player
                current_player = "O"  # Switch to computer
            else:
                print("Block taken, try a different square!")
                continue


        else:

            # --- COMPUTER TURN (The 'Thinker') ---

            print("Computer is thinking...")

            best_move = None

            # 1. BLOCKING/WINNING LOGIC

            # We scan every possible move to see if it results in a win or needs a block

            empty_spots = [(r, c) for r in range(3) for c in range(3) if board[r][c] == " "]

            # Check for a WIN first, then a BLOCK

            for icon in ["O", "X"]:

                for r, c in empty_spots:

                    # Temporarily "test" the move

                    board[r][c] = icon

                    # Check if this move creates a win

                    is_win = False

                    # (Same logic as your win checks below)

                    for i in range(3):

                        if (board[i][0] == board[i][1] == board[i][2] == icon or

                                board[0][i] == board[1][i] == board[2][i] == icon):
                            is_win = True

                    if (board[0][0] == board[1][1] == board[2][2] == icon or

                            board[0][2] == board[1][1] == board[2][0] == icon):
                        is_win = True

                    # Undo the "test" move

                    board[r][c] = " "

                    if is_win:
                        best_move = (r, c)

                        break

                if best_move: break

            # 2. DECISION

            if best_move:

                r, c = best_move

            else:

                # If no win/block found, pick a random empty spot

                r, c = random.choice(empty_spots)

            board[r][c] = "O"

            current_player = "X"

        # --- STEP 2: WIN CHECKS ---
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] == "X" or board[0][i] == board[1][i] == board[2][i] == "X":
                print("X wins!")
                game_running = False
            elif board[i][0] == board[i][1] == board[i][2] == "O" or board[0][i] == board[1][i] == board[2][i] == "O":
                print("O wins!")
                game_running = False

        # Diagonal Win Checks
        if board[0][0] == board[1][1] == board[2][2] != " " or board[0][2] == board[1][1] == board[2][0] != " ":
            winner = board[1][1]  # Since the middle is part of every diagonal win
            print(f"{winner} wins!")
            game_running = False

        # --- STEP 3: DRAW CHECK ---
        if game_running:
            if not any(" " in row for row in board):
                print("It's a draw!")
                game_running = False

    display_board(board)


play_game()