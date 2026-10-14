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


def game_loop():
    pass


def main():
    screen, clock = game_loop()


if __name__ == "__main__":
    main()
