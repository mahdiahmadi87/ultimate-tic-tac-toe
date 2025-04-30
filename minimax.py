import copy
import math

AI_PLAYER = None  # مشخص می‌شود بر اساس تعداد مهره‌ها
HUMAN_PLAYER = None
EMPTY = '.'

class SmallBoard:
    def __init__(self):
        self.grid = [[EMPTY for _ in range(3)] for _ in range(3)]
        self.winner = None

    def make_move(self, r, c, player):
        if self.grid[r][c] == EMPTY and self.winner is None:
            self.grid[r][c] = player
            self.update_winner()
            return True
        return False

    def update_winner(self):
        lines = self.grid + [list(col) for col in zip(*self.grid)] + [
            [self.grid[i][i] for i in range(3)],
            [self.grid[i][2 - i] for i in range(3)]
        ]
        for line in lines:
            if line.count(line[0]) == 3 and line[0] != EMPTY:
                self.winner = line[0]
                return
        if all(cell != EMPTY for row in self.grid for cell in row):
            self.winner = 'draw'

    def is_full(self):
        return all(cell != EMPTY for row in self.grid for cell in row)

class UltimateBoard:
    def __init__(self):
        self.boards = [[SmallBoard() for _ in range(3)] for _ in range(3)]
        self.main_winner = None

    def make_move(self, big_r, big_c, small_r, small_c, player):
        board = self.boards[big_r][big_c]
        success = board.make_move(small_r, small_c, player)
        self.update_main_winner()
        return success

    def update_main_winner(self):
        status_grid = [[board.winner for board in row] for row in self.boards]
        lines = status_grid + [list(col) for col in zip(*status_grid)] + [
            [status_grid[i][i] for i in range(3)],
            [status_grid[i][2 - i] for i in range(3)]
        ]
        for line in lines:
            if line.count(line[0]) == 3 and line[0] in (AI_PLAYER, HUMAN_PLAYER):
                self.main_winner = line[0]
                return
        if all(board.winner is not None for row in self.boards for board in row):
            self.main_winner = 'draw'

    def get_available_moves(self, big_r, big_c):
        board = self.boards[big_r][big_c]
        if board.winner is None:
            return [(big_r, big_c, r, c) for r in range(3) for c in range(3) if board.grid[r][c] == EMPTY]
        else:
            return [(br, bc, r, c) for br in range(3) for bc in range(3)
                    if self.boards[br][bc].winner is None
                    for r in range(3) for c in range(3) if self.boards[br][bc].grid[r][c] == EMPTY]

def evaluate_small_board(board, player):
    if board.winner == player:
        return 1
    elif board.winner == 'draw':
        return 0
    elif board.winner is not None:
        return -1
    return 0

def evaluate_board(ub):
    score = 0
    for row in ub.boards:
        for sb in row:
            score += evaluate_small_board(sb, AI_PLAYER)
    return score

def minimax(board, depth, alpha, beta, is_max):
    if depth == 0 or board.main_winner is not None:
        return evaluate_board(board)

    big_r, big_c = board.last_small if hasattr(board, 'last_small') else (0, 0)
    moves = board.get_available_moves(big_r, big_c)

    if is_max:
        max_eval = -math.inf
        for move in moves:
            new_board = copy.deepcopy(board)
            new_board.last_small = (move[2], move[3])
            new_board.make_move(*move, AI_PLAYER)
            eval = minimax(new_board, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for move in moves:
            new_board = copy.deepcopy(board)
            new_board.last_small = (move[2], move[3])
            new_board.make_move(*move, HUMAN_PLAYER)
            eval = minimax(new_board, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def find_best_move_ultimate(board, next_big_r, next_big_c):
    best_score = -math.inf
    best_move = None
    moves = board.get_available_moves(next_big_r, next_big_c)
    for move in moves:
        new_board = copy.deepcopy(board)
        new_board.last_small = (move[2], move[3])
        new_board.make_move(*move, AI_PLAYER)
        score = minimax(new_board, 4, -math.inf, math.inf, False)
        if score > best_score:
            best_score = score
            best_move = move
    return best_move

def parse_input():
    lines = [input().strip() for _ in range(10)]
    grid = [line.split() for line in lines[:9]]
    next_r, next_c = map(int, lines[9].split())
    return grid, next_r, next_c

def determine_players(grid):
    flat = [cell for row in grid for cell in row]
    x_count = flat.count('X')
    y_count = flat.count('O')
    if x_count == y_count:
        return 'X', 'O'
    else:
        return 'O', 'X'

def build_ultimate_board(grid):
    ub = UltimateBoard()
    for big_r in range(3):
        for big_c in range(3):
            for r in range(3):
                for c in range(3):
                    ch = grid[big_r*3 + r][big_c*3 + c]
                    if ch != EMPTY:
                        ub.boards[big_r][big_c].grid[r][c] = ch
            ub.boards[big_r][big_c].update_winner()
    ub.update_main_winner()
    return ub

def main():
    global AI_PLAYER, HUMAN_PLAYER
    grid, next_r, next_c = parse_input()
    AI_PLAYER, HUMAN_PLAYER = determine_players(grid)
    ub = build_ultimate_board(grid)
    move = find_best_move_ultimate(ub, next_r, next_c)
    if move:
        print(f"{move[0]} {move[1]} {move[2]} {move[3]}")
    else:
        print("-1 -1 -1 -1")

if __name__ == '__main__':
    main()
