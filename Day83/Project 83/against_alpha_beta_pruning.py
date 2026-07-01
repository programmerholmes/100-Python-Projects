import random


def display_board(board):
    print("\n  " + board[0][0] + " | " + board[0][1] + " | " + board[0][2])
    print(" ---+---+---")
    print("  " + board[1][0] + " | " + board[1][1] + " | " + board[1][2])
    print(" ---+---+---")
    print("  " + board[2][0] + " | " + board[2][1] + " | " + board[2][2] + "\n")


# --- CORE LOGIC: WINNER & MINIMAX ---

def check_winner(board):
    # Rows and Columns
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != " ": return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != " ": return board[0][i]

    # Diagonals
    if board[0][0] == board[1][1] == board[2][2] != " ": return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != " ": return board[0][2]

    # Check for Draw
    if not any(" " in row for row in board): return "Draw"

    return None


def minimax(board, depth, alpha, beta, is_maximizing):
    result = check_winner(board)
    if result == "O": return 10 - depth  # AI Wins
    if result == "X": return depth - 10  # Human Wins
    if result == "Draw": return 0

    if is_maximizing:
        best_score = -float('inf')
        for r in range(3):
            for c in range(3):
                if board[r][c] == " ":
                    board[r][c] = "O"
                    score = minimax(board, depth + 1, alpha, beta, False)
                    board[r][c] = " "
                    best_score = max(score, best_score)
                    # --- ALPHA-BETA PRUNING ---
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break  # Prune the branch
        return best_score
    else:
        best_score = float('inf')
        for r in range(3):
            for c in range(3):
                if board[r][c] == " ":
                    board[r][c] = "X"
                    score = minimax(board, depth + 1, alpha, beta, True)
                    board[r][c] = " "
                    best_score = min(score, best_score)
                    # --- ALPHA-BETA PRUNING ---
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break  # Prune the branch
        return best_score


# --- GAME ENGINE ---

def play_game():
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = 'X'
    game_running = True

    print("Welcome to Tic-Tac-Toe AI!")
    print("You are X, the Computer is O.")

    while game_running:
        display_board(board)

        if current_player == "X":
            # --- HUMAN TURN ---
            move = input("Enter your move (1-9): ")
            moves_map = {
                "1": (0, 0), "2": (0, 1), "3": (0, 2),
                "4": (1, 0), "5": (1, 1), "6": (1, 2),
                "7": (2, 0), "8": (2, 1), "9": (2, 2)
            }
            if move in moves_map:
                r, c = moves_map[move]
                if board[r][c] == " ":
                    board[r][c] = "X"
                    current_player = "O"
                else:
                    print("That square is taken!")
                    continue
            else:
                print("Invalid input, please enter 1-9.")
                continue
        else:
            # --- AI TURN (Pruned Minimax) ---
            print("AI is calculating...")
            best_score = -float('inf')
            best_move = None

            # Start the search
            for r in range(3):
                for c in range(3):
                    if board[r][c] == " ":
                        board[r][c] = "O"
                        # We pass initial alpha (-inf) and beta (+inf)
                        score = minimax(board, 0, -float('inf'), float('inf'), False)
                        board[r][c] = " "
                        if score > best_score:
                            best_score = score
                            best_move = (r, c)

            if best_move:
                board[best_move[0]][best_move[1]] = "O"
            current_player = "X"

        # Check for winner
        result = check_winner(board)
        if result:
            display_board(board)
            if result == "Draw":
                print("Game Over: It's a draw!")
            else:
                print(f"Game Over: {result} wins!")
            game_running = False


if __name__ == "__main__":
    play_game()