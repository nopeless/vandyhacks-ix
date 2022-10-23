import pygame
import math

import keyboard

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
                        (trydx, trydy),
                        (-trydx, trydy),
                        (trydx, -trydy),
                        (-trydx, -trydy),
                    ):
                        movable_entity.pos = (ox + usex, oy + usey)
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
            movable_entity.pos.y = oy + dy
            movable_entity.velocity.y = 0
            return
        if dy == 0:
            movable_entity.pos.x = ox + dx
            movable_entity.velocity.x = 0
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
        if keyboard.keydown(event, pygame.K_w):
            self.world.player.velocity -= (0, 5)

    def update(self, keys):
        """
        Updates itself based on 60hz
        """
        if keys[pygame.K_j]:
            self.world.camera.pos -= (1, 0)
        if keys[pygame.K_l]:
            self.world.camera.pos += (1, 0)

        if keys[pygame.K_i]:
            self.world.camera.pos += (0, -1)
        if keys[pygame.K_k]:
            self.world.camera.pos += (0, 1)
        move = (
            pygame.Vector2(
                keyboard.pygame_keys_x_axis(keys),
                0,
            )
            * 0.1
        )

        self.world.player.velocity += move

        for sprite in self.world.sprites():
            # Add gravity
            if sprite.gravity:
                # continue
                sprite.velocity.y += 0.2

            # Process friction
            # TODO improve friction
            sprite.velocity *= 0.9

        self.world.update()

        # Process collisions
        for sprite in self.world.sprites():
            if not sprite.static:
                process_collision(sprite, self.world.collision_sprites)

        # print("player where", self.world.player.rect)
        self.world.camera.target = self.world.player.rect.center
        self.world.camera.update()
