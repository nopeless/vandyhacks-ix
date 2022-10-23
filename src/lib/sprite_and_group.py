import functools
import logging
import math

import pygame

import keyboard
import resources

sfx = resources.sfx
from .image_helpers import IGif
from util import angle_to, rot_center, flip


@functools.cache
def image_to_mask(image):
    return pygame.mask.from_surface(image)


DEG_TO_RAD = math.pi / 180


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
        self.world = None

        self.static = True
        self.gravity = False

        self.ground_timer = 0
        self.hit_ceiling = False

        self.use_manual_hitbox = False
        self._hitbox_image = None

        self.last_direction = 0
        self.flip_for_direction = False

        self.image = pygame.image.load("src/_internal_resources/fallback.png")
        self._image_cache = None
        self._rendering_mode = "PYSURFACE"

        # Might not dynamically change in the layered update group
        self.layer = 0

        self._id = None

        self.pos = pygame.Vector2(0, 0)
        self.last_pos = self.pos.copy()

        self.velocity = pygame.Vector2(0, 0)

    def on_land(self):
        pass

    def on_head(self):
        pass

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
        i = self._image_cache

        if self.flip_for_direction:
            if self.last_direction == -1:
                i = flip(i)
        return i

    @image.setter
    def image(self, v):
        if isinstance(v, IGif):
            self._rendering_mode = "IGIF"
            self._image_cache = v.image
        else:
            self._rendering_mode = "PYSURFACE"
            self._image_cache = v
        self._image = v

        # Respect hitboxes
        if not self.use_manual_hitbox:
            self.mask = image_to_mask(self.image)

    def update(self, *args, **kwargs):
        if self._rendering_mode is "IGIF":
            # Updates the frame index
            self._image_cache = self._image.frame
        self.ground_timer += 1
        self.last_pos = self.pos.copy()
        self.pos += self.velocity

    @property
    def rect(self):
        return self._image_cache.get_rect().move(self.pos)

    def draw(self, screen):
        """
        Implemented like SpriteGroup.draw
        """
        screen.blit(self.image, self.rect)


class Group(pygame.sprite.LayeredUpdates):
    def __init__(self, *sprites):
        super().__init__(*sprites)


class Player(Sprite):
    def __init__(self, image, cleaner=None):
        super().__init__()
        self.static = False
        self.gravity = True
        self.image = image

        self.cleaner = cleaner

        self.used_double_jump = False
        self.flip_for_direction = True
        self.last_direction = 0
        self.last_key_hit_timer = 0
        self.used_dash = False
        self.dash_cooldown = 0

    def on_land(self):
        sfx.land.play()
        self.used_dash = False
        self.used_double_jump = False

    def on_head(self):
        sfx.head.play()

    def event(self, event):
        # Jump
        if keyboard.keydown(event, pygame.K_w):
            if self.ground_timer < 12:
                logging.info("player jumped")
                sfx.jump.play()
                self.velocity -= (0, 4)
            elif not self.used_double_jump and self.ground_timer < 60:
                logging.info("player used second jump")
                sfx.jump.play()
                self.velocity.y = -5.5
                self.used_double_jump = True

        # Dash
        for x, key in (
            (1, pygame.K_d),
            (-1, pygame.K_a),
        ):
            if self.dash_cooldown < 0:
                if (
                    not self.used_dash
                    and x == self.last_direction
                    and self.last_key_hit_timer < 8
                    and keyboard.keydown(event, key)
                ):
                    logging.debug("player dashed")
                    sfx.dash.play()
                    self.used_dash = True
                    self.velocity = pygame.Vector2(4 * x, 0)
                    self.dash_cooldown = 60

    def update(self, keys):

        # Cleaner logic
        if self.cleaner:
            if self.world:
                angle = angle_to(self.rect.center, self.world.get_mouse_pos())
                self.cleaner.pos = pygame.Vector2(self.rect.topleft)
                self.cleaner.rotation = angle

        # Jump enhance
        if keys[pygame.K_w]:
            if self.ground_timer < 30:
                if not self.hit_ceiling:
                    self.velocity -= (
                        0,
                        0.3 * ((30 - self.ground_timer) / 30),
                    )

        if keys[pygame.K_j]:
            self.world.camera.pos -= (1, 0)
        if keys[pygame.K_l]:
            self.world.camera.pos += (1, 0)

        if keys[pygame.K_i]:
            self.world.camera.pos += (0, -1)
        if keys[pygame.K_k]:
            self.world.camera.pos += (0, 1)

        xs = keyboard.pygame_keys_x_axis(keys)

        move = (
            pygame.Vector2(
                xs,
                0,
            )
            * 0.2
        )

        if self.ground_timer < 1:
            self.used_dash = False

        if xs != 0:
            self.last_key_hit_timer = 0
            self.last_direction = xs

        self.velocity += move

        self.last_key_hit_timer += 1
        self.dash_cooldown -= 1
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


class PlayerCleaner(Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rotation = 0


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

    def __init__(self, image):
        super().__init__()
        self.image = image
        self.static = True


class NPC(Sprite):
    """
    A non-player character

    Shows a text bubble when the player is close
    """
