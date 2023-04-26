from numpy import row_stack
import pygame
import sys, os, math
import time
from miniMax_agent import *
from alpha_beta_agent import *
from logic import *
pygame.font.init()

"""
Main file which runs the game.
Draws the various game elements.
Main game loop which calls the various functions and updates the window.
Get
""" 

# Matrix to define the starting gameboard
# '.' - Empty, 'b' - black piece, 'w' - white piece
gameboard = []
gameboard = [[1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [2, 2, 2, 2, 2, 2, 2, 2],
            [2, 2, 2, 2, 2, 2, 2, 2]]

FPS = 1

GRID_SIZE = 75

WIN_HEIGHT = len(gameboard)*GRID_SIZE
WIN_WIDTH = (len(gameboard[0])*GRID_SIZE) + (GRID_SIZE*4)

# CREATE A DISPLAY SURFACE
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Breakthrough Galactic!")

# COLORS TO BE USED TEMPORARILY
# BOARD SQUARES AND PIECE COLORS WILL BE REPLACED WITH IMAGES
WHITE = (255, 255, 255)         # White pieces
BLACK = (0, 0, 0)               # Black pieces

# LOAD IMAGES
moon = pygame.image.load(os.path.join('assets', 'Moon.jpg'))

DARK_BOARD_SQUARE = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'SpaceDark.png')), (GRID_SIZE, GRID_SIZE))
DARK_BOARD_SQUARE.convert()
DARK_BOARD_SQUARE_rect = DARK_BOARD_SQUARE.get_rect()
LIGHT_BOARD_SQUARE = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'SpaceLight.png')), (GRID_SIZE, GRID_SIZE))
LIGHT_BOARD_SQUARE.convert()
LIGHT_BOARD_SQUARE_rect = LIGHT_BOARD_SQUARE.get_rect()

RESET_BTN = None
RESET_BTN_rect = None
AI_MOVE_BTN = None
AI_MOVE_BTN_rect = None
AUTOPLAY_BTN = None
AUTOPLAY_BTN_rect = None

PLAYER1 = pygame.image.load(os.path.join('assets', 'alien1.png'))
P1 = pygame.transform.scale(PLAYER1, (60, 60)).convert_alpha()
P1_rect = P1.get_rect()
PLAYER2 = pygame.image.load(os.path.join('assets', 'alien2.png'))
P2 = pygame.transform.scale(PLAYER2, (60, 60)).convert_alpha()
P2_rect = P2.get_rect()

WINNER_P1 = None
WINNER_P1_rect = None
WINNER_P2 = None
WINNER_P2_rect = None

# FONTS
PIXEL_FONT = pygame.font.Font(os.path.join('assets', 'pixelfont.ttf'), 20)


"""
Main Game Loop.
This should hold things related to game logic.
Other specialized functions should be written outside and called in the game loop when needed
"""
class BreakthroughG:
    def __init__(self):
        pygame.init()
        self.width, self.height = (len(gameboard[0])*GRID_SIZE + GRID_SIZE*4), len(gameboard)*GRID_SIZE
        self.sizeofcell = int(560/8)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill([255, 255, 255])
        # gameboard and pieces
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

        self.gameboard = [[1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [2, 2, 2, 2, 2, 2, 2, 2],
                            [2, 2, 2, 2, 2, 2, 2, 2]]

        self.total_nodes_1 = 0
        self.total_nodes_2 = 0
        self.total_time_1 = 0
        self.total_time_2 = 0
        self.total_step_1 = 0
        self.total_step_2 = 0
        self.eat_piece = 0
        self.redraw_window()
        self.draw_game_board()
        self.draw_pieces()

    def draw_game_board(self):

        for y in range(0, len(gameboard)):
            for x in range(0, len(gameboard[0])):
                if (x+y) % 2 == 0:
                    WIN.blit(LIGHT_BOARD_SQUARE, (x * GRID_SIZE, y * GRID_SIZE))
                    pygame.draw.rect(WIN, WHITE, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
                    
                else:
                    WIN.blit(DARK_BOARD_SQUARE, (x * GRID_SIZE, y * GRID_SIZE))
                    pygame.draw.rect(WIN, WHITE, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

        pygame.display.update()


    def draw_pieces(self):

        for row in range(len(gameboard)):
            for col in range(len(gameboard[row])):
                if gameboard[row][col] == 1:
                    P1_rect.center = ((col*GRID_SIZE)+(GRID_SIZE/2), (row*GRID_SIZE)+(GRID_SIZE/2))
                    gameboard[row][col] = WIN.blit(P1, P1_rect)
                    

                elif gameboard[row][col] == 2:
                    P2_rect.center = ((col*GRID_SIZE)+(GRID_SIZE/2), (row*GRID_SIZE)+(GRID_SIZE/2))
                    gameboard[row][col] = WIN.blit(P2, P2_rect)

        pygame.display.update()


    def player_turn():
        pass


    def click_piece():
        mouse_pos = pygame.mouse.get_pos()
        if P1_rect.collidepoint(mouse_pos):
            pygame.mouse.get_pressed()
            # HIGHLIGHT THE P1 PIECE IN YELLOW SQUARE
        elif P2_rect.collidepoint(mouse_pos):
            pygame.mouse.get_pressed()
            # HIGHLIGHT THE P2 PIECE IN YELLOW SQUARE


    def check_collision():
        pass

    def is_valid_move(self):
        if (self.gameboard[self.ori_x][self.ori_y] == 1
            and self.gameboard[self.new_x][self.new_y] != 1
            and self.new_x - self.ori_x == 1
            and self.ori_y - 1 <= self.new_y <= self.ori_y + 1
            and not (self.ori_y == self.new_y and self.gameboard[self.new_x][self.new_y] == 2)) \
            or (self.gameboard[self.ori_x][self.ori_y] == 2
                and self.gameboard[self.new_x][self.new_y] != 2
                and self.ori_x - self.new_x == 1
                and self.ori_y - 1 <= self.new_y <= self.ori_y + 1
                and not (self.ori_y == self.new_y and self.gameboard[self.new_x][self.new_y] == 1)):
            return 1
        return 0

    def get_available_moves(self):
        #Returns a list of all possible moves for a given piece.
        possible_moves = []
        piece = self.gameboard[self.row][self.col]
        if piece == 0:
            return []

        player = piece()

        # Check the direction of the piece based on the player
        if player == 1:
            move_direction = -1
        else:
            move_direction = 1

        # Move one step forward
        if self.is_valid_move(self.row+move_direction, self.col) and self.gameboard[self.row+move_direction][self.col] == 0:
            possible_moves.append((self.row+move_direction, self.col))


        # Move diagonally
        if player == 1:
            if self.is_valid_move(self.row+move_direction, self.col+1) and self.gameboard[self.row+move_direction][self.col+1] == 0 or self.is_valid_move(self.row+move_direction, self.col-1) and self.gameboard[self.row+move_direction][self.col+1] == 2:
                possible_moves.append((self.row+move_direction, self.col+1))

            if self.is_valid_move(self.row+move_direction, self.col-1) and self.gameboard[self.row+move_direction][self.col-1] == 0 or self.is_valid_move(self.row+move_direction, self.col-1) and self.gameboard[self.row+move_direction][self.col-1] == 2:
                possible_moves.append((self.row+move_direction, self.col-1))
        else:
            if self.is_valid_move(self.row+move_direction, self.col+1) and self.gameboard[self.row+move_direction][self.col+1] == 0 or self.is_valid_move(self.row+move_direction, self.col-1) and self.gameboard[self.row+move_direction][self.col+1] == 1:
                possible_moves.append((self.row+move_direction, self.col+1))

            if self.is_valid_move(self.row+move_direction, self.col-1) and self.gameboard[self.row+move_direction][self.col-1] == 0 or self.is_valid_move(self.row+move_direction, self.col-1) and self.gameboard[self.row+move_direction][self.col-1] == 1:
                possible_moves.append((self.row+move_direction, self.col-1))
        
        return possible_moves

    def move_piece(self):
        self.gameboard[self.new_x][self.new_y] = self.gameboard[self.ori_x][self.ori_y]
        self.gameboard[self.ori_x][self.ori_y] = 0
        if self.turn == 1:
            self.turn = 2
        elif self.turn == 2:
            self.turn = 1
        self.status = 0
    
    def movechess(self):
        self.gameboard[self.new_x][self.new_y] = self.gameboard[self.ori_x][self.ori_y]
        self.gameboard[self.ori_x][self.ori_y] = 0
        if self.turn == 1:
            self.turn = 2
        elif self.turn == 2:
            self.turn = 1
        self.status = 0

    def isreset(self, pos):
        x, y = pos
        if 670 >= x >= 590 and 50 <= y <= 130:
            return True
        return False

    def iscomputer(self, pos):
        x, y = pos
        if 590 <= x <= 670 and 200 <= y <= 280:
            return True
        return False

    def isauto(self, pos):
        x, y = pos
        if 590 <= x <= 670 and 340 <= y <= 420:
            return True
        return False

    def isabletomove(self):
        if (self.gameboard[self.ori_x][self.ori_y] == 1
            and self.gameboard[self.new_x][self.new_y] != 1
            and self.new_x - self.ori_x == 1
            and self.ori_y - 1 <= self.new_y <= self.ori_y + 1
            and not (self.ori_y == self.new_y and self.gameboard[self.new_x][self.new_y] == 2)) \
            or (self.gameboard[self.ori_x][self.ori_y] == 2
                and self.gameboard[self.new_x][self.new_y] != 2
                and self.ori_x - self.new_x == 1
                and self.ori_y - 1 <= self.new_y <= self.ori_y + 1
                and not (self.ori_y == self.new_y and self.gameboard[self.new_x][self.new_y] == 1)):
            return 1
        return 0

    def ai_move(self, searchtype, evaluation):
        if searchtype == 1:
            return self.ai_move_minimax(evaluation)
        elif searchtype == 2:
            return self.ai_move_alphabeta(evaluation)

    def ai_move_minimax(self, function_type):
        board, nodes, piece = MinMaxAgent(self.gameboard, self.turn, 3, function_type).minimax_decision()
        self.gameboard = board.getMatrix()
        if self.turn == 1:
            self.total_nodes_1 += nodes
            self.turn = 2
        elif self.turn == 2:
            self.total_nodes_2 += nodes
            self.turn = 1
        self.eat_piece = 16 - piece
        if self.isgoalstate():
            self.status = 3
            #print(self.gameboard)

    def ai_move_alphabeta(self, function_type):
        board, nodes, piece = AlphaBetaAgent(self.gameboard, self.turn, 5, function_type).alpha_beta_decision()
        self.gameboard = board.getMatrix()
        if self.turn == 1:
            self.total_nodes_1 += nodes
            self.turn = 2
        elif self.turn == 2:
            self.total_nodes_2 += nodes
            self.turn = 1
        self.eat_piece = 16 - piece
        if self.isgoalstate():
            self.status = 3

    def check_win(self, base=0):
        if base == 0:
            if 2 in self.gameboard[0] or 1 in self.gameboard[7]:
                return True
            else:
                for line in self.gameboard:
                    if 1 in line or 2 in line:
                        return False
            return True
        else:
            count = 0
            for i in self.gameboard[0]:
                if i == 2:
                    count += 1
            if count == 3:
                return True
            count = 0
            for i in self.gameboard[7]:
                if i == 1:
                    count += 1
            if count == 3:
                return True
            count1 = 0
            count2 = 0
            for line in self.gameboard:
                for i in line:
                    if i == 1:
                        count1 += 1
                    elif i == 2:
                        count2 += 1
            if count1 <= 2 or count2 <= 2:
                return True
        return False
    
    def run(self):
        self.clock.tick(60)

        # clear the screen
        self.screen.fill([255, 255, 255])


        if self.status == 5:
            # Black
            if self.turn == 1:
                start = time.process_time()
                self.ai_move(2, 2)
                self.total_time_1 += (time.process_time() - start)
                self.total_step_1 += 1
                print('total_step_1 = ', self.total_step_1,
                      'total_nodes_1 = ', self.total_nodes_1,
                      'node_per_move_1 = ', self.total_nodes_1 / self.total_step_1,
                      'time_per_move_1 = ', self.total_time_1 / self.total_step_1,
                      'have_eaten = ', self.eat_piece)
            elif self.turn == 2:
                start = time.process_time()
                self.ai_move(2, 2)
                self.total_time_2 += (time.process_time() - start)
                self.total_step_2 += 1
                print('total_step_2 = ', self.total_step_2,
                      'total_nodes_2 = ', self.total_nodes_2,
                      'node_per_move_2 = ', self.total_nodes_2 / self.total_step_2,
                      'time_per_move_2 = ', self.total_time_2 / self.total_step_2,
                      'have_eaten: ', self.eat_piece)

    def redraw_window(self):
        WIN.fill(BLACK)
        moon_size = ((WIN.get_width()), (WIN.get_height()))
        MOON = pygame.transform.scale(moon, moon_size)
        MOON.convert()
        WIN.blit(MOON, (0, 0))

        # DRAW TEXT LABELS FOR "RESET", "AI MOVE", AND "AUTO PLAY" BUTTONS
        reset = PIXEL_FONT.render(f"Reset Board", 1, WHITE)
        reset_rect = reset.get_rect()
        reset_rect.center = ((WIN.get_width()) - (reset.get_width())*.85, (WIN.get_height()*.33)-35)
        ai_move = PIXEL_FONT.render(f"Computer Move", 1, WHITE)
        ai_move_rect = ai_move.get_rect()
        ai_move_rect.center = ((WIN.get_width()) - (reset.get_width())*.85, (WIN.get_height()*.66)-35)
        auto_play = PIXEL_FONT.render(f"Simulate Game", 1, WHITE)
        auto_play_rect = auto_play.get_rect()
        auto_play_rect.center = ((WIN.get_width()) - (reset.get_width())*.85, (WIN.get_height()*.99)-35)

        WIN.blit(reset, reset_rect)
        WIN.blit(ai_move, ai_move_rect)
        WIN.blit(auto_play, auto_play_rect)

        pygame.display.update()

def main():
    
    # Clock item to control how many times we loop per second
    clock = pygame.time.Clock()
        
    run = True
    if run:
        game = BreakthroughG()
        #game.redraw_window()
        #game.draw_game_board()
        #game.draw_pieces()
        # Update the window to display what has been drawn in the loop
        #pygame.display.update()
    
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # reset button pressed
            elif event.type == pygame.MOUSEBUTTONDOWN and game.isreset(event.pos):
                game.gameboard = [[1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [2, 2, 2, 2, 2, 2, 2, 2],
                            [2, 2, 2, 2, 2, 2, 2, 2]]
                game.turn = 1
                game.status = 0
             # computer button pressed
            elif event.type == pygame.MOUSEBUTTONDOWN and game.iscomputer(event.pos):
                game.ai_move_alphabeta(1)
                # self.ai_move_minimax()

            elif event.type == pygame.MOUSEBUTTONDOWN and game.isauto(event.pos):
                game.status = 5

            # ====================================================================================
            # select chess
            elif event.type == pygame.MOUSEBUTTONDOWN and game.status == 0:
                x, y = event.pos
                coor_y = math.floor(x / game.sizeofcell)
                coor_x = math.floor(y / game.sizeofcell)
                if game.gameboard[coor_x][coor_y] == game.turn:
                    game.status = 1
                    game.ori_y = math.floor(x / game.sizeofcell)
                    game.ori_x = math.floor(y / game.sizeofcell)
            # check whether the selected chess can move, otherwise select other chess
            elif event.type == pygame.MOUSEBUTTONDOWN and game.status == 1:
                x, y = event.pos
                game.new_y = math.floor(x / game.sizeofcell)
                game.new_x = math.floor(y / game.sizeofcell)
                if game.is_valid_move():
                    game.movechess()
                    if (game.new_x == 7 and game.gameboard[game.new_x][game.new_y] == 1) \
                        or (game.new_x == 0 and game.gameboard[game.new_x][game.new_y] == 2):
                        game.status = 3
                elif game.gameboard[game.new_x][game.new_y] == game.gameboard[game.ori_x][game.ori_y]:
                    game.ori_x = game.new_x
                    game.ori_y = game.new_y
                    # display the board and chess
        #game.draw_game_board()
        #game.draw_pieces()
        # update the screen
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()
