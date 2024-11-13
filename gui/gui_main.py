import tkinter as tk
from tkinter import messagebox
from game_utils import initialize_game_state, apply_player_action, check_end_state, PLAYER1, PLAYER2, GameState
from agents.agent_random import generate_move_random

class Connect4GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect 4")

        # 初始化游戏状态
        self.board = initialize_game_state()
        self.current_player = PLAYER1

        # 创建每列的按钮
        self.buttons = [tk.Button(root, text=f"Drop in {i}", command=lambda i=i: self.drop_piece(i)) for i in range(7)]
        for i, button in enumerate(self.buttons):
            button.grid(row=0, column=i)

        # 创建棋盘标签
        self.labels = [[tk.Label(root, text=" ", width=4, height=2, relief="ridge", bg="white") for _ in range(7)] for _ in range(6)]
        for row in range(6):
            for col in range(7):
                self.labels[row][col].grid(row=row+1, column=col)

    def drop_piece(self, column):
        # 检查列是否可用
        if not self.is_valid_move(column):
            messagebox.showinfo("Invalid Move", "This column is full. Choose another column.")
            return

        # 玩家下棋
        apply_player_action(self.board, column, self.current_player)
        self.update_board()

        # 检查是否胜利或平局
        if self.check_game_end():
            return

        # 切换到电脑回合
        self.current_player = PLAYER2 if self.current_player == PLAYER1 else PLAYER1
        if self.current_player == PLAYER2:
            self.computer_move()

    def computer_move(self):
        # 使用随机代理生成电脑下棋动作
        action, _ = generate_move_random(self.board, PLAYER2, None)
        apply_player_action(self.board, action, PLAYER2)
        self.update_board()

        # 检查游戏状态
        if self.check_game_end():
            return

        # 切换回玩家
        self.current_player = PLAYER1

    def update_board(self):
        # 更新棋盘显示
        for row in range(6):
            for col in range(7):
                piece = self.board[row, col]
                color = "red" if piece == PLAYER1 else "yellow" if piece == PLAYER2 else "white"
                self.labels[row][col].config(bg=color)

    def is_valid_move(self, column):
        # 检查顶部行是否为空，若为空则表示该列可落子
        return self.board[0, column] == 0

    def check_game_end(self):
        # 使用 game_utils.py 中的 check_end_state 检查游戏状态
        end_state = check_end_state(self.board, self.current_player)
        if end_state == GameState.IS_WIN:
            messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
            self.reset_game()
            return True
        elif end_state == GameState.IS_DRAW:
            messagebox.showinfo("Game Over", "It's a draw!")
            self.reset_game()
            return True
        return False

    def reset_game(self):
        # 重置游戏状态
        self.board = initialize_game_state()
        self.current_player = PLAYER1
        self.update_board()

if __name__ == "__main__":
    root = tk.Tk()
    game = Connect4GUI(root)
    root.mainloop()
