import logging
import time

import pygame

import resources

import config

from lib import Group, Tile, Player, Particle
from ui import BaseText

from util import clamp

from .world_load import load


class Camera:
    def __init__(self, world):
        self.world = world

        # Local zoom * Global render scale
        self._zoom = 1 * 6

        # Use quadratic speed (hard coded)
        self.camera_stiffness = 0.1

        # Do not change this value
        self.camera_speed_factor = self.world.dimensions.length()

        self.pos = pygame.Vector2(128, 128)

        self.target = None

        self.target_zoom = None

    # TODO NOT tested
    def translator(self, pos):
        return (pos - self.pos) * self.zoom

    @property
    def center(self):
        return self.pos + self.world.screen_size / self.zoom / 2

    @property
    def rect(self):
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
        c1 = self.absolute_rect.center
        self._zoom = v
        # Trigger clamp update
        c2 = self.absolute_rect.center
        self.pos = self.pos + (c1[0] - c2[0], c1[1] - c2[1])

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
            0, self._pos.x, self.world.width - self.world.screen_size[0] / self.zoom
        )
        self._pos.y = clamp(
            0, self._pos.y, self.world.height - self.world.screen_size[1] / self.zoom
        )

    @property
    def center(self):
        return (
            self.pos.x + self.world.screen_size.x / self.zoom / 2,
            self.pos.y + self.world.screen_size.y / self.zoom / 2,
        )

    def update(self):
        # TODO not tested
        if self.target is not None:
            d = pygame.Vector2(self.target) - self.center
            # TODO improve this block
            dd = d / 10

            self.pos = self.pos + dd
        if self.target_zoom is not None:
            self.zoom = (
                self.zoom + (self.target_zoom - self.zoom) * self.camera_stiffness
            )


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

        logging.info(
            f"accepted tmx of tile {self.tilewidth}x{self.tileheight} total {self.width}x{self.height}"
        )

        idx, collision_layer = next(
            ((i, l) for i, l in enumerate(self.tmx.layers) if l.name == "collision"),
            None,
        )
        if collision_layer is None:
            raise Exception(
                "Collision layer was not found. Check if 'collision' layer is present"
            )

        del self.tmx.layers[idx]

        self.collision_sprites = pygame.sprite.Group()

        for col, row, surface in collision_layer.tiles():
            t = Tile(col, row, self.tilewidth, self.tileheight, surface)
            self.collision_sprites.add(t)

        self.debug = config.debug

        self.debug_use_absolute_camera = config.debug
        self.debug_show_hitbox = config.debug

        logging.info(f"{self.debug_use_absolute_camera=}")
        logging.info(f"{self.debug_show_hitbox=}")

        self.dimensions = pygame.Vector2(self.width, self.height)

        if self.tilewidth != self.tileheight:
            logging.warning("Tiles are not a square, this will cause serious issues")

        logging.debug(f"Accepted screen config of {config.screen_size}")
        self.screen_size = pygame.Vector2(config.screen_size)

        self.score = 0

        self.start_time = time.time()

        # This will be dealt by the render function
        self.particles = Group()

        # Special rendering layer tht shouldn't be treated like a sprite group
        self.texts = Group()

        self.collectibles = Group()

        self.camera = Camera(self)

        self.player = resources.sprites.player

        self.player.world = self
        self.player.pos = pygame.Vector2(20, 8)

        self.add(self.player)

        # Must be last call
        load(self)

    def get_ellapsed_time(self):
        return time.time() - self.start_time

    def get_mouse_pos(self):
        """
        Get the mouse position in world coordinates
        """
        return (
            pygame.Vector2(pygame.mouse.get_pos()) / self.camera.zoom + self.camera.pos
        )
