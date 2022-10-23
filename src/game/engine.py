import math
import logging

import pygame

import keyboard
import resources

sfx = resources.sfx

"""
Accepts a world and modifies it
"""


def get_angle_from_xy(x, y):
    return -math.atan2(-y, x)


def is_entity_colliding(entity, objects):
    return pygame.sprite.spritecollideany(
        entity, objects, collided=pygame.sprite.collide_mask
    )


# This depends on the nature of the map
EXPLORE_DERIVATIVE_THRESHOLD = 5
DEG_TO_RAD = math.pi / 180


def process_collision(movable_entity, static_entities):
    """
    This is a rewrite
    """
    if is_entity_colliding(movable_entity, static_entities):
        relpos = movable_entity.pos.copy()

        ox, oy = movable_entity.rect.x, movable_entity.rect.y

        # Pixel align
        movable_entity.pos.x, movable_entity.pos.y = ox, oy

        dx = 0
        dy = 0

        def _():
            nonlocal dx, dy
            for trydx in range(EXPLORE_DERIVATIVE_THRESHOLD):
                for trydy in range(EXPLORE_DERIVATIVE_THRESHOLD):
                    for usex, usey in (
                        (trydx, -trydy),
                        (trydx, trydy),
                        (-trydx, -trydy),
                        (-trydx, trydy),
                    ):
                        movable_entity.pos = pygame.Vector2(ox + usex, oy + usey)
                        if not is_entity_colliding(movable_entity, static_entities):
                            dx = usex
                            dy = usey
                            return

        _()

        if dx == 0 and dy == 0:
            # We're stuck
            return

        # Reset movable_entity
        movable_entity.pos = relpos

        angle = get_angle_from_xy(dx, dy)

        v = None

        # Circle quadrant calculations
        if dx < 0 and dy < 0:
            v = pygame.Vector2(-dy, -dx)
        if dx > 0 and dy < 0:
            v = pygame.Vector2(dy, dx)
        if dx > 0 and dy > 0:
            v = pygame.Vector2(-dy, -dx)
        if dx < 0 and dy > 0:
            v = pygame.Vector2(dy, dx)

        if dx == 0:
            if dy < 0:
                if movable_entity.ground_timer > 10:
                    movable_entity.on_land()
                movable_entity.ground_timer = 0
                movable_entity.hit_ceiling = False
            else:
                movable_entity.hit_ceiling = True
                movable_entity.on_head()

            movable_entity.pos.y = oy + dy
            movable_entity.velocity.y = 0
            return
        if dy == 0:
            movable_entity.pos.x = ox + dx
            movable_entity.velocity.x = 0
            # Special
            if movable_entity.velocity.y > 0.4:
                movable_entity.velocity.y = 0.4
            return

        if v.length() > 1:
            v = v.normalize()

            velocity_vector = movable_entity.velocity

            if abs(velocity_vector.angle_to(v)) < 90:
                velocity_vector = v.rotate(90) * velocity_vector.dot(v.rotate(90))

                # print("new vector", velocity_vector)
                movable_entity.velocity = velocity_vector

            movable_entity.pos.x += dx
            movable_entity.pos.y += dy
        # else:
        #     # print("here", dx, dy)
        #     if (
        #         dx == 0
        #         and dy == 0
        #         and is_entity_colliding(movable_entity, static_entities)
        #     ):
        #         # print("cannot process")
        #         movable_entity.pos = relpos - movable_entity.velocity
        #         movable_entity.velocity = pygame.Vector2(0, 0)
        #         return

        #     if dx == 0:
        #         movable_entity.pos.y = oy + dy
        #     if dy == 0:
        #         movable_entity.pos.x = ox + dx


# def process_collision(movable_entity, static_entities):
#     """
#     This took more than 3 hours to write, but it works and don't touch it
#     """
#     if is_entity_colliding(movable_entity, static_entities):
#         relpos = movable_entity.pos.copy()
#         ox, oy = movable_entity.rect.x, movable_entity.rect.y

#         # Pixel align
#         movable_entity.pos.x, movable_entity.pos.y = ox, oy

#         dx = 0
#         dy = 0
#         for i in range(1, EXPLORE_DERIVATIVE_THRESHOLD):
#             movable_entity.pos.x = ox + i
#             if not is_entity_colliding(movable_entity, static_entities):
#                 dx = i
#                 break
#             movable_entity.pos.x = ox - i
#             if not is_entity_colliding(movable_entity, static_entities):
#                 dx = -i
#                 break

#         # Reset movable_entity
#         movable_entity.pos.x, movable_entity.pos.y = ox, oy

#         for i in range(1, EXPLORE_DERIVATIVE_THRESHOLD):
#             movable_entity.pos.y = oy + i
#             if not is_entity_colliding(movable_entity, static_entities):
#                 dy = i
#                 break
#             movable_entity.pos.y = oy - i
#             if not is_entity_colliding(movable_entity, static_entities):
#                 dy = -i
#                 break

#         # Reset movable_entity
#         movable_entity.pos.x, movable_entity.pos.y = ox, oy

#         angle = get_angle_from_xy(dx, dy)

#         v = None

#         # Circle quadrant calculations
#         if dx < 0 and dy < 0:
#             v = pygame.Vector2(-dy, -dx)
#         if dx > 0 and dy < 0:
#             v = pygame.Vector2(dy, dx)
#         if dx > 0 and dy > 0:
#             v = pygame.Vector2(-dy, -dx)
#         if dx < 0 and dy > 0:
#             v = pygame.Vector2(dy, dx)

#         if dx == 0:
#             v = pygame.Vector2(0, -dy)
#         if dy == 0:
#             v = pygame.Vector2(-dx, 0)

#         if v.length() > 3:
#             v = v.normalize()

#             velocity_vector = movable_entity.velocity

#             if abs(velocity_vector.angle_to(v)) < 90:
#                 velocity_vector = v.rotate(90) * velocity_vector.dot(v.rotate(90))

#                 # print("new vector", velocity_vector)
#                 movable_entity.velocity = velocity_vector

#             if dx == 0:
#                 movable_entity.pos.y += dy
#             elif dy == 0:
#                 movable_entity.pos.x += dx
#             else:
#                 movable_entity.pos.x += dx / 2
#                 movable_entity.pos.y += dy / 2
#         else:
#             # print("here", dx, dy)
#             if (
#                 dx == 0
#                 and dy == 0
#                 and is_entity_colliding(movable_entity, static_entities)
#             ):
#                 # print("cannot process")
#                 movable_entity.pos = relpos - movable_entity.velocity
#                 movable_entity.velocity = pygame.Vector2(0, 0)
#                 return

#             if dx == 0:
#                 movable_entity.pos.y = oy + dy
#             if dy == 0:
#                 movable_entity.pos.x = ox + dx


class Engine:
    def __init__(self, world):
        self.world = world

    def event(self, event):
        """
        Process pygame events
        """
        self.world.player.event(event)

    def update(self, keys):
        """
        Updates itself based on 60hz
        """

        for sprite in self.world.sprites():
            # Add gravity
            if sprite.gravity:
                sprite.velocity.y += 0.2

            # Process friction
            # TODO improve friction
            sprite.velocity.y *= 0.95
            sprite.velocity.x *= 0.9

            if abs(sprite.velocity.x) < 0.1:
                sprite.velocity.x = 0

        self.world.update(keys=keys)

        player = self.world.player

        if not is_entity_colliding(player, self.world.collision_sprites):
            # attemp to snap to ground
            last_pos = player.pos.copy()
            player.pos.y += 1
            if is_entity_colliding(player, self.world.collision_sprites):
                # Special override
                player.pos.y = last_pos.y

        # Process collisions
        for sprite in self.world.sprites():
            if not sprite.static:
                process_collision(sprite, self.world.collision_sprites)

        # Process collectibles
        for sprite in self.world.collectibles:
            if sprite.rect.colliderect(player.rect):
                sprite.kill()
                self.world.collectibles.remove(sprite)
                self.world.score += 100
                continue

            diff = sprite.pos - player.pos
            if diff.length() < 100:
                # print("in range")
                if (
                    abs(diff.angle_to(self.world.get_mouse_pos() - player.rect.center))
                    < 180 * DEG_TO_RAD
                ):
                    sprite.velocity += (
                        diff.normalize() * -0.1 * 300 / (diff.length() + 150)
                    )

            sprite.velocity *= 0.9

        self.world.collectibles.update()

        # print("player where", player.rect)
        self.world.camera.target = player.rect.center
        self.world.camera.update()
