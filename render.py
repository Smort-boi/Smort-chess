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
    (186, 202, 68),  # highlight color
]


def game_init() -> tuple:
    # initializes pygame contains side effects
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Smort chess")
    clock = pygame.time.Clock()
    return (screen, clock)


# renders the BG once to
def render_bg_square(dimensions: int, colors: list[tuple], sq_size: int):

    board_surface = pygame.Surface((dimensions * sq_size, dimensions * sq_size))
    for i in range(dimensions):
        for j in range(dimensions):
            color = colors[(i + j) % 2]
            rect = (j * sq_size, i * sq_size, sq_size, sq_size)
            pygame.draw.rect(board_surface, color, rect)
    return board_surface


def render_highlights(color: tuple, sq_size) -> pygame.Surface:
    highlight_surface = pygame.Surface((sq_size, sq_size))
    pygame.draw.rect(highlight_surface, color, (0, 0, sq_size, sq_size))
    return highlight_surface


# the goal is to send the data generated/collected to be sent to
# other functions for processing
def game_loop(main_surface: pygame.Surface, clock: pygame.Clock):
    # pre-rendering
    board_surface = render_bg_square(DIMENSIONS, COLORS, SQ_SIZE)
    highlight_surface = render_highlights(COLORS[2], SQ_SIZE)
    running: bool = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running: bool = False
        raw_mouse_pos_x, raw_mouse_pos_y = pygame.mouse.get_pos()
        # current square index
        current_x = raw_mouse_pos_x // SQ_SIZE
        current_y = raw_mouse_pos_y // SQ_SIZE

        # main_surface.fill((255, 255, 255))
        # render the frame
        main_surface.blit(board_surface, (0, 0))
        main_surface.blit(highlight_surface, (current_x * SQ_SIZE, current_y * SQ_SIZE))
        # finish rendering the frame
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


def main():
    screen, clock = game_init()
    game_loop(screen, clock)


if __name__ == "__main__":
    main()
