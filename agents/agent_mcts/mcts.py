import math
import numpy as np
from typing import Optional, List, Tuple
from game_utils import apply_player_action, check_end_state, connected_four, GameState, PlayerAction, BoardPiece, NO_PLAYER, SavedState

UCT_CONSTANT = 1.41
MCTS_SIMULATIONS = 1000

class GameStateNode:
    def __init__(self, board: np.ndarray, last_action: Optional[PlayerAction] = None):
        self.board = board
        self.last_action = last_action

class Node:
    def __init__(self, state: GameStateNode, parent=None):
        self.state = state
        self.parent = parent
        self.children: List[Node] = []
        self.visits = 0
        self.wins = 0

def expand(node: Node, player: BoardPiece):
    valid_moves = [col for col in range(node.state.board.shape[1]) if np.any(node.state.board[:, col] == NO_PLAYER)]
    if not valid_moves:
        return
    for move in valid_moves:
        new_board = node.state.board.copy()
        apply_player_action(new_board, move, player)
        child_state = GameStateNode(board=new_board, last_action=move)
        child_node = Node(state=child_state, parent=node)
        node.children.append(child_node)

def best_uct(node: Node):
    if not node.children:
        raise ValueError("No children nodes found in UCT calculation.")
    
    def uct_value(child: Node):
        if child.visits == 0:
            return float("inf")
        exploitation = child.wins / child.visits
        exploration = math.sqrt(math.log(node.visits) / child.visits)
        return exploitation + UCT_CONSTANT * exploration
    
    return max(node.children, key=uct_value)

def simulate(node: Node, player: BoardPiece) -> int:
    current_board = node.state.board.copy()
    current_player = player

    while True:
        valid_moves = [col for col in range(current_board.shape[1]) if np.any(current_board[:, col] == NO_PLAYER)]
        if not valid_moves:
            return 0

        for move in valid_moves:
            temp_board = current_board.copy()
            apply_player_action(temp_board, move, BoardPiece(3 - current_player))
            if connected_four(temp_board, BoardPiece(3 - current_player)):
                return -1  
        for move in valid_moves:
            temp_board = current_board.copy()
            apply_player_action(temp_board, move, current_player)
            if connected_four(temp_board, current_player):
                return 1

        move = np.random.choice(valid_moves)
        apply_player_action(current_board, move, current_player)

        if connected_four(current_board, current_player):
            return 1 if current_player == player else -1

        current_player = BoardPiece(3 - current_player)

def backpropagate(node: Node, result: int):
    while node is not None:
        node.visits += 1
        node.wins += result
        result = -result
        node = node.parent

def mcts_search(root: Node, player: BoardPiece, simulations: int) -> Optional[Node]:
    for _ in range(simulations):
        node = root

        while node.children:
            node = best_uct(node)
        
        if check_end_state(node.state.board, player) != GameState.IS_WIN:
            expand(node, player)

        if node.children:
            node = np.random.choice(node.children)
            result = simulate(node, player)
        else:
            result = 0

        backpropagate(node, result)

    return max(root.children, key=lambda child: child.visits, default=None)

def generate_move_mcts(
    board: np.ndarray, player: BoardPiece, saved_state: Optional["SavedState"]
) -> tuple[PlayerAction, Optional["SavedState"]]:
    valid_moves = [col for col in range(board.shape[1]) if np.any(board[:, col] == NO_PLAYER)]
    if not valid_moves:
        raise ValueError("No valid moves available! The board might be full.")
    
    root = Node(state=GameStateNode(board=board))
    best_node = mcts_search(root, player, simulations=MCTS_SIMULATIONS)

    if not best_node or best_node.state.last_action is None:
        raise ValueError("No valid moves available after MCTS!")
    
    return PlayerAction(best_node.state.last_action), saved_state
