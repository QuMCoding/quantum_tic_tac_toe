"""
for Python >= 3.5
written in python 3.10.8
"""

import sys
import pygame
from typing import Sequence
from collections import defaultdict
import asyncio

import os
from datetime import datetime

GAMELOG_DIR = "gamelog"

if not os.path.exists(GAMELOG_DIR):
    os.makedirs(GAMELOG_DIR)


class WriteGameLog(object):
    def __init__(self):
        self.win = False
        self.current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.log_file_name = f"game_log_{self.current_time}.txt"
        self.log_path = os.path.join(GAMELOG_DIR, self.log_file_name)
        self.write_log("Game Start")

    def write_log(self, log_content, collapse_info=None, winning_info=False):
        if not self.win:
            self.current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            with open(self.log_path, "a") as f:
                f.write(f"[{self.current_time}] {log_content}\n")
                if collapse_info:
                    f.write(f"Collapse Information: {collapse_info}\n")
        if winning_info:
            self.win = True

# 中間的文字
class CenterText:
    """Centered Text Class"""

    def __init__(self, text, _x, _y, size=20, color=(0, 0, 0), bold=False):
        # 設定中心位置
        self.x = _x
        self.y = _y

        # 將pygame的字體設定好
        pygame.font.init()
        font = pygame.font.SysFont("Consolas", size, bold=bold)
        self.txt = font.render(text, True, color)  # 將需要的字轉化成pygame物件
        self.size = font.size(text)  # (width, height)

    # 將文字渲染到螢幕上
    def draw(self, screen):
        # 計算真實位置
        drawX = self.x - (self.size[0] / 2.)
        drawY = self.y - (self.size[1] / 2.)
        coords = (drawX, drawY)  # 真實座標
        screen.blit(self.txt, coords)  # 將東西渲染上去


# 在畫面上的OOXX
class OneMove(pygame.sprite.Sprite):
    """
    Add a cross or circle to the board.
    if player=0, it's cross
    if player=1, it's circle.
    """

    def __init__(self, player: int, number: int, pos: Sequence[int]):
        super().__init__()
        self.font = pygame.font.SysFont("Consolas", 15 if number > 0 else 40)  # 將字體設定好
        self.player = player  # 設定自己是O還是X
        self.number = number  # 若為負數，則為已被觀測的步。其絕對值為那步的下標數字
        self.size = 40 if number > 0 else 120  # 設定大小，已確定的步會較大
        self.image = pygame.image.load(r"assets/circle.png" if player == 1 else r"assets/cross.png")  # 設定自己的圖片
        self.image = pygame.transform.scale(self.image, (self.size, self.size))  # 設定圖片的大小
        # 將自己渲染到畫面上
        self.rect = pygame.Rect(pos[0], pos[1], 1, 1)
        self.image.blit(self.font.render(str(abs(number)), True, (0, 0, 0)), (self.size // 1.3, self.size // 2.2))


# 檢查有沒有環在遊戲裡，使用暴力法
def has_cycle(wanted_board):
    # 定義一個Tree的節點
    class Node:
        def __init__(self, val=None, roads=None, parent=None):
            self.parent = parent  # 自己的父節點
            self.next = []  # 自己的子節點
            self.val = val  # 自己的值
            self.roads = roads  # 所有道路，key為兩端，value為有幾條
            # 執行函式
            self.find_next()  # 找到所有子節點
            self.find_cyclic()  # 找到有環的部分

        # 找到子節點
        def find_next(self):
            # 將roads的keys裡包含自己的遍歷一次
            for _k, _v in {k: v for k, v in self.roads.items() if self.val in k}.items():
                # val的值為road的另一端
                # roads的值為所有不包含自己那條road的剩下的部分，也就是原本的roads把現在這條的value減1。"|"代表合併起來，限Python3.9以上
                # parent就是自己
                _next = Node(val=next(filter(lambda t: t != self.val, _k)),
                             roads={**{k: v for k, v in self.roads.items() if k != _k},
                                    **{k: v - 1 for k, v in self.roads.items() if k == _k and v - 1 > 0}},
                             parent=self)
                self.next.append(_next)  # 將子節點新增到next裡

        # 尋找有沒有環，一直往上找父節點
        def find_cyclic(self):
            global cycle  # 跟之後說cycle是全域的變數
            _now = self.parent  # 現在檢查的
            o = []  # 已經找過的節點

            # 找到沒有父節點為止
            while _now is not None:
                o.append(_now.val)  # 將現在檢查的放進已經找過的
                # 檢查自己的值是否與現在檢查的值相同，若相同則代表有環
                if _now.val == self.val:
                    cycle = set(o)
                    return o
                _now = _now.parent
            return None

    parsed = {_k: _v for _k, _v in wanted_board.items() if all(__v[1] > 0 for __v in _v)}
    paths = defaultdict(lambda *_: 0)
    for drxy, dpn in parsed.items():
        for _k, _v in parsed.items():
            for e in _v:
                if e in dpn and not _k == drxy:
                    paths[tuple(sorted((drxy, _k), key=lambda l: l[1] * 3 + l[0]))] += 1
    paths = {k: v // 2 for k, v in paths.items()}

    for i in set(i for _a in paths.keys() for i in _a):
        _n = Node(val=i, roads=paths)


def check_collapse(board_wanted, target_cycle):
    # BSF 廣度優先搜尋
    touched = set()
    waiting = [tuple(target_cycle)[0]]
    while waiting:
        touched.add(waiting[0])
        for cus in board_wanted[waiting[0]]:
            for w in (k for k, d in board_wanted.items() if cus in d and k not in touched):
                waiting.append(w)
        waiting.pop(0)
    return touched

winning_combinations = [
    [(0, 0), (0, 1), (0, 2)],
    [(1, 0), (1, 1), (1, 2)],
    [(2, 0), (2, 1), (2, 2)],
    [(0, 0), (1, 0), (2, 0)],
    [(0, 1), (1, 1), (2, 1)],
    [(0, 2), (1, 2), (2, 2)],
    [(0, 0), (1, 1), (2, 2)],
    [(0, 2), (1, 1), (2, 0)]
]

# 檢查有沒有贏家
def check_winner(board_wanted):
    for sim in (0, 1):
        for i in winning_combinations:
            c = True
            for j in i:
                if c:
                    if not j in board_wanted:
                        c = False
                        continue
                    else:
                        if len(board_wanted[j]) > 1:
                            c = False
                            continue
                        if board_wanted[j][0][1] > 0:
                            c = False
                            continue
                        if board_wanted[j][0][0] != sim:
                            c = False
                            continue
            if c:
                # print(sim)
                return sim
    return None

# 將dict格式的board渲染到畫面上
def board_render(board_wanted=None) -> None:
    for e in board_widgets:
        e.kill()
    board_widgets.empty()
    for k, v in board_wanted.items():
        for i, e in enumerate(v):
            fx = 90 + k[0] * 150 + (i % 3) * 40
            fy = 110 + k[1] * 150 + (i // 3) * 40
            move = OneMove(e[0], e[1], (fx, fy))
            board_widgets.add(move)


def error_msg(msg):
    global current_error_msg
    current_error_msg = msg
    print(msg)
    update_frame()


# 更新1幀
def update_frame(winner=None):
    root.fill((255, 255, 255))  # Fill the entire screen with white
    if winner is not None:
        # Draw the winner
        win_font = CenterText(f"{'O' if winner else 'X'} won!", 300, 80, size=40, color=(255, 0, 0), bold=True)
        win_font.draw(root)
        # Draw the boxes
        for r in range(3):
            for c in range(3):
                rect = pygame.Rect(80 + c * 150, 100 + r * 150, 150, 150)
                if hover_x == c and hover_y == r:
                    pygame.draw.rect(root, (200, 200, 200), rect)
                if rx == c and ry == r:
                    pygame.draw.rect(root, (200, 200, 0), rect)
                pygame.draw.rect(root, (0, 0, 0), rect, 3)
        
        board_render(board)
        board_widgets.draw(root)
        
        # Set the title
        head_font = CenterText("quantum tic-tac-toe", 300, 30, size=40, color=(0, 0, 0))
        head_font.draw(root)
        # Draw the exit button
        pygame.draw.rect(root, (0, 150, 250) if hover_action else (0, 100, 200), pygame.Rect(100, 600, 150, 80), border_radius=10)
        action_btn_word = CenterText("exit", 175, 640, size=30, color=(255, 255, 255))
        action_btn_word.draw(root)
        # Draw the reset button
        pygame.draw.rect(root, (250, 0, 0) if hover_restart else (200, 0, 0), pygame.Rect(350, 600, 150, 80), border_radius=10)
        reset_btn_word = CenterText("restart", 425, 640, size=30, color=(255, 255, 255))
        reset_btn_word.draw(root)
    else:
        # Draw the boxes
        for r in range(3):
            for c in range(3):
                rect = pygame.Rect(80 + c * 150, 100 + r * 150, 150, 150)
                if hover_x == c and hover_y == r:
                    pygame.draw.rect(root, (200, 200, 200), rect)
                if rx == c and ry == r:
                    pygame.draw.rect(root, (200, 200, 0), rect)
                pygame.draw.rect(root, (0, 0, 0), rect, 3)
        
        board_render(board)
        board_widgets.draw(root)
        
        # Set the title
        head_font = CenterText("quantum tic-tac-toe", 300, 30, size=40, color=(0, 0, 0))
        head_font.draw(root)
        
        # Set the turn message
        if not collapse_flag:
            if (ROUND // 2) % 2 == 0:
                turn_font = CenterText("X's turn", 300, 80, size=20, color=(0, 0, 0))
            else:
                turn_font = CenterText("O's turn", 300, 80, size=20, color=(0, 0, 0))
        else:
            turn_font = CenterText("collapse mode", 300, 80, size=20, color=(0, 0, 0))
        turn_font.draw(root)
        
        # Draw error message
        error_font = CenterText(current_error_msg, 300, 575, size=20, color=(200, 0, 0))
        error_font.draw(root)
        
        # Draw action button
        pygame.draw.rect(root, (0, 150, 250) if hover_action else (0, 100, 200), pygame.Rect(100, 600, 150, 80), border_radius=10)
        action_btn_word = CenterText("action", 175, 640, size=30, color=(255, 255, 255))
        action_btn_word.draw(root)
        
        # Draw reset button
        pygame.draw.rect(root, (250, 0, 0) if hover_restart else (200, 0, 0), pygame.Rect(350, 600, 150, 80), border_radius=10)
        reset_btn_word = CenterText("restart", 425, 640, size=30, color=(255, 255, 255))
        reset_btn_word.draw(root)
        
        board_widgets.update()
    pygame.display.update()



# 初始化pygame
pygame.init()
# 設定使用者畫面
root = pygame.display.set_mode((600, 800))
# 設定視窗標題
pygame.display.set_caption("quantum tic-tac-toe")

def init():
    global WGL, ROUND, hover_x, hover_y, hover_action, hover_restart, rx, ry, srx, sry, collapse_flag, current_error_msg, board, cycle, board_widgets, winner
    WGL = WriteGameLog()

    # 定義遊戲內狀況
    board = defaultdict(list)

    hover_x, hover_y = None, None  # 滑鼠在哪一格
    hover_action, hover_restart = None, None # 滑鼠在哪一個按鈕

    ROUND = 0  # 第幾回合
    winner = None  # 誰贏了
    rx, ry, srx, sry = None, None, None, None  # 使用者目前與哪一格互動

    cycle = set()  # 有沒有cycle
    has_cycle(board)  # 找出cycle
    collapse_flag = False

    current_error_msg = ""  # 當前的錯誤訊息

    # 畫OOXX的群組
    board_widgets = pygame.sprite.Group()

async def main():
    global WGL, ROUND, hover_x, hover_y, hover_action, hover_restart, rx, ry, srx, sry, collapse_flag, current_error_msg, board, cycle, board_widgets, winner
    init()
    update_frame()

    while True:
        if winner is not None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    WGL.write_log("Game End")
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if 350 <= x <= 500 and 600 <= y <= 680:
                        WGL.write_log("Game Restart")
                        init()
                        update_frame()
                    if 100 <= x <= 250 and 600 <= y <= 680:
                        WGL.write_log("Game End")
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.MOUSEMOTION:
                    x, y = event.pos
                    if 300 <= x <= 450 and 600 <= y <= 680:
                        hover_restart = True
                    elif 100 <= x <= 250 and 600 <= y <= 680:
                        hover_action = True
                    else:
                        hover_restart, hover_action = None, None
                    update_frame(winner)

            WGL.write_log(f"Player {winner} wins", winning_info=True)
            update_frame(winner)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    WGL.write_log("Game End")
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    # boxes
                    _rx = (x - 80) // 150
                    _ry = (y - 100) // 150
                    _rx = _rx if 0 <= _rx <= 2 else None
                    _ry = _ry if 0 <= _ry <= 2 else None
                    if not (_rx is None or _ry is None):
                        rx, ry = _rx, _ry
                        # in collapse mode, need more detail.
                        if collapse_flag:
                            sub_rx = (x - 80 - rx * 150) // 50
                            sub_ry = (y - 100 - ry * 150) // 50
                            sub_rx = sub_rx if 0 <= sub_rx <= 2 else None
                            sub_ry = sub_ry if 0 <= sub_ry <= 2 else None
                            if not (sub_rx is None or sub_ry is None):
                                srx, sry = sub_rx, sub_ry
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    _rx = (x - 80) // 150
                    _ry = (y - 100) // 150
                    _rx = _rx if 0 <= _rx <= 2 else None
                    _ry = _ry if 0 <= _ry <= 2 else None
                    if not (_rx is None or _ry is None):
                        rx, ry = _rx, _ry
                        update_frame()
                    # triggered the button
                    if 350 <= x <= 500 and 600 <= y <= 680:
                        ROUND = 0
                        rx, ry, srx, sry = None, None, None, None
                        cycle = set()
                        has_cycle(board)
                        collapse_flag = False
                        current_error_msg = ""
                        board.clear()
                        board_widgets.empty()
                        update_frame()
                        if not board == {}:
                            WGL.write_log("Game Restart")
                            WGL = WriteGameLog()
                    if 100 <= x <= 250 and 600 <= y <= 680:
                        if rx is None or ry is None:
                            error_msg("make a move")
                            continue
                        # check if is determined
                        if board[(rx, ry)] and board[(rx, ry)][0][1] < 0:
                            error_msg("you should not place a symbol in a determined box")
                            continue
                        # regular move
                        if not collapse_flag:
                            collapse_flag = False
                            # check if the symbol is already in the box
                            if ((ROUND // 2) % 2, ROUND // 4 + 1) in board[rx, ry]:
                                error_msg("you should not place two same symbols in one box")
                                continue

                            # mess with board
                            board[rx, ry].append(((ROUND // 2) % 2, ROUND // 4 + 1))
                            WGL.write_log(f"Player {((ROUND // 2) % 2) + 1} placed a {'O' if  ((ROUND // 2) % 2) else 'X'}{(ROUND // 2) + 1} in box ({rx}, {ry})")
                            rx, ry = None, None
                            if ROUND % 2 == 1:
                                # check if it's cyclic
                                cycle = set()
                                has_cycle(board)
                                if len(cycle) > 0:
                                    collapse_flag = True
                            current_error_msg = ""
                            ROUND += 1
                        # collapse move
                        else:
                            collapse_flag = True
                            collapse_boxes = check_collapse(board, cycle)  # the boxes that will be changed
                            collapse = board[(rx, ry)]  # the box the user chose
                            # check if user's input is valid
                            if (srx is None or sry is None):
                                error_msg("make a move")
                                continue
                            if (srx + sry * 3) >= len(collapse):
                                error_msg("click on the symbol you want to collapse")
                                continue
                            exit_closed_loop_flag = False
                            retrace_board = board.copy()
                            while True:
                                retrace_only_one = [i for i in collapse_boxes if len(retrace_board[i]) == 1]
                                if collapse[srx + sry * 3] in (retrace_board[_l][0] for _l in retrace_only_one):
                                    error_msg("you must observe the symbol in the closed loop")
                                    exit_closed_loop_flag = True
                                    break
                                # remove the pair of only one inside board
                                for _l in retrace_only_one:
                                    die_symbol = retrace_board[_l][0]
                                    for con in collapse_boxes:
                                        retrace_board[con] = [o for o in retrace_board[con] if o not in (die_symbol,)]

                                if len(retrace_only_one) == 0:
                                    break
                            if exit_closed_loop_flag:
                                continue

                            # start eliminating/collapsing
                            eliminated = {(rx, ry), }  # store who has been eliminated
                            death_note = set()  # store who should be died
                            board[rx, ry] = [collapse[srx + sry * 3]]  # kill the opposite of which user picked
                            while len(eliminated) < len(collapse_boxes):  # if everyone is "processed"
                                for c in collapse_boxes:
                                    if len(board[c]) <= 1:
                                        board[c] = [(board[c][0][0], abs(board[c][0][1]) * -1)]
                                        death_note.add((board[c][0][0], abs(board[c][0][1])))
                                        eliminated.add(c)
                                    for con in collapse_boxes:
                                        board[con] = [o for o in board[con] if o not in death_note]
                            WGL.write_log(f"Player {(((ROUND + 1) // 2) % 2) + 1} collapsed the box ({rx}, {ry}){'O' if board[rx, ry][0][0] else 'X'}{abs(board[rx, ry][0][1])}")
                            collapse_flag = False
                            board_widgets.empty()
                            current_error_msg = ""
                            try:
                                winner = check_winner(board)
                            except Exception as e:
                                print(e)
                                continue
                        update_frame()

                if event.type == pygame.MOUSEMOTION:  # Check for mouse motion
                    x, y = event.pos
                    # Check if mouse is over a box
                    _rx = (x - 80) // 150
                    _ry = (y - 100) // 150
                    _rx = _rx if 0 <= _rx <= 2 else None
                    _ry = _ry if 0 <= _ry <= 2 else None
                    if not (_rx is None or _ry is None):
                        hover_x, hover_y = _rx, _ry
                        update_frame()
                        # print("Mouse is over box", _ry, _rx)
                    elif 100 <= x <= 250 and 600 <= y <= 680:
                        hover_action = True
                        update_frame()
                    elif 350 <= x <= 500 and 600 <= y <= 680:
                        hover_restart = True
                        update_frame()
                    else:
                        hover_x, hover_y, hover_action, hover_restart = None, None, None, None
                        update_frame()
                        # print("Mouse is not over a box")
        await asyncio.sleep(0.0)

if __name__ == '__main__':
    asyncio.run(main())
                
