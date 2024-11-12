# agents/agent_human_user/human_user.py

import numpy as np
from typing import Callable, Any
from game_utils import BoardPiece, PlayerAction, SavedState, MoveStatus, check_move_status

def query_user(prompt_function: Callable) -> Any:
    usr_input = prompt_function("Column? ")
    return usr_input

def convert_str_to_action(input_move_string: str) -> PlayerAction | None:
    """
    将用户输入的字符串转换为 PlayerAction 类型。
    """
    try:
        input_move = PlayerAction(int(input_move_string))
    except ValueError:
        print('Invalid move: Input must be an integer.')
        print('Try again.')
        return None
    return input_move

def user_move(board: np.ndarray, player: BoardPiece, saved_state: SavedState | None) -> tuple[PlayerAction, SavedState | None]:
    """
    获取用户的列选择并返回该操作。
    """
    move_status = None
    while move_status != MoveStatus.IS_VALID:
        input_move_string = query_user(input)
        input_move = convert_str_to_action(input_move_string)
        if input_move is None:
            continue
        move_status = check_move_status(board, input_move)
        if move_status != MoveStatus.IS_VALID:
            print(f'Move is invalid: {move_status.value}')
            print('Try again.')
    return input_move, saved_state
