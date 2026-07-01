import random

def display_board(board):
    print("\n  " + board[0][0] + " | " + board[0][1] + " | " + board[0][2])
    print(" ---+---+---")
    print("  " + board[1][0] + " | " + board[1][1] + " | " + board[1][2])
    print(" ---+---+---")
    print("  " + board[2][0] + " | " + board[2][1] + " | " + board[2][2] + "\n")

# --- MINIMAX CORE LOGIC ---

def check_winner_simple(board):
    # Same logic as yours, just returning the winner icon
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != " ": return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != " ": return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != " ": return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != " ": return board[0][2]
    if not any(" " in row for row in board): return "Draw"
    return None

def minimax(board, depth, is_maximizing):
    result = check_winner_simple(board)
    if result == "O": return 10 - depth  # AI wins (prefer faster wins)
    if result == "X": return depth - 10  # Human wins (prefer slower losses)
    if result == "Draw": return 0

    if is_maximizing:
        best_score = -float('inf')
        for r in range(3):
            for c in range(3):
                if board[r][c] == " ":
                    board[r][c] = "O"
                    score = minimax(board, depth + 1, False)
                    board[r][c] = " " # Undo move
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for r in range(3):
            for c in range(3):
                if board[r][c] == " ":
                    board[r][c] = "X"
                    score = minimax(board, depth + 1, True)
                    board[r][c] = " " # Undo move
                    best_score = min(score, best_score)
        return best_score

# --- GAME ENGINE ---

def play_game():
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = 'X'
    game_running = True

    while game_running:
        display_board(board)

        if current_player == "X":
            # HUMAN TURN
            move = input("Enter your turn (1-9): ")
            moves_map = {"1":(0,0),"2":(0,1),"3":(0,2),"4":(1,0),"5":(1,1),"6":(1,2),"7":(2,0),"8":(2,1),"9":(2,2)}
            if move in moves_map:
                r, c = moves_map[move]
                if board[r][c] == " ":
                    board[r][c] = "X"
                    current_player = "O"
                else:
                    print("Taken!")
                    continue
            else: continue
        else:
            # COMPUTER TURN (MINIMAX)
            print("AI is calculating every possible future...")
            best_score = -float('inf')
            best_move = None
            for r in range(3):
                for c in range(3):
                    if board[r][c] == " ":
                        board[r][c] = "O"
                        score = minimax(board, 0, False)
                        board[r][c] = " "
                        if score > best_score:
                            best_score = score
                            best_move = (r, c)
            board[best_move[0]][best_move[1]] = "O"
            current_player = "X"

        # Win Checks
        winner = check_winner_simple(board)
        if winner:
            display_board(board)
            print(f"Result: {winner} wins!" if winner != "Draw" else "It's a Draw!")
            game_running = False

play_game()