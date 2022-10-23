import functools

import pygame
from .image_helpers import IGif


@functools.cache
def image_to_mask(image):
    return pygame.mask.from_surface(image)


class Tile(pygame.sprite.Sprite):
    """
    Should not be drawn
    """

    def __init__(self, col, row, w, h, image):
        super().__init__()
        self.col, self.row = col, row
        self.rect = pygame.Rect(col * w, row * h, w, h)
        self._image = image
        self.mask = image_to_mask(image)


class Sprite(pygame.sprite.Sprite):
    """
    A better sprite class that acts as the base sprite class

    Defaults

      static - the sprite is static and will not collide with the collision layer
      gravity - the sprite will not be affected by gravity
    """

    def __init__(self):
        super().__init__()
        static = True
        gravity = False
        self.use_manual_hitbox = False

        self.image = pygame.image.load("src/_internal_resources/fallback.png")
        self._rendering_mode = "PYSURFACE"

        # Might not dynamically change in the layered update group
        self.layer = 0

        self.pos = pygame.Vector2(0, 0)

        self.velocity = pygame.Vector2(0, 0)

    @property
    def hitbox(self):
        return self.mask

    @hitbox.setter
    def hitbox(self, v):
        self.use_manual_hitbox = True
        self.mask = image_to_mask(v)

    @property
    def image(self):
        if self._rendering_mode is "PYSURFACE":
            return self._image
        elif self._rendering_mode is "IGIF":
            return self._image.image

        raise Exception("This should not happen")

    @image.setter
    def image(self, v):
        self._rendering_mode = "IGIF" if isinstance(v, IGif) else "PYSURFACE"
        self._image = v

        # Respect hitboxes
        if not self.use_manual_hitbox:
            self.mask = image_to_mask(self.image)

    def update(self):
        if self._rendering_mode is "IGIF":
            # Updates the frame index
            self.frame
        self.pos += self.velocity

    @property
    def rect(self):
        return self.image.get_rect().move(self.pos)

    def draw(self, screen):
        """
        Implemented like SpriteGroup.draw
        """
        screen.blit(self.image, self.rect)


class Group(pygame.sprite.LayeredUpdates):
    def __init__(self, *sprites):
        super().__init__(*sprites)


class Player(Sprite):
    def __init__(self, image):
        super().__init__()
        self.static = False
        self.gravity = True
        self.image = image


class PlayerGun(Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image


class Particle(Sprite):
    """
    A self removing sprite
    """

    def __init__(self, image, callback=None):
        super().__init__()
        self.image = image
        self.callback = (
            callback if callback else lambda s, t: None if t < 60 else self.kill()
        )

    def update(self):
        super().update()
        self.callback()

    def create_at(self, pos):
        """
        Creates a new particle at the given position
        """
        p = Particle(self.image, self.callback)
        p.pos = pos
        return p
