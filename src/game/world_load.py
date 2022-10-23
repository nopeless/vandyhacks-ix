import logging
import random

import pygame

import config
import resources

from lib import Group, Tile, Player, Particle, Trash
from ui import BaseText

from util import clamp

# Copied from main file
def is_entity_colliding(entity, objects):
    return pygame.sprite.spritecollideany(
        entity, objects, collided=pygame.sprite.collide_mask
    )


def load(world):
    """
    Register things
    """
    # Debugging
    if world.debug:

        def fac(x, y, text):
            t = BaseText(text)
            t.pos = pygame.Vector2(x, y)
            return t

        for x in range(0, config.tmx.width, 4):
            for y in range(0, config.tmx.width, 4):
                world.texts.add(fac(x * 8, y * 8, f"{x}x{y}"))
        logging.info("added debug tile coordinates")

    # Litter trash
    def fac(x, y, img):
        t = Trash(img)
        return t

    trash = resources.images.trash

    g = lambda: fac(
        0,
        0,
        random.choice(
            [trash.banana, trash.chum, trash.plasticrings, trash.sodacan]
        ).clone(),
    )

    to_be_added = g()

    for x in range(0, config.tmx.width, 4):
        for y in range(15, config.tmx.width, 4):
            to_be_added.pos = pygame.Vector2(
                x * 8 + random.randint(-10, 10), y * 8 + random.randint(-10, 10)
            )
            if random.random() < 0.2 and not is_entity_colliding(
                to_be_added, world.collision_sprites
            ):
                world.add(to_be_added)
                to_be_added = g()
