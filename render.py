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
    (238, 238, 210),  # lighter color
    (118, 150, 86),  # darker color
]
HIGHLIGHT_COLOR: tuple = (186, 202, 68)


def game_init() -> tuple:
    # initializes pygame contains side effects
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Smort chess")
    clock = pygame.time.Clock()
    return (screen, clock)


def render_bg_square(dimensions: int, colors: list[tuple], sq_size: int):
    board_surface = pygame.Surface((dimensions * sq_size, dimensions * sq_size))
    for i in range(dimensions):
        for j in range(dimensions):
            color = colors[(i + j) % 2]
            rect = j * sq_size, i * sq_size, sq_size, sq_size
            pygame.draw.rect(board_surface, color, rect)
    return board_surface


def render_highlights(color, sq_size):
    highlight_surface = pygame.Surface((sq_size, sq_size))
    pygame.draw.rect(highlight_surface, color, (0, 0, sq_size, sq_size))
    return highlight_surface


def game_loop(main_surface, clock):
    board_surface = render_bg_square(DIMENSIONS, COLORS, SQ_SIZE)
    highlight_surface = render_highlights(HIGHLIGHT_COLOR, SQ_SIZE)
    running: bool = True
    clock.tick(60)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running: bool = False
        # current mouse position in raw coordinates in a
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        current_x, current_y = mouse_pos_x // SQ_SIZE, mouse_pos_y // SQ_SIZE
        print(current_x, current_y)
        main_surface.fill((255, 255, 255))
        # render the frame
        main_surface.blit(board_surface, (0, 0))
        main_surface.blit(highlight_surface, (current_x * SQ_SIZE, current_y * SQ_SIZE))
        # finish rendering the frame
        pygame.display.flip()
    pygame.quit()


def main():
    screen, clock = game_init()
    game_loop(screen, clock)


if __name__ == "__main__":
    main()
