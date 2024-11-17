import pytest
import numpy as np
from game_utils import (
    initialize_game_state,
    pretty_print_board,
    string_to_board,
    apply_player_action,
    connected_four,
    check_end_state,
    GameState,
    PLAYER1,
    PLAYER2,
    NO_PLAYER,
    check_move_status,
    MoveStatus,
)


def test_initialize_game_state():
    """测试棋盘初始化状态"""
    board = initialize_game_state()
    assert board.shape == (6, 7)  # 检查棋盘大小
    assert np.all(board == NO_PLAYER)  # 检查是否所有格子为空


def test_pretty_print_board():
    """测试棋盘字符串显示功能"""
    board = initialize_game_state()
    board[0, 0] = PLAYER1
    board[0, 1] = PLAYER2
    pretty = pretty_print_board(board)
    assert "X" in pretty  # 检查玩家1棋子的显示
    assert "O" in pretty  # 检查玩家2棋子的显示
    assert "|==============|" in pretty  # 检查边界显示


def test_string_to_board():
    """测试字符串到棋盘数组的转换"""
    board = initialize_game_state()
    board[0, 0] = PLAYER1
    board[0, 1] = PLAYER2
    board_str = pretty_print_board(board)
    converted_board = string_to_board(board_str)
    assert np.array_equal(board, converted_board)


def test_apply_player_action():
    """测试玩家动作的应用"""
    board = initialize_game_state()
    apply_player_action(board, 0, PLAYER1)
    assert board[0, 0] == PLAYER1  # 检查第0列第1行
    apply_player_action(board, 0, PLAYER2)
    assert board[1, 0] == PLAYER2  # 检查第0列第2行


def test_connected_four_horizontal():
    """测试横向连成四子"""
    board = initialize_game_state()
    for col in range(4):
        apply_player_action(board, col, PLAYER1)
    assert connected_four(board, PLAYER1)


def test_connected_four_vertical():
    """测试纵向连成四子"""
    board = initialize_game_state()
    for row in range(4):
        apply_player_action(board, 0, PLAYER1)
    assert connected_four(board, PLAYER1)


def test_connected_four_diagonal():
    """测试对角线连成四子"""
    board = initialize_game_state()
    for i in range(4):
        for j in range(i):
            apply_player_action(board, i, PLAYER2)  # 填充干扰棋子
        apply_player_action(board, i, PLAYER1)
    assert connected_four(board, PLAYER1)


def test_check_end_state_win():
    """测试胜利状态"""
    board = initialize_game_state()
    for col in range(4):
        apply_player_action(board, col, PLAYER1)
    assert check_end_state(board, PLAYER1) == GameState.IS_WIN


def test_check_end_state_draw():
    """测试平局状态"""
    board = initialize_game_state()
    for col in range(7):
        for row in range(6):
            board[row, col] = PLAYER1 if (row + col) % 2 == 0 else PLAYER2
    assert check_end_state(board, PLAYER1) == GameState.IS_DRAW
    assert check_end_state(board, PLAYER2) == GameState.IS_DRAW


def test_check_move_status():
    """测试动作是否合法"""
    board = initialize_game_state()
    assert check_move_status(board, 0) == MoveStatus.IS_VALID
    for row in range(6):
        apply_player_action(board, 0, PLAYER1)
    assert check_move_status(board, 0) == MoveStatus.FULL_COLUMN
    assert check_move_status(board, -1) == MoveStatus.OUT_OF_BOUNDS
    assert check_move_status(board, 7) == MoveStatus.OUT_OF_BOUNDS
    assert check_move_status(board, "abc") == MoveStatus.WRONG_TYPE
