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


# def rect_absolute_scale(rect, factor):
#     return pygame.Rect(
#         rect.left * factor, rect.top * factor, rect.width * factor, rect.height * factor
#     )


# This value refers to the relative scale of the buffer to the screen resolution
# 8 means 8 pixels on the screen is 1 pixel on the tile
# Setting this value to a 1 will result in a buffer that fits the entire screen
WORLD_RENDER_SCALE = 6

# def safe_subsurface(img, rect):


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
        logging.info(f"initialized world canvas {self.world.screen_size}")
        self.canvas = pygame.Surface(self.world.screen_size, pygame.SRCALPHA, 32)

        self.pyscroll_view = pygame.Surface(
            self.world.screen_size / WORLD_RENDER_SCALE, pygame.SRCALPHA, 32
        )

        logging.info(
            f"if using absolute camera, the render port {self.world.screen_size / WORLD_RENDER_SCALE} will be scaled to world canvas size"
        )

    def render(self, screen):
        """
        Renders the world on the screen
        """
        self.canvas.fill((0, 0, 0, 0))
        self.pyscroll_view.fill((0, 0, 0, 0))

        self.group.center(self.world.camera.rect.center)

        self.group.draw(self.pyscroll_view)

        self.canvas.blit(self.pyscroll_view, self.group.view)

        pygame.draw.rect(self.canvas, (0, 0, 255), self.world.camera.rect, width=2)

        screen.blit(
            # self.pyscroll_view,
            self.canvas,
            (0, 0)
            # pygame.transform.scale(self.pyscroll_view, self.world.screen_size), (0, 0)
        )

        # if self.world.debug:
        #     if self.world.debug_use_absolute_camera:
        #         # Draw blue outline for camera
        #         pygame.draw.rect(self.canvas, (0, 0, 255, 64), self.world.camera.rect)

        # self.group.draw(self.canvas)

        # self.world.draw(self.canvas)
        # self.world.particles.draw(self.canvas)

        # if self.world.debug_use_absolute_camera:
        #     screen.blit(
        #         self.canvas,
        #         (0, 0),
        #     )
        #     return

        # projection = None

        # if not self.group.view.contains(self.world.camera.absolute_rect):
        #     logging.error("zoom was outside of what was rendered")
        #     projection = self.scrollsurface
        # else:
        #     # Subsurface is used to zoom
        #     r = self.world.camera.absolute_rect

        #     # r.topleft = (
        #     #     r.left - self.group.view.left,
        #     #     r.top - self.group.view.top,
        #     # )

        #     projection = self.scrollsurface.subsurface(r)
        #     projection = pygame.transform.scale(projection, self.world.screen_size)

        # Upscale the
        # projection = pygame.transform.scale(projection, self.world.screen_size)
        # screen.blit(projection, (0, 0))

        # screen.blit(projection, (0, 0))

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
