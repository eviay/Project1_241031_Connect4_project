# agents/agent_random/random.py

import numpy as np
from game_utils import BoardPiece, PlayerAction, SavedState, MoveStatus, check_move_status

def generate_move_random(
    board: np.ndarray, player: BoardPiece, saved_state: SavedState | None
) -> tuple[PlayerAction, SavedState | None]:
    """
    随机选择一个有效的非满列，并返回它作为下一步的动作。
    
    参数:
        board (np.ndarray): 当前棋盘状态。
        player (BoardPiece): 当前玩家的标识（PLAYER1 或 PLAYER2）。
        saved_state (SavedState | None): 用于保存代理状态（随机代理不使用此参数）。

    返回:
        tuple[PlayerAction, SavedState | None]: 返回一个包含所选列和保存状态的元组。
    """
    valid_columns = [col for col in range(board.shape[1]) 
                     if check_move_status(board, col) == MoveStatus.IS_VALID]
    if valid_columns:
        action = np.random.choice(valid_columns)  # 随机选择一个有效的列
        return action, saved_state
    else:
        raise ValueError("No valid moves available")
