"""
Accepts a world and blits on a screen
"""
import logging
import math
import functools

import pygame
import pyscroll

import keyboard

from lib import Group
from util import angle_to, rot_center, flip
from ui import BaseText

DEG_TO_RAD = math.pi / 180


# def scale_rect(rect, factor):
#     center = rect.center
#     width = rect.width * factor
#     height = rect.height * factor
#     return pygame.Rect(center, (width, height)).move(-width / 2, -height / 2)


def rect_absolute_scale(rect, factor):
    return pygame.Rect(
        rect.left * factor, rect.top * factor, rect.width * factor, rect.height * factor
    )


# This value refers to the relative scale of the buffer to the screen resolution
# 8 means 8 pixels on the screen is 1 pixel on the tile
# Setting this value to a 1 will result in a buffer that fits the entire screen
WORLD_RENDER_SCALE = 6


@functools.cache
def to_str(i):
    return str(i)


class Renderer:
    def __init__(self, world):
        self.world = world

        self.map_data = pyscroll.TiledMapData(world.tmx)

        self.map_layer = pyscroll.BufferedRenderer(
            self.map_data,
            self.world.screen_size / WORLD_RENDER_SCALE,
            alpha=True,
            clamp_camera=False,
        )

        # make the PyGame SpriteGroup with a scrolling map
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer)

        # This is a virtual screen
        logging.info(f"initialized world canvas {self.world.dimensions}")
        self.canvas = pygame.Surface(self.world.dimensions, pygame.SRCALPHA, 32)

        self.pyscroll_view = pygame.Surface(
            self.world.screen_size / WORLD_RENDER_SCALE, pygame.SRCALPHA, 32
        )

        self.text_canvas = pygame.Surface(self.world.screen_size, pygame.SRCALPHA, 32)

        logging.info(
            f"if using absolute camera, the render port {self.world.screen_size / WORLD_RENDER_SCALE} will be scaled to world canvas size"
        )

        self.hud = Group()

        self.score_text = BaseText("score:        ", size=64)
        self.score_text.pos = pygame.Vector2(self.world.screen_size[0] - 300, 0)

        def l(*args, **kwargs):
            self.score_text.text = "Score: " + to_str(self.world.score)

        # Register updater
        self.score_text.update = l

        self.hud.add(self.score_text)

    def render(self, screen):
        """
        Renders the world on the screen
        """
        self.canvas.fill((0, 0, 0, 0))
        self.text_canvas.fill((0, 0, 0, 0))
        self.pyscroll_view.fill((0, 0, 0, 0))

        # Update hud elements
        self.hud.update()

        self.group.center(self.world.camera.rect.center)

        self.group.draw(self.pyscroll_view)

        self.canvas.blit(self.pyscroll_view, self.group.view)

        if self.world.debug and self.world.debug_use_absolute_camera:
            pygame.draw.rect(self.canvas, (0, 0, 255), self.world.camera.rect, width=2)

        for sprite in self.world.sprites():
            if self.world.debug_show_hitbox:
                if sprite.use_manual_hitbox and sprite._hitbox_image:
                    self.canvas.blit(sprite._hitbox_image, sprite.rect)
                    continue
            self.canvas.blit(sprite.image, sprite.rect)

        cleaner = self.world.player.cleaner
        # Special logic handler
        if cleaner:
            cleaner.update()
            if (
                90 * DEG_TO_RAD < cleaner.rotation
                or -90 * DEG_TO_RAD > cleaner.rotation
            ):
                image, rect = rot_center(
                    cleaner.image, 90 * DEG_TO_RAD + cleaner.rotation / 2, (12, 12)
                )
                image = flip(image)
                self.canvas.blit(image, cleaner.pos + rect.topleft + (-14, 6))
            else:
                image, rect = rot_center(cleaner.image, -cleaner.rotation / 2, (12, 12))
                self.canvas.blit(image, cleaner.pos + rect.topleft + (14, 6))

        self.world.collectibles.draw(self.canvas)

        self.world.particles.draw(self.canvas)

        if self.world.debug_use_absolute_camera:
            screen.blit(self.canvas, (0, 0))
        else:
            pre = pygame.transform.scale(
                self.canvas.subsurface(self.world.camera.rect),
                self.world.screen_size,
            )

            for text in self.world.texts:
                # Blit high quality things here
                text.blit_to(
                    self.text_canvas,
                    (text.pos - self.group.view.topleft) * WORLD_RENDER_SCALE,
                )

            text_overlay = pygame.transform.scale(
                self.text_canvas,
                self.world.screen_size * self.world.camera.zoom / WORLD_RENDER_SCALE,
            )

            # Render high quality text
            pre.blit(
                text_overlay,
                # (0, 0)
                (
                    pygame.Vector2(self.group.view.topleft)
                    - self.world.camera.rect.topleft
                )
                * WORLD_RENDER_SCALE
                * 2,
            )

            screen.blit(
                pre,
                (
                    WORLD_RENDER_SCALE
                    * (self.world.camera.rect.left - self.world.camera.pos.x),
                    WORLD_RENDER_SCALE
                    * (self.world.camera.rect.top - self.world.camera.pos.y),
                ),
            )

            pygame.draw.rect(screen, (0, 0, 0), screen.get_rect(), width=8)

            # Draw hud
            for sprite in self.hud.sprites():
                sprite.blit_to(screen, sprite.pos)

    def event(self, event):
        if self.world.debug:
            if keyboard.debug_key(event.keys, event, pygame.K_o):
                self.world.debug_use_absolute_camera = (
                    not self.world.debug_use_absolute_camera
                )
                logging.debug(
                    f"Toggling absolute camera to {self.world.debug_use_absolute_camera }"
                )
            if keyboard.debug_key(event.keys, event, pygame.K_b):
                self.world.debug_show_hitbox = not self.world.debug_show_hitbox
                logging.debug(
                    f"Toggling show hitbox to {self.world.debug_show_hitbox }"
                )

    def update(self, keys):
        """
        Updates itself based on 60hz
        """
