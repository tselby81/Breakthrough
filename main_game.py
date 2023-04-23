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

FPS = 15

GRID_SIZE = 75

WIN_HEIGHT = len(gameboard)*GRID_SIZE
WIN_WIDTH = (len(gameboard[0])*GRID_SIZE) + (GRID_SIZE*4)

BOARD_HEIGHT = len(gameboard)*GRID_SIZE
BOARD_WIDTH = (len(gameboard[0])*GRID_SIZE)


# CREATE A DISPLAY SURFACE
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Breakthrough")


# COLORS TO BE USED TEMPORARILY
# BOARD SQUARES AND PIECE COLORS WILL BE REPLACED WITH IMAGES
WHITE = (255, 255, 255)         # White pieces
BLACK = (0, 0, 0)               # Black pieces

# Images
moon = pygame.image.load(os.path.join('assets', 'Moon.jpg'))
DARK_BOARD_SQUARE = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'SpaceDark.png')), (GRID_SIZE, GRID_SIZE))
DARK_BOARD_SQUARE.convert()
DARK_BOARD_SQUARE_rect = DARK_BOARD_SQUARE.get_rect()
LIGHT_BOARD_SQUARE = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'SpaceLight.png')), (GRID_SIZE, GRID_SIZE))
LIGHT_BOARD_SQUARE.convert()
LIGHT_BOARD_SQUARE_rect = LIGHT_BOARD_SQUARE.get_rect()


def draw_game_board():

    for y in range(0, len(gameboard)):
        for x in range(0, len(gameboard[0])):
            if (x+y) % 2 == 0:
                # r = pygame.Rect((x * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                # pygame.draw.rect(surface, pygame.Color(LIGHT_PURPLE), r)
                WIN.blit(LIGHT_BOARD_SQUARE, (x * GRID_SIZE, y * GRID_SIZE))
                pygame.draw.rect(WIN, WHITE, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
                
            else:
                # r = pygame.Rect((x * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                # pygame.draw.rect(surface, pygame.Color(PURPLISH_BLACK), r)
                pygame.draw.rect(WIN, WHITE, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
                WIN.blit(DARK_BOARD_SQUARE, (x * GRID_SIZE, y * GRID_SIZE))
                pygame.draw.rect(WIN, WHITE, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)


def draw_pieces():

    draw_game_board()

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
    
    def redraw_window():
        WIN.fill(BLACK)
        moon_size = ((WIN.get_width()), (WIN.get_height()))
        MOON = pygame.transform.scale(moon, moon_size)
        MOON.convert()
        WIN.blit(MOON, (0, 0))

        pygame.display.update()

    run = True
    while run:
        clock.tick(FPS)
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_pieces()

    pygame.quit()


if __name__ == "__main__":
    main()

