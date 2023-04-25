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
gameboard = [['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],
             ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'],
             ['.', '.', '.', '.', '.', '.', '.', '.'],
             ['.', '.', '.', '.', '.', '.', '.', '.'],
             ['.', '.', '.', '.', '.', '.', '.', '.'],
             ['.', '.', '.', '.', '.', '.', '.', '.'],
             ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'],
             ['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w']]

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
def main():
    
    # Clock item to control how many times we loop per second
    clock = pygame.time.Clock()
    
    def redraw_window():
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

    run = True
    if run:
    
        redraw_window()
        draw_game_board()
        draw_pieces()
        # Update the window to display what has been drawn in the loop
        #pygame.display.update()
    
    while run:
      clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()


def draw_game_board():

    for y in range(0, len(gameboard)):
        for x in range(0, len(gameboard[0])):
            if (x+y) % 2 == 0:
                WIN.blit(LIGHT_BOARD_SQUARE, (x * GRID_SIZE, y * GRID_SIZE))
                pygame.draw.rect(WIN, WHITE, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
                
            else:
                WIN.blit(DARK_BOARD_SQUARE, (x * GRID_SIZE, y * GRID_SIZE))
                pygame.draw.rect(WIN, WHITE, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

    pygame.display.update()


def draw_pieces():

    for row in range(len(gameboard)):
        for col in range(len(gameboard[row])):
            if gameboard[row][col] == 'b':
                P1_rect.center = ((col*GRID_SIZE)+(GRID_SIZE/2), (row*GRID_SIZE)+(GRID_SIZE/2))
                gameboard[row][col] = WIN.blit(P1, P1_rect)
                

            elif gameboard[row][col] == 'w':
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
    if (self.boardmatrix[self.ori_x][self.ori_y] == 'b'
        and self.boardmatrix[self.new_x][self.new_y] != 'b'
        and self.new_x - self.ori_x == 'b'
        and self.ori_y - 1 <= self.new_y <= self.ori_y + 1
        and not (self.ori_y == self.new_y and self.boardmatrix[self.new_x][self.new_y] == 'w')) \
        or (self.boardmatrix[self.ori_x][self.ori_y] == 'w'
            and self.boardmatrix[self.new_x][self.new_y] != 'w'
            and self.ori_x - self.new_x == 'b'
            and self.ori_y - 1 <= self.new_y <= self.ori_y + 1
            and not (self.ori_y == self.new_y and self.boardmatrix[self.new_x][self.new_y] == 'b')):
        return 1
    return 0

def get_available_moves(self):
    #Returns a list of all possible moves for a given piece.
    possible_moves = []
    piece = self.boardmatrix[row][col]
    if piece == '.':
        return []

    player = piece.lower()

    # Check the direction of the piece based on the player
    if player == 'b':
        move_direction = -1
    else:
        move_direction = 1

    # Move one step forward
    if self.is_valid_move(row+move_direction, col) and self.gameboard[row+move_direction][col] == '.':
        possible_moves.append((row+move_direction, col))


    # Move diagonally (without capturing)
    if self.is_valid_move(row+move_direction, col+1) and self.gameboard[row+move_direction][col+1] == '.':
        possible_moves.append((row+move_direction, col+1))

    if self.is_valid_move(row+move_direction, col-1) and self.gameboard[row+move_direction][col-1] == '.':
        possible_moves.append((row+move_direction, col-1))

    return possible_moves


def check_win():
    pass


if __name__ == "__main__":
    main()
