

"""
This will hold some of the logic that will be used by the minimax and alpha-beta search agents.
Including the board matrix, piece-movement logic (available moves, capturing pieces, check-turn), alternating turns, 
win-conditions, offensive functions(agent focuses on moving forward and capturing opponent's pieces), 
and defensive functions(agent focuses on defending territory and preventing opponent from capturing pieces.)
"""

from logic import *


class AlphaBetaAgent:
    def __init__(self, boardmatrix, turn, depth, function, type=0):
        self.boardmatrix = boardmatrix
        self.turn = turn
        self.maxdepth = depth
        self.function = function
        self.type = type

        self.nodes = 0
        self.piece_num = 0

    def max_value(self, state, alpha, beta, depth):
        if depth == self.maxdepth or state.isgoalstate() != 0:
            return state.utility(self.turn)
        v = MINVAL
        actions = state.check_possible_actions()

        #if self.turn == 1:
        actions = sorted(state.check_possible_actions(), key=lambda action: self.orderaction(action, state), reverse=True)
        #else:
        #    actions = sorted(state.possible_actions(), key=lambda action: self.orderaction(action, state))

        for action in actions:
            self.nodes += 1

            v = max(v, self.min_value(state.transfer(action), alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(self, state, alpha, beta, depth):
        if depth == self.maxdepth or state.isgoalstate() != 0:
            return state.utility(self.turn)
        v = MAXVAL
        actions = state.check_possible_actions()

        #if self.turn == 1:
        actions = sorted(state.check_possible_actions(), key=lambda action: self.orderaction(action, state))
        #else:
        #    actions = sorted(state.check_possible_actions(), key=lambda action: self.orderaction(action, state), reverse=True)

        for action in actions:
            self.nodes += 1

            v = min(v, self.max_value(state.transfer(action), alpha, beta, depth + 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    def alpha_beta_decision(self):
        final_action = None
        if self.type == 0:
            initialstate = State(boardmatrix=self.boardmatrix, turn=self.turn, function=self.function)
        else:
            initialstate = State(boardmatrix=self.boardmatrix, turn=self.turn, function=self.function, height=5, width=10)
        v = MINVAL
        for action in initialstate.check_possible_actions():
            self.nodes += 1

            new_state = initialstate.transfer(action)
            if new_state.isgoalstate():
                final_action = action
                break
            minresult = self.min_value(new_state, MINVAL, MAXVAL, 1)
            if minresult > v:
                final_action = action
                v = minresult
        print(v)
        if self.turn == 1:
            self.piece_num = initialstate.transfer(final_action).white_num
        elif self.turn == 2:
            self.piece_num = initialstate.transfer(final_action).black_num
        print(final_action.getString())
        return initialstate.transfer(final_action), self.nodes, self.piece_num

    # order actions to make more pruning
    def orderaction(self, action, state):

        y = action.coordinate[0]
        x = action.coordinate[1]
        if action.turn == 1:
            if action.direction == 1:
                if (y - 1, x - 1) in state.white_positions:
                    return 2
            if action.direction == 2:
                if (y - 1, x) in state.white_positions:
                    return 2
            if action.direction == 2:
                if (y - 1, x + 1) in state.white_positions:
                    return 2

        elif action.turn == 2:
            if action.direction == 1:
                if (y + 1, x - 1) in state.black_positions:
                    return 2
            if action.direction == 2:
                if (y + 1, x) in state.black_positions:
                    return 2
            if action.direction == 2:
                if (y + 1, x + 1) in state.black_positions:
                    return 2
        return 1
            #if action.coordinate[]

        #print(self.turn)
        # return state.transfer(action).utility(self.turn)
        #if action.turn == 1:
        #    return max(state.get_farthest_piece(self.turn), action.coordinate[0] + 1)
        #elif action.turn == 2:
        #    return max(state.get_farthest_piece(self.turn), 7 - action.coordinate[0] + 1)
        return 0
