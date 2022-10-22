import pygame
from .image_helpers import IGif


class Sprite(pygame.sprite.Sprite):
    """
    A better sprite class that acts as the base sprite class
    """

    def __init__(self):
        super().__init__()
        self._image = pygame.image.load("../_internal_resources/fallback.png")
        self._rendering_mode = "PYSURFACE"

        self.velocity = pygame.Vector2(0, 0)

    @property
    def image(self):
        if self._rendering_mode is "PYSURFACE":
            return self._image
        elif self._rendering_mode is "IGIF":
            return self._image.image

        raise Exception("This should not happen")

    @property.setter
    def image(self, v):
        self._rendering_mode = "IGIF" if isinstance(v, IGif) else "PYSURFACE"
        self._image = v
        self.rect = v.get_rect()

    def update(self):
        if self._rendering_mode is "IGIF":
            # Updates the frame index
            self.frame

        self.pos += self.velocity

    def draw(self, screen):
        """
        Implemented like SpriteGroup.draw
        """
        screen.blit(self.image, self.rect)

    # Getters and setters

    @property
    def x(self):
        return self.rect.x

    @property
    def y(self):
        return self.rect.y

    @property.setter
    def x(self, v):
        self.rect.x = v

    @property.setter
    def y(self, v):
        self.rect.y = v

    @property
    def pos(self):
        """
        Composite variable of x and y
        """
        return pygame.Vector2(self.x, self.y)

    @property.setter
    def pos(self, v):
        """
        sets x and y
        """
        self.x = v.x
        self.y = v.y

    @property
    def vx(self):
        return self.velocity.x

    @property.setter
    def vx(self, v):
        self.velocity.x = v

    @property
    def vy(self):
        return self.velocity.y

    @property.setter
    def vy(self, v):
        self.velocity.y = v


class Player(Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
