import cv2

def draw_suggestion(img, move):
    if not move: return img
    fr, fc, tr, tc, _ = move
    GRID_W, GRID_H = 80, 80
    x1 = fc * GRID_W + GRID_W // 2
    y1 = fr * GRID_H + GRID_H // 2
    x2 = tc * GRID_W + GRID_W // 2
    y2 = tr * GRID_H + GRID_H // 2
    cv2.arrowedLine(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return img