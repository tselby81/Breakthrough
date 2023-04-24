
from model import *

class Alpha_Beta_Agent:
    def __init__(self, board_matrix: List[List[int]], turn: int, depth: int, function, type=0):
        self.board_matrix = board_matrix
        self.turn = turn
        self.max_depth = depth
        self.function = function
        self.type = type
        self.nodes = 0
        self.piece_num = 0

    def max_value(self, state: 'State', alpha: int, beta: int, depth: int) -> int:
        if depth == self.max_depth or state.is_goal_state() != 0:
            return state.utility(self.turn)

        v = float('-inf')
        actions = state.available_actions()
        sorted_actions = self.sort_actions(actions, state)

        for action in sorted_actions:
            self.nodes += 1
            v = max(v, self.min_value(state.transfer(action), alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)

        return v

    def min_value(self, state: 'State', alpha: int, beta: int, depth: int) -> int:
        if depth == self.max_depth or state.is_goal_state() != 0:
            return state.utility(self.turn)

        v = float('inf')
        actions = state.available_actions()
        sorted_actions = self.sort_actions(actions, state)

        for action in sorted_actions:
            self.nodes += 1
            v = min(v, self.max_value(state.transfer(action), alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)

        return v

    def alpha_beta_decision(self) -> Tuple['State', int, int]:
        if self.type == 0:
            initial_state = State(board_matrix=self.board_matrix, turn=self.turn, function=self.function)
        else:
            initial_state = State(board_matrix=self.board_matrix, turn=self.turn, function=self.function, height=5, width=10)

        v = float('-inf')
        final_action = None
        for depth in range(1, self.max_depth + 1):
            for action in initial_state.available_actions():
                self.nodes += 1
                new_state = initial_state.transfer(action)
                if new_state.is_goal_state():
                    final_action = action
                    break
                min_result = self.min_value(new_state, float('-inf'), float('inf'), 1)
                if min_result > v:
                    final_action = action
                    v = min_result
            if final_action is not None:
                break

        if self.turn == 1:
            self.piece_num = initial_state.transfer(final_action).white_num
        elif self.turn == 2:
            self.piece_num = initial_state
        return initial_state.transfer(final_action), self.nodes, self.piece_num

    def sort_actions(self, actions: List['Action'], state: 'State') -> List['Action']:
        sorted_actions = sorted(actions, key=lambda action: self.action_score(action, state), reverse=True)
        return sorted_actions

    def action_score(self, action: 'Action', state: 'State') -> int:
        score = state.transfer(action).utility(self.turn)
        return score
