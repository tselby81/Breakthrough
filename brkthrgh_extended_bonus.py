

"""
Game file if we want to create Breakthrough gamemode with extended ruleset for BONUS POINTS.
"""
Long Rectangular Board: For this variation, stick to the original, 1-worker-toenemy-base win criterion. Instead, change the board shape to an oblong
rectangle of dimensions 5x10.
"""

import pygame
# from pygame.locals import *
import sys, os, math
from minimax_agent import *
from model import *
from alpha_beta_agent import *
import time


class BreakthroughGame:
    def __init__(self):
        pygame.init()
        self.width, self.height = 1000, 400
        self.sizeofcell = int(800/10)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill([255, 255, 255])
        # chessboard and workers
        self.board = 0
        self.blackchess = 0
        self.whitechess = 0
        self.outline = 0
        self.reset = 0
        self.winner = 0
        self.computer = None

        # status 0: origin;  1: ready to move; 2: end
        # turn 1: black 2: white
        self.status = 0
        self.turn = 1
        # Variable for moving
        self.ori_x = 0
        self.ori_y = 0
        self.new_x = 0
        self.new_y = 0

        # matrix for position of chess, 0 - empty, 1 - black, 2 - white
        self.boardmatrix = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]]

        self.total_nodes_1 = 0
        self.total_nodes_2 = 0
        self.total_time_1 = 0
        self.total_time_2 = 0
        self.total_step_1 = 0
        self.total_step_2 = 0
        self.eat_piece = 0

        # Caption
        pygame.display.set_caption("Breakthrough!")

        # initialize pygame clock
        self.clock = pygame.time.Clock()
        self.initgraphics()

    def run(self):
        self.clock.tick(60)

        # clear the screen
        self.screen.fill([255, 255, 255])

        # display the board and chess

        if self.status == 5:
            # Black
            if self.turn == 1:
                start = time.clock()
                self.ai_move(2, 6, 9)
                self.total_time_1 += (time.clock() - start)
                self.total_step_1 += 1
                print('total_step_1 = ', self.total_step_1,
                      'total_nodes_1 = ', self.total_nodes_1,
                      'node_per_move_1 = ', self.total_nodes_1 / self.total_step_1,
                      'time_per_move_1 = ', self.total_time_1 / self.total_step_1,
                      'have_eaten = ', self.eat_piece)
            elif self.turn == 2:
                start = time.clock()
                self.ai_move(2, 5, 9)
                self.total_time_2 += (time.clock() - start)
                self.total_step_2 += 1
                print('total_step_2 = ', self.total_step_2,
                      'total_nodes_2 = ', self.total_nodes_2,
                      'node_per_move_2 = ', self.total_nodes_2 / self.total_step_2,
                      'time_per_move_2 = ', self.total_time_2 / self.total_step_2,
                      'have_eaten: ', self.eat_piece)
        # Events accepting
        for event in pygame.event.get():
            # Quit if close the windows
            if event.type == pygame.QUIT:
                exit()
            # reset button pressed
            elif event.type == pygame.MOUSEBUTTONDOWN and self.isreset(event.pos):
                self.boardmatrix = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                                    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2]]
                self.turn = 1
                self.status = 0
            # computer button pressed
            elif event.type == pygame.MOUSEBUTTONDOWN and self.iscomputer(event.pos):
                self.ai_move_alphabeta(1, 9)
                # self.ai_move_minimax()

            elif event.type == pygame.MOUSEBUTTONDOWN and self.isauto(event.pos):
                self.status = 5

            # ====================================================================================
            # select chess
            elif event.type == pygame.MOUSEBUTTONDOWN and self.status == 0:
                x, y = event.pos
                coor_y = math.floor(x / self.sizeofcell)
                coor_x = math.floor(y / self.sizeofcell)
                if self.boardmatrix[coor_x][coor_y] == self.turn:
                    self.status = 1
                    self.ori_y = math.floor(x / self.sizeofcell)
                    self.ori_x = math.floor(y / self.sizeofcell)
            # check whether the selected chess can move, otherwise select other chess
            elif event.type == pygame.MOUSEBUTTONDOWN and self.status == 1:
                x, y = event.pos
                self.new_y = math.floor(x / self.sizeofcell)
                self.new_x = math.floor(y / self.sizeofcell)
                if self.isabletomove():
                    self.movechess()
                    if (self.new_x == 4 and self.boardmatrix[self.new_x][self.new_y] == 1) \
                        or (self.new_x == 0 and self.boardmatrix[self.new_x][self.new_y] == 2):
                        self.status = 3
                elif self.boardmatrix[self.new_x][self.new_y] == self.boardmatrix[self.ori_x][self.ori_y]:
                    self.ori_x = self.new_x
                    self.ori_y = self.new_y
        self.display()
        # update the screen
        pygame.display.flip()
        
++++++++++++++++++++++++++ working on
