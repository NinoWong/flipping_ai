from ai.minimax import minimax

def suggest_move(grid, side='R'):
    return minimax(grid, side, depth=2)