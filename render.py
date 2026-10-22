"""now i need a function movement functionality to the game loop"""

import os
import sys

import pygame

from board import Board, Piece

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


# initializes pygame contrains side effects
def game_init() -> tuple:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Smort chess")
    # pygame.display.set_icon("")
    clock = pygame.time.Clock()
    return (screen, clock)


# return dict containing the file as values of the aliases
def load_pieces_into_memory(asset_directory, size) -> dict[int, pygame.Surface]:
    asset_dir = os.path.join(os.getcwd(), asset_directory)
    piece_aliases = {
        "black-bishop.png": 12,
        "black-king.png": 9,
        "black-knight.png": 11,
        "black-pawn.png": 10,
        "black-queen.png": 14,
        "black-rook.png": 13,
        "white-bishop.png": 20,
        "white-king.png": 17,
        "white-knight.png": 19,
        "white-pawn.png": 18,
        "white-queen.png": 22,
        "white-rook.png": 21,
    }
    # Some black magic type shit
    return {
        piece_aliases[file]: pygame.transform.smoothscale(
            pygame.image.load(os.path.join(asset_dir, file)).convert_alpha(),
            (size, size),
        )
        for file in os.listdir(asset_dir)
        if file in piece_aliases
    }


def render_pieces(
    dimensions: int,
    sq_size: int,
    board_array: list[int],
    piece_surfaces: dict[int, pygame.Surface],
) -> pygame.Surface:

    board_surface = pygame.Surface(
        (dimensions * sq_size, dimensions * sq_size), pygame.SRCALPHA
    )
    for index, piece in enumerate(board_array):
        if piece == 0:
            continue
        else:
            rect = ((index % dimensions) * sq_size, (index // dimensions) * sq_size)
            board_surface.blit(piece_surfaces[piece], rect)
    return board_surface


# renders the BG once to
def render_bg_square(
    dimensions: int, colors: list[tuple], sq_size: int
) -> pygame.Surface:

    board_surface = pygame.Surface((dimensions * sq_size, dimensions * sq_size))
    for i in range(dimensions):
        for j in range(dimensions):
            color = colors[(i + j) % 2]
            rect = (j * sq_size, i * sq_size, sq_size, sq_size)
            pygame.draw.rect(board_surface, color, rect)
    return board_surface


def render_highlights(color: tuple, sq_size: int) -> pygame.Surface:
    highlight_surface = pygame.Surface((sq_size, sq_size))
    pygame.draw.rect(highlight_surface, color, (0, 0, sq_size, sq_size))
    return highlight_surface


# the goal is to send the data generated/collected to be sent to
# other functions for processing
def game_loop(main_surface: pygame.Surface, clock: pygame.Clock, board: Board):
    board.make_move(0, 50)
    # pre-rendering------------------------------------------------
    loaded_pieces = load_pieces_into_memory(asset_directory="assets", size=SQ_SIZE)
    board_surface = render_bg_square(
        dimensions=DIMENSIONS, colors=COLORS, sq_size=SQ_SIZE
    )
    highlight_surface = render_highlights(color=COLORS[2], sq_size=SQ_SIZE)
    piece_surface = render_pieces(
        dimensions=DIMENSIONS,
        sq_size=SQ_SIZE,
        board_array=board.squares,
        piece_surfaces=loaded_pieces,
    )
    # --------------------------------------------------------------
    running: bool = True
    while running:
        raw_mouse_pos_x, raw_mouse_pos_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running: bool = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pass
        # current square index
        current_x = raw_mouse_pos_x // SQ_SIZE
        current_y = raw_mouse_pos_y // SQ_SIZE

        # main_surface.fill((255, 255, 255))
        # start rendering the frame
        main_surface.blit(board_surface, (0, 0))
        main_surface.blit(highlight_surface, (current_x * SQ_SIZE, current_y * SQ_SIZE))
        # testing the if the picees load at all
        main_surface.blit(piece_surface, (0, 0))
        # finish rendering the frame
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    sys.exit()


def main():
    screen, clock = game_init()
    board: Board = Board()
    board.from_fen_to_board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
    game_loop(screen, clock, board)


if __name__ == "__main__":
    main()
