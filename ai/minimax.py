
import copy
from ai.evaluator import evaluate

# 简化的棋盘走法生成器
def generate_moves(board, side):
    moves = []
    for r in range(len(board)):
        for c in range(len(board[0])):
            piece = board[r][c]
            if piece == side:
                # 这里只示例简单的上下左右走法，不考虑规则限制
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < len(board) and 0 <= nc < len(board[0]):
                        if board[nr][nc] is None or board[nr][nc] != side:
                            moves.append((r, c, nr, nc, board[nr][nc]))  # (from_row, from_col, to_row, to_col, captured)
    return moves

def apply_move(board, move):
    r1, c1, r2, c2, _ = move
    new_board = copy.deepcopy(board)
    new_board[r2][c2] = new_board[r1][c1]
    new_board[r1][c1] = None
    return new_board

def minimax(board, side, depth):
    best_score = float('-inf')
    best_move = None

    moves = generate_moves(board, side)
    for move in moves:
        new_board = apply_move(board, move)
        score = minimax_recursive(new_board, switch_side(side), depth - 1, False)
        if score > best_score:
            best_score = score
            best_move = move

    return best_move, best_score

def minimax_recursive(board, side, depth, is_maximizing):
    if depth == 0:
        return evaluate(board, side)

    moves = generate_moves(board, side)
    if not moves:
        return evaluate(board, side)

    if is_maximizing:
        best_score = float('-inf')
        for move in moves:
            new_board = apply_move(board, move)
            score = minimax_recursive(new_board, switch_side(side), depth - 1, False)
            best_score = max(best_score, score)
        return best_score
    else:
        best_score = float('inf')
        for move in moves:
            new_board = apply_move(board, move)
            score = minimax_recursive(new_board, switch_side(side), depth - 1, True)
            best_score = min(best_score, score)
        return best_score

def switch_side(side):
    return 'B' if side == 'R' else 'R'