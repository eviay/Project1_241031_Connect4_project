import sys
from game_utils import PLAYER1, PLAYER2, PLAYER1_PRINT, PLAYER2_PRINT, GameState, MoveStatus, GenMove
from game_utils import initialize_game_state, pretty_print_board, apply_player_action, check_end_state, check_move_status
from agents.agent_human_user import user_move
from agents.agent_random import generate_move_random as random_move

try:
    # 尝试导入 GUI 代码
    from gui.gui_main import Connect4GUI
    import tkinter as tk
except ImportError:
    Connect4GUI = None

def human_vs_agent(
    generate_move_1: GenMove,
    generate_move_2: GenMove = user_move,
    player_1: str = "Player 1",
    player_2: str = "Player 2",
):
    """CLI模式下的游戏主循环"""
    players = (PLAYER1, PLAYER2)
    saved_state = {PLAYER1: None, PLAYER2: None}
    board = initialize_game_state()
    gen_moves = (generate_move_1, generate_move_2)
    player_names = (player_1, player_2)

    playing = True
    while playing:
        for player, player_name, gen_move in zip(players, player_names, gen_moves):
            print(pretty_print_board(board))
            print(f'{player_name}, you are playing with {PLAYER1_PRINT if player == PLAYER1 else PLAYER2_PRINT}')
            
            # 获取玩家的动作
            action, saved_state[player] = gen_move(board.copy(), player, saved_state[player])

            # 检查动作是否合法
            move_status = check_move_status(board, action)
            if move_status != MoveStatus.IS_VALID:
                print(f'Move {action} is invalid: {move_status.value}')
                print(f'{player_name} lost by making an illegal move.')
                playing = False
                break

            # 应用玩家的动作
            apply_player_action(board, action, player)

            # 检查游戏状态
            end_state = check_end_state(board, player)
            if end_state == GameState.IS_WIN:
                print(pretty_print_board(board))
                print(f'{player_name} wins as {PLAYER1_PRINT if player == PLAYER1 else PLAYER2_PRINT}!')
                playing = False
                break
            elif end_state == GameState.IS_DRAW:
                print(pretty_print_board(board))
                print('Game ended in a draw.')
                playing = False
                break

def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'gui' and Connect4GUI:
        print("Running in GUI mode")  # 输出确认信息
        root = tk.Tk()
        game = Connect4GUI(root)
        root.mainloop()
    else:
        print("Running in CLI mode. Use 'gui' argument to run with GUI.")
        human_vs_agent(random_move, user_move)

if __name__ == "__main__":
    main()
