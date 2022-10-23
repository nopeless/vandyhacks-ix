"""
Accepts a world and blits on a screen
"""
import logging

import pygame
import pyscroll

import keyboard


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

        import ui

    def render(self, screen):
        """
        Renders the world on the screen
        """
        self.canvas.fill((0, 0, 0, 0))
        self.text_canvas.fill((0, 0, 0, 0))
        self.pyscroll_view.fill((0, 0, 0, 0))

        self.group.center(self.world.camera.rect.center)

        self.group.draw(self.pyscroll_view)

        self.canvas.blit(self.pyscroll_view, self.group.view)

        if self.world.debug:
            pygame.draw.rect(self.canvas, (0, 0, 255), self.world.camera.rect, width=2)

        self.world.draw(self.canvas)
        self.world.particles.draw(self.canvas)

        # self.text.text += "|"

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

    def event(self, event):
        if self.world.debug:
            if keyboard.debug_key(event.keys, event, pygame.K_o):
                self.world.debug_use_absolute_camera = (
                    not self.world.debug_use_absolute_camera
                )
                logging.debug(
                    f"Toggling absolute camera to {self.world.debug_use_absolute_camera }"
                )

    def update(self, keys):
        """
        Updates itself based on 60hz
        """
