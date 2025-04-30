import copy
import math

def check_win(board, player):
    """Checks if the specified player has won."""
    # Check rows
    for row in board:
        if all(cell == player for cell in row):
            return True
    # Check columns
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    # Check diagonals
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_draw(board):
    """Checks if the game is a draw (board full, no winner)."""
    # Assumes check_win has already been called for both players
    for row in board:
        if EMPTY in row:
            return False
    # Board is full, and since no one won, it's a draw
    return True

def get_available_moves(board):
    """Returns a list of available moves as (row, col) tuples."""
    moves = []
    for r in range(3):
        for c in range(3):
            if board[r][c] == EMPTY:
                moves.append((r, c))
    return moves

def evaluate_board(board):
    """Evaluates the board state from the AI's perspective."""
    if check_win(board, AI_PLAYER):
        return 1  # AI wins
    elif check_win(board, HUMAN_PLAYER):
        return -1 # Human wins
    elif is_draw(board):
        return 0  # Draw
    else:
        return None # Game not over

def minimax_alpha_beta(board, depth, alpha, beta, is_maximizing_player):
    """
    Minimax algorithm with Alpha-Beta pruning.
    Returns the best score achievable from the current board state.
    """
    score = evaluate_board(board)
    if score is not None:
        return score # Terminal state reached

    available_moves = get_available_moves(board)

    if is_maximizing_player: # AI's turn (Maximizer)
        max_eval = -math.inf
        for r, c in available_moves:
            board_copy = copy.deepcopy(board)
            board_copy[r][c] = AI_PLAYER
            eval_score = minimax_alpha_beta(board_copy, depth + 1, alpha, beta, False) # Opponent's turn next
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break # Beta cutoff (Pruning)
        return max_eval
    else: # Human's turn (Minimizer)
        min_eval = math.inf
        for r, c in available_moves:
            board_copy = copy.deepcopy(board)
            board_copy[r][c] = HUMAN_PLAYER
            eval_score = minimax_alpha_beta(board_copy, depth + 1, alpha, beta, True) # AI's turn next
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha:
                break # Alpha cutoff (Pruning)
        return min_eval

def find_best_move(board):
    """
    Finds the best move for the AI player using Minimax with Alpha-Beta pruning.
    """
    best_score = -math.inf
    best_move = None
    alpha = -math.inf
    beta = math.inf

    available_moves = get_available_moves(board)
    if not available_moves:
        return None # Should not happen if called on non-terminal state

    for r, c in available_moves:
        board_copy = copy.deepcopy(board)
        board_copy[r][c] = AI_PLAYER

        # Call minimax for the *opponent's* turn after AI makes the move
        score = minimax_alpha_beta(board_copy, 0, alpha, beta, False) # False because it's now Minimizer's turn

        # Update best score and move if current move is better
        if score > best_score:
            best_score = score
            best_move = (r, c)

        # Note: Alpha is updated here at the top level, although it's not strictly
        # necessary for finding the best move itself, only for pruning within
        # the recursive calls initiated by the next iteration of this loop.
        # We don't need the pruning logic directly in this top-level loop.
        # alpha = max(alpha, score) # Keep track of the best score AI can guarantee

    # Handle case where no moves improve score (e.g., only losing moves left)
    if best_move is None and available_moves:
        best_move = available_moves[0] # Default to first available move if all lead to loss/draw

    return best_move

AI_PLAYER = 'x'
HUMAN_PLAYER = 'y'
EMPTY = '.'

board = []
string = ""
for i in range(9):
    row = input()
    string += row
    row = row.strip().split(" ")
    row = [row[:3], row[3:6], row[6:]]
    board.append(row)

x_count = string.count('x')
y_count = string.count('y')
if x_count > y_count:
    AI_PLAYER = 'y'
    HUMAN_PLAYER = 'x'

xy = input().strip().split(" ")
x, y = int(xy[0]), int(xy[1])
squre = [board[x*3][y], board[x*3+1][y], board[x*3+2][y]]

move = find_best_move(squre)
print(x, y, move[0], move[1])
