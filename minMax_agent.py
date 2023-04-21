
import numpy as np
from logic import *

"""
Gamefile for implementing the minimax search agent.
"""
#Class that defines MinMaxAgent agent that takes several parameters as input
class MinMaxAgent:
    def __init__(self, gameboard, turn, depth, function, type=0):
        self.gameboard = gameboard
        self.turn = turn
        self.maxdepth = depth
        self.function = function
        self.type = type
        self.nodes = 0
        self.piece_num = 0

#Maximizer function to find the maximum value found in the subtree at current state
    def maximizer(self, state, depth):
        if depth == self.maxdepth or state.isgoalstate() != 0:
            #If the depth is max or goal state return current state utility
            return state.utility(self.turn)
        v = MINVAL
        for action in state.available_actions():
            # Calculates the maximum value of child nodes by calling minimizer on all children
            v = max(v, self.minimizer(state.transfer(action), depth + 1))
            self.nodes += 1
        return v

#Minimizer function to find the minimum value found in the subtree at current state
    def minimizer(self, state, depth):
        if depth == self.maxdepth or state.isgoalstate() != 0:
            #If the depth is max or goal state return current state utility
            return state.utility(self.turn)
        v = MAXVAL
        for action in state.available_actions():
            # Calculates the minimum value of child nodes by calling maximizer on all children
            v = min(v, self.maximizer(state.transfer(action), depth + 1))
            self.nodes += 1

        return v

    def MinMaxAgent_decision(self):
        final_action = None
        if self.type == 0:
            start_state = State(gameboard=self.gameboard, turn=self.turn, function=self.function)
        else:
            start_state = State(gameboard=self.gameboard, turn=self.turn, function=self.function, height=5, width=10)
        v = MINVAL
        for action in start_state.available_actions():
            self.nodes += 1
            new_state = start_state.transfer(action)
            if new_state.isgoalstate():
                final_action = action
                break
            minresult = self.minimizer(new_state, 1)
            #If the game is over final_action set to current state
            if minresult > v:
                final_action = action
                v = minresult
        if self.turn == 1:
            self.piece_num = start_state.transfer(final_action).white_num
        elif self.turn == 2:
            self.piece_num = start_state.transfer(final_action).black_num
        print(final_action.getString())
        return start_state.transfer(final_action), self.nodes, self.piece_num
