from board.recognizer import recognize_board
from ai.strategy import suggest_move
from board.renderer import draw_suggestion
import cv2
import numpy as np

def recognize_board():
    # ✅ 模拟棋盘图像（空白背景）
    board_img = np.ones((640, 320, 3), dtype=np.uint8) * 255

    # ✅ 模拟棋子布局（2 个棋子）
    grid = [
        [None, None, None, None],
        [None, None, None, None],
        [None, 'R',   None, None],
        [None, 'B',   None, None],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
        [None, None, None, None],
    ]
    return board_img, grid
def main():
    print("🔍 正在识别棋盘...")
    board_img, grid = recognize_board()

    print("🧠 AI分析中...")
    move, score = suggest_move(grid, side='R')  # 红方

    print(f"✅ 推荐走法: {move}, 预估分数: {score}")
    img_with_arrow = draw_suggestion(board_img, move)
    cv2.imshow("AI 提示", img_with_arrow)
    cv2.waitKey(0)

if __name__ == '__main__':
    main()