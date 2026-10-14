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


def game_loop(main_surface, clock):
    running: bool = True
    clock.tick(60)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running: bool = False
        # screen reset
        main_surface.fill((255, 255, 255))
        # render
        pygame.display.flip()
    pygame.quit()


def main():
    screen, clock = game_init()
    game_loop(screen, clock)


if __name__ == "__main__":
    main()
