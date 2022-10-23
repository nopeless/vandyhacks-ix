import functools

import pygame
from .image_helpers import IGif

import resources


@functools.cache
def image_to_mask(image):
    return pygame.mask.from_surface(image)


@functools.cache
def flip(image):
    return pygame.transform.flip(image, True, False)


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
        self.static = True
        self.gravity = False
        self.ground_timer = 0
        self.hit_ceiling = False
        self.use_manual_hitbox = False
        self._hitbox_image = None
        self.last_direction = 0
        self.flip_for_direction = False

        self.image = pygame.image.load("src/_internal_resources/fallback.png")
        self._rendering_mode = "PYSURFACE"

        # Might not dynamically change in the layered update group
        self.layer = 0

        self._id = None

        self.pos = pygame.Vector2(0, 0)
        self.last_pos = self.pos.copy()

        self.velocity = pygame.Vector2(0, 0)

    @property
    def id(self):
        if not self._id:
            raise Exception("Sprite has no id")
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def hitbox(self):
        return self.mask

    @hitbox.setter
    def hitbox(self, v):
        self._hitbox_image = v
        self.use_manual_hitbox = True
        self.mask = image_to_mask(v)

    @property
    def image(self):
        i = None
        if self._rendering_mode is "PYSURFACE":
            i = self._image
        elif self._rendering_mode is "IGIF":
            i = self._image.image
        else:
            raise Exception("This should not happen")

        if self.flip_for_direction:
            if self.last_direction == -1:
                i = flip(i)
        return i

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
            self._image.frame
        self.ground_timer += 1
        self.last_pos = self.pos.copy()
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

        self.used_double_jump = False
        self.flip_for_direction = True
        self.last_direction = 0
        self.last_key_hit_timer = 0
        self.used_dash = False
        self.dash_cooldown = 0

    def update(self):
        self.last_key_hit_timer += 1
        self.dash_cooldown -= 1
        if self.ground_timer == 0:
            self.used_dash = False
            self.used_double_jump = False
        super().update()

        vel = self.pos - self.last_pos

        if vel.y > 2:
            # Falling
            self.image = resources.images.player.fall
        else:
            v = abs(vel.x)
            if v < 0.5:
                # Idle
                self.image = resources.images.player.idle
            elif v < 1:
                # Walk
                self.image = resources.images.player.walk
            elif v < 2:
                # Run
                self.image = resources.images.player.run
            else:
                # Dashing
                self.image = resources.images.player.dash


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


class Trash(Sprite):
    """
    Freeflowing, moving trash
    """


class NPC(Sprite):
    """
    A non-player character

    Shows a text bubble when the player is close
    """
