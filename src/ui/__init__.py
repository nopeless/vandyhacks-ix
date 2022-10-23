"""
Buttons, titles, and other UI elements
"""

import pygame
import config

from lib import Sprite


class BaseText(Sprite):
    """A much better text system"""

    def __init__(
        self,
        text="",
        font=config.Font.default,
        text_color=(255, 255, 255),
        horizontal_center=False,
        size=None,
        *args,
        **kwargs
    ):
        """
        The max size of this text box is calculated by the initial text provided
        """
        super().__init__()
        size = size or font.size
        self.size = size
        self.font = font
        self.text_color = text_color
        self.horizontal_center = horizontal_center

        self.render_cache = None
        self._text = None
        self.text = text

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if self._text == value:
            return
        self.render_cache = self.font.render(value, self.text_color, size=self.size)
        self._text = value

    def blit_to(self, surface, pos):
        x, y = pos
        surface.blit(
            self.render_cache[0],
            (
                x
                - (
                    self.render_cache[1].width // 2 + self.render_cache[1].left
                    if self.horizontal_center
                    else 0
                ),
                y + self.size - self.render_cache[1].top,
            ),
        )
