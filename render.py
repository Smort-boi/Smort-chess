import os
import sys

import pygame

# Constants
DIMENSIONS = 8
WIDTH, HEIGHT = 640, 640
SQ_SIZE = 80
FPS = 60
COLORS = [(238, 238, 210), (118, 150, 86)]  # 0 is the light color # 1 is the dark color


def game_init():
    # initializes pygame contains side effects
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Smort chess")
    clock = pygame.time.Clock()
    return (screen, clock)


def handle_events(running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    return running


def get_board_squares(dimensions: int, sq_size: int, colors: list):
    # pure function that return the square positions (color,start_posX,start_posY,sizeX,sizeY).
    return [
        (colors[(i + j) % 2], (i * sq_size, j * sq_size, sq_size, sq_size))
        for i in range(dimensions)
        for j in range(dimensions)
    ]


def draw_frame(main_surface, squares):
    main_surface.fill((255, 255, 255))
    for color, rect in squares:
        pygame.draw.rect(main_surface, color, rect)
    pygame.display.flip()


def run_game_loop(main_surface, clock, squares):
    running = True
    while running:
        clock.tick(FPS)
        running = handle_events(running)
        draw_frame(main_surface, squares)


def main():
    screen, clock = game_init()
    bg_squares = get_board_squares(DIMENSIONS, SQ_SIZE, COLORS)
    run_game_loop(screen, clock, bg_squares)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
