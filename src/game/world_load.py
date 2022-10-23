import logging

import pygame

import resources

import config

from lib import Group, Tile, Player, Particle
from ui import BaseText

from util import clamp


def load(world):
    """
    Register things
    """
    # Debugging
    if world.debug:

        def fac(x, y, text):
            t = BaseText(text)
            t.pos = pygame.Vector2(x, y)
            return t

        for x in range(0, config.tmx.width, 4):
            for y in range(0, config.tmx.width, 4):
                world.texts.add(fac(x * 8, y * 8, f"{x}x{y}"))
