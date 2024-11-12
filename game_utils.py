# game_utils.py

from typing import Callable, Optional, Any
from enum import Enum
import numpy as np

# 棋盘参数设置
BOARD_COLS = 7
BOARD_ROWS = 6
BOARD_SHAPE = (BOARD_ROWS, BOARD_COLS)
INDEX_HIGHEST_ROW = BOARD_ROWS - 1
INDEX_LOWEST_ROW = 0

# 棋盘数据类型和玩家标识
BoardPiece = np.int8  # 棋子的数据类型
NO_PLAYER = BoardPiece(0)  # 空位
PLAYER1 = BoardPiece(1)  # 玩家1
PLAYER2 = BoardPiece(2)  # 玩家2

# 棋子符号的字符串表示
BoardPiecePrint = str
NO_PLAYER_PRINT = BoardPiecePrint(' ')
PLAYER1_PRINT = BoardPiecePrint('X')
PLAYER2_PRINT = BoardPiecePrint('O')

# 玩家动作类型（列数）
PlayerAction = np.int8  

# 游戏状态的枚举类
class GameState(Enum):
    IS_WIN = 1
    IS_DRAW = -1
    STILL_PLAYING = 0

# 移动状态的枚举类
class MoveStatus(Enum):
    IS_VALID = 1
    WRONG_TYPE = 'Input is not a number.'
    NOT_INTEGER = 'Input is not an integer or equivalent to an integer.'
    OUT_OF_BOUNDS = 'Input is out of bounds.'
    FULL_COLUMN = 'Selected column is full.'

# 保存状态的占位符类（可用于复杂代理的状态保存）
class SavedState:
    pass

# 生成下一步操作的函数类型
GenMove = Callable[
    [np.ndarray, BoardPiece, Optional[SavedState]],  # 输入参数
    tuple[PlayerAction, Optional[SavedState]]  # 返回值
]

# 初始化棋盘状态
def initialize_game_state() -> np.ndarray:
    """
    返回一个表示游戏初始状态的空棋盘，形状为 BOARD_SHAPE，数据类型为 BoardPiece，初始化为 NO_PLAYER。
    """
    return np.full(BOARD_SHAPE, NO_PLAYER, dtype=BoardPiece)

# 棋盘状态转换为字符串格式，方便输出显示
def pretty_print_board(board: np.ndarray) -> str:
    """
    将棋盘转换为人类可读的字符串表示形式。棋盘顶部为最高行，底部为最低行。
    """
    board_str = "|==============|\n"
    for row in range(BOARD_ROWS - 1, -1, -1):  # 从最高行到最低行
        row_str = "|"
        for col in range(BOARD_COLS):
            piece = board[row, col]
            if piece == PLAYER1:
                row_str += PLAYER1_PRINT + " "
            elif piece == PLAYER2:
                row_str += PLAYER2_PRINT + " "
            else:
                row_str += NO_PLAYER_PRINT + " "
        row_str = row_str.strip() + "|\n"
        board_str += row_str
    board_str += "|==============|\n|0 1 2 3 4 5 6 |"
    return board_str

# 将字符串格式的棋盘状态转换回数组
def string_to_board(pp_board: str) -> np.ndarray:
    """
    将`pretty_print_board`的输出转换为np.ndarray格式。
    """
    lines = pp_board.strip().splitlines()[1:-2]  # 忽略顶部和底部的边界
    board = initialize_game_state()
    for i, line in enumerate(lines[::-1]):  # 从底部行开始填充
        for j, char in enumerate(line[1::2]):
            if char == PLAYER1_PRINT:
                board[i, j] = PLAYER1
            elif char == PLAYER2_PRINT:
                board[i, j] = PLAYER2
            else:
                board[i, j] = NO_PLAYER
    return board

# 应用玩家操作，将棋子放置在指定列的最低空位
def apply_player_action(board: np.ndarray, action: PlayerAction, player: BoardPiece):
    """
    将玩家棋子放置在指定列中的最低空位。
    """
    for row in range(BOARD_ROWS):
        if board[row, action] == NO_PLAYER:
            board[row, action] = player
            break

# 检查是否存在四个相同棋子相连，判断玩家是否获胜
def connected_four(board: np.ndarray, player: BoardPiece) -> bool:
    """
    检查是否存在四个相同棋子相连（横向、纵向或对角线）。
    """
    # 检查横向
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if np.all(board[row, col:col+4] == player):
                return True
    # 检查纵向
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - 3):
            if np.all(board[row:row+4, col] == player):
                return True
    # 检查正对角线
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if all(board[row + i, col + i] == player for i in range(4)):
                return True
    # 检查反对角线
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if all(board[row - i, col + i] == player for i in range(4)):
                return True
    return False

# 检查当前游戏状态
def check_end_state(board: np.ndarray, player: BoardPiece) -> GameState:
    """
    判断当前游戏状态：是否有玩家胜利、平局或继续游戏。
    """
    if connected_four(board, player):
        return GameState.IS_WIN
    elif np.all(board != NO_PLAYER):  # 检查是否所有格子已被填满
        return GameState.IS_DRAW
    else:
        return GameState.STILL_PLAYING

# 检查玩家操作是否合法
def check_move_status(board: np.ndarray, column: Any) -> MoveStatus:
    """
    检查玩家的输入是否为有效列，并返回相应的状态信息。
    """
    # 检查输入是否为数值
    try:
        column = int(float(column))
    except ValueError:
        return MoveStatus.WRONG_TYPE
    
    # 检查是否为整数
    if not isinstance(column, int):
        return MoveStatus.NOT_INTEGER
    
    # 检查是否在有效范围内
    if not (0 <= column < BOARD_COLS):
        return MoveStatus.OUT_OF_BOUNDS
    
    # 检查该列是否已满
    if board[INDEX_HIGHEST_ROW, column] != NO_PLAYER:
        return MoveStatus.FULL_COLUMN
    
    return MoveStatus.IS_VALID
