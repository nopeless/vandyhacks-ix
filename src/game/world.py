import logging

import pygame

from lib import Group


def clamp(s, n, l):
    if n < s:
        return s
    if n > l:
        return l
    return n


class Camera:
    def __init__(self, world):
        self.world = world

        self._zoom = 16.0

        self.pos = pygame.Vector2(0, 0)

    # TODO NOT tested
    def translator(self, pos):
        return (pos - self.pos) * self.zoom

    @property
    def center(self):
        return self.pos + self.world.screen_size / self.zoom / 2

    @property
    def absolute_rect(self):
        """
        where the view rect lies in the actual map
        """
        return pygame.Rect(
            self.pos.x,
            self.pos.y,
            self.world.screen_size.x / self.zoom,
            self.world.screen_size.y / self.zoom,
        )

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def zoom(self, v):
        self._zoom = v
        # Trigger clamp update
        self.pos = self.pos

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, pos):
        """
        Clamp camera to world
        """
        self._pos = pygame.Vector2(pos)

        # TODO: zoom might be broken
        self._pos.x = clamp(
            self._pos.x, 0, self.world.width - self.world.screen_size[0] / self.zoom
        )
        self._pos.y = clamp(
            self._pos.y, 0, self.world.height - self.world.screen_size[1] / self.zoom
        )

    def update(self):
        pass
        return
        # TODO FIX THIS
        self.pos = self.world.player.pos


class World(Group):
    def __init__(self, config):
        """
        .tmx - The tmx file
        .screen_size - (width, height) of screen to be used by camera

        TMX will contain metadata
        """
        super().__init__()

        self.tmx = config.tmx

        self.tilewidth = config.tmx.tilewidth
        self.tileheight = config.tmx.tileheight

        self.width = config.tmx.width * self.tilewidth
        self.height = config.tmx.height * self.tileheight

        self.dimensions = pygame.Vector2(self.width, self.height)

        if self.tilewidth != self.tileheight:
            logging.warning("Tiles are not a square, this will cause serious issues")

        logging.debug(f"Accepted screen config of {config.screen_size}")
        self.screen_size = pygame.Vector2(config.screen_size)

        self.camera = Camera(self)

        self.particles = Group()

        # Register the particle system
        self.add(self.particles)
