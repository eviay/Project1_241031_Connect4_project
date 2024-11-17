from typing import Callable, Optional, Any
from enum import Enum
import numpy as np

BOARD_COLS = 7
BOARD_ROWS = 6
BOARD_SHAPE = (BOARD_ROWS, BOARD_COLS)
INDEX_HIGHEST_ROW = BOARD_ROWS - 1
INDEX_LOWEST_ROW = 0

BoardPiece = np.int8  
NO_PLAYER = BoardPiece(0) 
PLAYER1 = BoardPiece(1)  
PLAYER2 = BoardPiece(2)  

BoardPiecePrint = str
NO_PLAYER_PRINT = BoardPiecePrint(' ')
PLAYER1_PRINT = BoardPiecePrint('X')
PLAYER2_PRINT = BoardPiecePrint('O')

PlayerAction = np.int8  

class GameState(Enum):
    IS_WIN = 1
    IS_DRAW = -1
    STILL_PLAYING = 0

class MoveStatus(Enum):
    IS_VALID = 1
    WRONG_TYPE = 'Input is not a number.'
    NOT_INTEGER = 'Input is not an integer or equivalent to an integer.'
    OUT_OF_BOUNDS = 'Input is out of bounds.'
    FULL_COLUMN = 'Selected column is full.'

class SavedState:
    pass


GenMove = Callable[
    [np.ndarray, BoardPiece, Optional[SavedState]],  
    tuple[PlayerAction, Optional[SavedState]]  
]

def initialize_game_state() -> np.ndarray:

    return np.full(BOARD_SHAPE, NO_PLAYER, dtype=BoardPiece)

def pretty_print_board(board: np.ndarray) -> str:

    board_str = "|==============|\n"
    for row in range(BOARD_ROWS - 1, -1, -1):  
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

def string_to_board(pp_board: str) -> np.ndarray:
    lines = pp_board.strip().splitlines()[1:-2]  
    board = initialize_game_state()
    for i, line in enumerate(lines[::-1]):  
        for j, char in enumerate(line[1::2]):
            if char == PLAYER1_PRINT:
                board[i, j] = PLAYER1
            elif char == PLAYER2_PRINT:
                board[i, j] = PLAYER2
            else:
                board[i, j] = NO_PLAYER
    return board

def apply_player_action(board: np.ndarray, action: PlayerAction, player: BoardPiece):
    for row in range(BOARD_ROWS):
        if board[row, action] == NO_PLAYER:
            board[row, action] = player
            break

def connected_four(board: np.ndarray, player: BoardPiece) -> bool:
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if np.all(board[row, col:col+4] == player):
                return True
    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - 3):
            if np.all(board[row:row+4, col] == player):
                return True
    for row in range(BOARD_ROWS - 3):
        for col in range(BOARD_COLS - 3):
            if all(board[row + i, col + i] == player for i in range(4)):
                return True
    for row in range(3, BOARD_ROWS):
        for col in range(BOARD_COLS - 3):
            if all(board[row - i, col + i] == player for i in range(4)):
                return True
    return False

def check_end_state(board: np.ndarray, player: BoardPiece) -> GameState:
    if connected_four(board, player):
        return GameState.IS_WIN
    elif np.all(board != NO_PLAYER):  
        return GameState.IS_DRAW
    else:
        return GameState.STILL_PLAYING

def check_move_status(board: np.ndarray, column: Any) -> MoveStatus:

    try:
        column = int(float(column))
    except ValueError:
        return MoveStatus.WRONG_TYPE
    
    if not isinstance(column, int):
        return MoveStatus.NOT_INTEGER
    
    if not (0 <= column < BOARD_COLS):
        return MoveStatus.OUT_OF_BOUNDS
    
    if board[INDEX_HIGHEST_ROW, column] != NO_PLAYER:
        return MoveStatus.FULL_COLUMN
    
    return MoveStatus.IS_VALID
