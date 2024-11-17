import numpy as np
from typing import Optional
from game_utils import (
    BoardPiece, PlayerAction, SavedState, GameState, 
    NO_PLAYER, apply_player_action, check_end_state
)

MAX_DEPTH = 4  # 搜索深度

def evaluate_board(board: np.ndarray, player: BoardPiece) -> int:
    """
    启发式评估函数，用于评估棋盘状态对指定玩家的有利程度。
    这里的评分策略较为简单，可以根据需求进一步优化。
    """
    opponent = BoardPiece(3 - player)
    player_score = np.sum(board == player)
    opponent_score = np.sum(board == opponent)
    return player_score - opponent_score

def minimax(
    board: np.ndarray,
    depth: int,
    maximizing: bool,
    player: BoardPiece,
    alpha: float,
    beta: float
) -> tuple[float, Optional[PlayerAction]]:
    """
    Minimax 算法实现，包含 Alpha-Beta 剪枝。

    Args:
        board (np.ndarray): 当前棋盘状态。
        depth (int): 剩余搜索深度。
        maximizing (bool): 当前是否为极大化玩家回合。
        player (BoardPiece): 当前搜索的玩家。
        alpha (float): Alpha 剪枝值。
        beta (float): Beta 剪枝值。

    Returns:
        tuple[float, Optional[PlayerAction]]: (最佳评分, 最佳动作)
    """
    opponent = BoardPiece(3 - player)
    valid_moves = [col for col in range(board.shape[1]) if board[0, col] == NO_PLAYER]

    # 检查是否达到终止条件
    if depth == 0 or not valid_moves:
        return evaluate_board(board, player), None

    best_action = None
    if maximizing:
        max_eval = -float("inf")
        for action in valid_moves:
            new_board = board.copy()
            apply_player_action(new_board, action, player)

            # 检查是否直接获胜
            if check_end_state(new_board, player) == GameState.IS_WIN:
                return float("inf"), action

            # 递归调用 Minimax
            eval_score, _ = minimax(new_board, depth - 1, False, player, alpha, beta)
            if eval_score > max_eval:
                max_eval = eval_score
                best_action = action

            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
        return max_eval, best_action
    else:
        min_eval = float("inf")
        for action in valid_moves:
            new_board = board.copy()
            apply_player_action(new_board, action, opponent)

            # 检查是否直接获胜
            if check_end_state(new_board, opponent) == GameState.IS_WIN:
                return -float("inf"), action

            # 递归调用 Minimax
            eval_score, _ = minimax(new_board, depth - 1, True, player, alpha, beta)
            if eval_score < min_eval:
                min_eval = eval_score
                best_action = action

            beta = min(beta, eval_score)
            if beta <= alpha:
                break
        return min_eval, best_action

def generate_move_minimax(
    board: np.ndarray, player: BoardPiece, saved_state: Optional[SavedState]
) -> tuple[PlayerAction, Optional[SavedState]]:
    """
    Minimax 算法的封装函数，用于生成玩家的最佳动作。

    Args:
        board (np.ndarray): 当前棋盘状态。
        player (BoardPiece): 当前玩家。
        saved_state (Optional[SavedState]): 可选的保存状态。

    Returns:
        tuple[PlayerAction, Optional[SavedState]]: (最佳动作, 保存状态)
    """
    _, best_action = minimax(board, MAX_DEPTH, True, player, -float("inf"), float("inf"))
    if best_action is None:
        raise ValueError("No valid moves available!")
    return PlayerAction(best_action), saved_state
