def evaluate(board, side):
    score_map = {'R': 1, 'B': -1}
    score = 0
    for row in board:
        for cell in row:
            if cell == 'R':
                score += 1
            elif cell == 'B':
                score -= 1
    return score if side == 'R' else -score