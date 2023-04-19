import pygame
import sys, os, math
import time

"""
Main file which runs the game.
Draws the various game elements.
Main game loop which calls the various functions and updates the window.
Get
"""
# Matrix to define the starting gameboard
# '.' - Empty, 'B' - black piece, 'W' - white piece
GAMEBOARD = [['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'],
             ['B', 'B', 'B', 'B', 'B', 'B', 'B', 'B'],
             ['.', '.', '.', '.', '.', '.', '.', '.'],
             ['.', '.', '.', '.', '.', '.', '.', '.'],
             ['.', '.', '.', '.', '.', '.', '.', '.'],
             ['.', '.', '.', '.', '.', '.', '.', '.'],
             ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
             ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W']]

FPS = 30

# CREATE THE MAIN GAME WINDOW
GRID_SIZE = 50

WIN_HEIGHT = (len(GAMEBOARD)*GRID_SIZE)
WIN_WIDTH = (len(GAMEBOARD[0])*GRID_SIZE)

WIN = pygame.display.set_mode((WIN_WIDTH + (GRID_SIZE*2), WIN_HEIGHT + (GRID_SIZE*2)))
pygame.display.set_caption("Breakthrough")


# COLORS TO BE USED TEMPORARILY
# BOARD SQUARES AND PIECE COLORS WILL BE REPLACED WITH IMAGES
LIGHT_PURPLE = (199, 164, 222)  # Light squares
PURPLISH_BLACK = (14, 11, 15)   # Dark squares
WHITE = (255, 255, 255)         # White pieces
BLACK = (0, 0, 0)               # Black pieces


def draw_game_board(surface):
    for y in range(0, int(WIN_HEIGHT + GRID_SIZE*4)):
        for x in range(0, int(WIN_WIDTH + GRID_SIZE*4)):
            if (x+y) % 2 == 0:
                r = pygame.Rect((x * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, pygame.Color(LIGHT_PURPLE), r)
            else:
                r = pygame.Rect((x * GRID_SIZE, y * GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, pygame.Color(PURPLISH_BLACK), r)


def draw_window():
    WIN.fill("lightslategrey")

    draw_game_board(WIN)

    for row in range(len(GAMEBOARD)):
        for col in range(len(GAMEBOARD[row])):
            if GAMEBOARD[row][col] == 'B':
                GAMEBOARD[row][col] = pygame.draw.rect(WIN, BLACK, pygame.Rect((col*GRID_SIZE)+(GRID_SIZE*2), (row*GRID_SIZE)+(GRID_SIZE*2), GRID_SIZE/2, GRID_SIZE/2))

            elif GAMEBOARD[row][col] == 'W':
                GAMEBOARD[row][col] = pygame.draw.rect(WIN, WHITE, pygame.Rect((col*GRID_SIZE)+(GRID_SIZE*2), (row*GRID_SIZE)+(GRID_SIZE*2), GRID_SIZE/2, GRID_SIZE/2))

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

        draw_window()

    pygame.quit()


if __name__ == "__main__":
    main()
