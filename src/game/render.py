"""
Accepts a world and blits on a screen
"""
import logging

import pygame
import pyscroll


# def scale_rect(rect, factor):
#     center = rect.center
#     width = rect.width * factor
#     height = rect.height * factor
#     return pygame.Rect(center, (width, height)).move(-width / 2, -height / 2)


# def rect_absolute_scale(rect, factor):
#     return pygame.Rect(
#         rect.left * factor, rect.top * factor, rect.width * factor, rect.height * factor
#     )


# This value refers to how many screen pixels are in a tile pixel
# Setting this value to a 1 will result in a buffer that fits the entire screen
# Please make sure that this value is a power of 2
PIXEL_CONVERSION = 1


class Renderer:
    def __init__(self, world):
        self.world = world

        self.map_data = pyscroll.TiledMapData(world.tmx)

        self.map_layer = pyscroll.BufferedRenderer(
            self.map_data, self.world.screen_size / PIXEL_CONVERSION, alpha=True
        )

        # make the PyGame SpriteGroup with a scrolling map
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer)

        # This is a virtual screen
        self.canvas = pygame.Surface(
            self.world.screen_size / PIXEL_CONVERSION, pygame.SRCALPHA, 32
        )

    def render(self, screen):
        """
        Renders the world on the screen
        """

        self.group.center(self.world.camera.center)

        self.canvas.fill((0, 0, 0, 0))
        self.group.draw(self.canvas)

        projection = None

        # print(self.group.view, self.world.camera.absolute_rect)

        if not self.group.view.contains(self.world.camera.absolute_rect):
            logging.error("zoom was outside of what was rendered")
            projection = self.canvas
        else:
            # Subsurface is used to zoom
            r = self.world.camera.absolute_rect

            r.topleft = (
                r.left - self.group.view.left,
                r.top - self.group.view.top,
            )

            # print(r)

            projection = self.canvas.subsurface(r)

        # Upscale the
        projection = pygame.transform.scale(projection, self.world.screen_size)

        screen.blit(projection, (0, 0))
