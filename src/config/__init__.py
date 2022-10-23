# setup stuff here
import os

# This line has to come before import pygame
# or else pygame will say "Hello from pygame"
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame
from pygame import freetype

# Trigger logger setup
from . import set_logger

# Pygame initializations
#
pygame.mixer.pre_init(44100, -16, 2, 2048)  # setup mixer to avoid sound lag
pygame.mixer.init()
pygame.freetype.init()
pygame.init()

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

DEV = True

SAVE_FILE = "game_save_data.json"

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Font:
    default = pygame.freetype.Font("resources/fonts/monogram.ttf", 16)
    comic = pygame.freetype.SysFont("comicsansms", 16)
