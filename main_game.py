import pygame
import sys, os, math
import time
from miniMax_agent import *
from alpha_beta_agent import *
from logic import *

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

FPS = 10

# CREATE THE MAIN GAME WINDOW
GRID_SIZE = 75

WIN_HEIGHT = len(gameboard)*GRID_SIZE
WIN_WIDTH = (len(gameboard[0])*GRID_SIZE) + (GRID_SIZE*2)


WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Breakthrough")


# COLORS TO BE USED TEMPORARILY
# BOARD SQUARES AND PIECE COLORS WILL BE REPLACED WITH IMAGES
LIGHT_PURPLE = (199, 164, 222)  # Light squares
PURPLISH_BLACK = (14, 11, 15)   # Dark squares
WHITE = (255, 255, 255)         # White pieces
BLACK = (0, 0, 0)               # Black pieces

# Images
DARK_BOARD_SQUARE = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'SpaceDark.png')), (GRID_SIZE, GRID_SIZE))
LIGHT_BOARD_SQUARE = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'SpaceLight.png')), (GRID_SIZE, GRID_SIZE))


def draw_game_board(surface):

    for y in range(0, int(WIN_HEIGHT + GRID_SIZE*4)):
        for x in range(0, int(WIN_WIDTH + GRID_SIZE*4)):
            if (x+y) % 2 == 0:
                # r = pygame.Rect((x * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                # pygame.draw.rect(surface, pygame.Color(LIGHT_PURPLE), r)
                WIN.blit(LIGHT_BOARD_SQUARE, (x * GRID_SIZE, y * GRID_SIZE))
                pygame.draw.rect(WIN, WHITE, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
                
            else:
                # r = pygame.Rect((x * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                # pygame.draw.rect(surface, pygame.Color(PURPLISH_BLACK), r)
                WIN.blit(DARK_BOARD_SQUARE, (x * GRID_SIZE, y * GRID_SIZE))
                pygame.draw.rect(WIN, WHITE, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)


def draw_pieces():
    WIN.fill("lightslategrey")

    draw_game_board(WIN)

    for row in range(len(gameboard)):
        for col in range(len(gameboard[row])):
            if gameboard[row][col] == 'b':
                gameboard[row][col] = pygame.draw.rect(WIN, BLACK, pygame.Rect((col*GRID_SIZE)+(GRID_SIZE*2), (row*GRID_SIZE)+(GRID_SIZE*2), GRID_SIZE/2, GRID_SIZE/2))

            elif gameboard[row][col] == 'w':
                gameboard[row][col] = pygame.draw.rect(WIN, WHITE, pygame.Rect((col*GRID_SIZE)+(GRID_SIZE*2), (row*GRID_SIZE)+(GRID_SIZE*2), GRID_SIZE/2, GRID_SIZE/2))


        # Need to update the window to display what has been drawn in the loop
        pygame.display.update()


"""
Main Game Loop.
This should hold things related to game logic.
Other specialized functions should be written outside and called in the game loop when needed
"""
def main():
    
    # Clock item to control how many times we loop per second
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_pieces()

    # for row in GAMEBOARD:
    #     print(''.join(row) + '\n')
    pygame.quit()


if __name__ == "__main__":
    main()

