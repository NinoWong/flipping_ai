import cv2
import numpy as np

# 读取全屏截图和模板图
screenshot = cv2.imread("data/testimage.png")
template = cv2.imread("data/window_anchor.png")  # 你预先裁剪好的小模板

# 模板匹配
res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
_, max_val, _, max_loc = cv2.minMaxLoc(res)

if max_val < 0.8:
    print("无法定位游戏窗口，匹配度太低")
else:
    top_left = max_loc
    print(f"游戏窗口定位在：{top_left}")

    # 假设从这个点偏移一定距离得到棋盘
    board_top_left = (top_left[0] - 260, top_left[1] - 40)
    board_bottom_right = (board_top_left[0] + 350, board_top_left[1] + 620)

    board_img = screenshot[board_top_left[1]:board_bottom_right[1], board_top_left[0]:board_bottom_right[0]]
    cv2.imshow("棋盘区域", board_img)
    cv2.waitKey(0)