import numbers
import math
import pygame

import logging
import sys
import os

import keyboard


SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 720

pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

import managers

running = True

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

tiles = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.mask = pygame.mask.from_surface(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Player(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.mask = pygame.mask.from_surface(image)
        self.rect = self.image.get_rect()

        # Default starting location
        self.rect.x, self.rect.y = 300, 150

        self.vx, self.vy = 0, 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy


# for x in range(10):
#     for y in range(10):
#         if x == 10 - y:
tiles.add(Tile(0, 0, managers.images.diag))

player = Player(managers.images.playerimg)


def is_player_colliding(player, tiles):
    return pygame.sprite.spritecollideany(
        player, tiles, collided=pygame.sprite.collide_mask
    )


def get_angle_from_xy(x, y):
    return -math.atan2(-y, x)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                player.vy -= 10
    screen.fill((255, 255, 255))

    keys = pygame.key.get_pressed()

    player.vy += 0.2
    player.vx = 2 * keyboard.pygame_keys_x_axis(keys)
    player.update()

    # player.rect.x, player.rect.y = pygame.mouse.get_pos()

    if is_player_colliding(player, tiles):
        ox, oy = player.rect.x, player.rect.y
        dx = 0
        dy = 0
        for i in range(64):
            player.rect.x = ox + i
            if not is_player_colliding(player, tiles):
                dx = i
                break
            player.rect.x = ox - i
            if not is_player_colliding(player, tiles):
                dx = -i
                break

        # Reset player rect
        player.rect.x, player.rect.y = ox, oy

        for i in range(64):
            player.rect.y = oy + i
            if not is_player_colliding(player, tiles):
                dy = i
                break
            player.rect.y = oy - i
            if not is_player_colliding(player, tiles):
                dy = -i
                break

        # Reset player rect
        player.rect.x, player.rect.y = ox, oy

        angle = get_angle_from_xy(dx, dy)

        v = None

        if dx < 0 and dy < 0:
            v = pygame.Vector2(-dy, -dx)
        if dx > 0 and dy < 0:
            v = pygame.Vector2(dy, dx)
        if dx > 0 and dy > 0:
            v = pygame.Vector2(-dy, -dx)
        if dx < 0 and dy > 0:
            v = pygame.Vector2(dy, dx)

        if dx == 0:
            v = pygame.Vector2(0, -dy)
        if dy == 0:
            v = pygame.Vector2(-dx, 0)

        if v.length() > 3:
            v = v.normalize()
            print(dx, dy)

            velocity_vector = pygame.Vector2(player.vx, player.vy)

            # print(v, velocity_vector, velocity_vector.angle_to(v))

            if abs(velocity_vector.angle_to(v)) < 90:
                velocity_vector = v * velocity_vector.dot(
                    v.rotate(90 if dx < 0 else -90)
                )
                # print("new velocity", velocity_vector)

                player.vx = velocity_vector.x
                player.vy = velocity_vector.y

            player.rect.x += dx / 2
            # print(dx)
            player.rect.y += dy / 2

        # if dx == 0:
        #     v = v.rotate(-90)
        # if dy == 0:
        #     v = v.rotate(-90)

        # if v.length() != 0:
        #     # normal = v.normalize()
        #     angle_vector = v.normalize().rotate(180)
        #     print("angle is", angle_vector.as_polar()[1])
        #     print("angv", angle_vector)

        #     velocity_vector = pygame.Vector2(player.vx, player.vy)

        #     print("velocity", velocity_vector)
        #     print("vv", velocity_vector.angle_to(angle_vector.rotate(-90)) + 360)

        #     # Should it be subject to normal force
        #     if (
        #         abs(
        #             (velocity_vector.angle_to(angle_vector.rotate(-90)) + 360) % 360
        #             - 180
        #         )
        #         <= 90
        #     ):
        #         velocity_vector = angle_vector * velocity_vector.dot(angle_vector)

        # Final calculation
        # player.vx = velocity_vector.x
        # player.vy = velocity_vector.y

        # # Force move player
        # player.rect.x += dx
        # # print(dx)
        # player.rect.y += dy
    tiles.draw(screen)
    player.draw(screen)

    pygame.display.update()
    clock.tick(60)
