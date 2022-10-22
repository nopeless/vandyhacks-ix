from types import SimpleNamespace
import time

import pygame

from game import World, Engine, Renderer
from util import Counter

import resources
import keyboard


def main(config):
    screen = config.screen

    config.screen_size = screen.get_size()
    config.tmx = resources.level.main

    world = World(config)
    engine = Engine(world)
    renderer = Renderer(world)

    clock = pygame.time.Clock()

    timer = time.time()

    for i in range(3600):
        ### Process events
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            engine.event(event)

        engine.update()

        pos = engine.world.camera.pos
        engine.world.camera.pos = (
            pos.x + keyboard.pygame_keys_x_axis(keys),
            pos.y - keyboard.pygame_keys_y_axis(keys),
        )
        if keys[pygame.K_q]:
            engine.world.camera.zoom *= 1.05
        if keys[pygame.K_e]:
            engine.world.camera.zoom /= 1.05

        # if keys[pygame.K_a]:
        #     engine.world.camera.zoom += 0.1
        # if keys[pygame.K_d]:
        #     engine.world.camera.zoom -= 0.1

        ### Render routine

        # Clear screen
        screen.fill((255, 255, 255))
        # Render to screen
        renderer.render(screen)

        # Call a redraw on screen
        pygame.display.update()

        # Clock
        clock.tick(60)

        if i % 60 == 0:
            print(f"fps: {60/(time.time() - timer)}")
            timer = time.time()
