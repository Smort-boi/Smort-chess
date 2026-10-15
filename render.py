import os
import sys

import pygame

# Constants
DIMENSIONS: int = 8
WIDTH: int = 640
HEIGHT: int = 640
SQ_SIZE: int = 80
FPS: int = 60
COLORS: list[tuple] = [
    (238, 238, 210),
    (118, 150, 86),
]  # 0 is the light color # 1 is the dark color


def game_init() -> tuple:
    # initializes pygame contains side effects
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Smort chess")
    clock = pygame.time.Clock()
    return (screen, clock)


def render_bg_square(dimensions, colors, sq_size):
    board_surface = pygame.Surface((dimensions * sq_size, dimensions * sq_size))
    for i in range(dimensions):
        for j in range(dimensions):
            color = colors[(i + j) % 2]
            rect = j * sq_size, i * sq_size, sq_size, sq_size
            pygame.draw.rect(board_surface, color, rect)
    return board_surface


def game_loop(main_surface, clock):
    board_surface = render_bg_square(DIMENSIONS, COLORS, SQ_SIZE)
    running: bool = True
    clock.tick(60)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running: bool = False
        # screen reset
        main_surface.fill((255, 255, 255))
        # render the frame
        main_surface.blit(board_surface, (0, 0))
        pygame.display.flip()
    pygame.quit()


def main():
    screen, clock = game_init()
    game_loop(screen, clock)


if __name__ == "__main__":
    main()
