import cv2
import numpy as np

def locate_game_window(screenshot_path, template_path, offset=(-260, -40), min_confidence=0.8):
    """
    定位游戏窗口在截图中的位置，并返回截图中对应区域图像
    :param screenshot_path: 全屏截图路径
    :param template_path: 锚点图路径（窗口内某个特征性图块）
    :param offset: 从锚点偏移到左上角的像素位置（如 (-260, -40)）
    :param min_confidence: 模板匹配最低可信度
    :return: 截图中窗口区域图像、窗口左上角坐标、置信度
    """
    screenshot = cv2.imread(screenshot_path)
    template = cv2.imread(template_path)

    res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    if max_val < min_confidence:
        raise ValueError("❌ 无法定位游戏窗口，匹配度太低")

    anchor_top_left = max_loc
    window_top_left = (anchor_top_left[0] + offset[0], anchor_top_left[1] + offset[1])

    # 你可以提前写好窗口的宽高（比如固定为 350×620）
    window_width, window_height = 350, 620
    x1, y1 = window_top_left
    x2, y2 = x1 + window_width, y1 + window_height

    window_img = screenshot[y1:y2, x1:x2]
    return window_img, window_top_left, max_val

def extract_board_from_window(window_img, board_offset=(0, 0), board_size=(400, 650)):
    """
    从窗口图像中提取棋盘区域（假设棋盘位置相对于窗口固定）
    :param window_img: 从 locate_game_window 返回的图像
    :param board_offset: 棋盘在窗口图像中的偏移位置 (x, y)
    :param board_size: 棋盘的宽高 (w, h)
    :return: 棋盘图像
    """
    x_off, y_off = board_offset
    w, h = board_size
    board_img = window_img[y_off:y_off + h, x_off:x_off + w]
    return board_img

def split_board_into_cells(board_img, rows=8, cols=4):
    """
    将棋盘图像分割为 8×4 的小格子图像
    :param board_img: 棋盘区域图像
    :param rows: 行数（默认8）
    :param cols: 列数（默认4）
    :return: 一个二维列表 cells[row][col] 对应每个位置的图像
    """
    cell_height = board_img.shape[0] // rows
    cell_width = board_img.shape[1] // cols

    cells = []
    for row in range(rows):
        row_cells = []
        for col in range(cols):
            y1 = row * cell_height
            y2 = (row + 1) * cell_height
            x1 = col * cell_width
            x2 = (col + 1) * cell_width
            cell_img = board_img[y1:y2, x1:x2]
            row_cells.append(cell_img)
        cells.append(row_cells)
    return cells

# 获取窗口图像
window_img, pos, conf = locate_game_window(
    screenshot_path="../data/testimage.png",
    template_path="../data/window_anchor.png",
    offset=(-260, -40)  # 你观察到棋盘左上角比 anchor 偏移的像素量
)

board_img = extract_board_from_window(
    window_img,
    board_offset=(78, 115),     # 棋盘相对窗口左上角的偏移
    board_size=(195, 390)      # 棋盘宽高
)

cells = split_board_into_cells(board_img)

# 可视化某一个格子，比如第3行第2列：
cv2.imshow("cell[2][1]", cells[0][3])
cv2.waitKey(0)