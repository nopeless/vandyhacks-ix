from types import SimpleNamespace
import time
import logging

import pygame

import resources
import keyboard

from game import World, Engine, Renderer
from util import Counter


def main(config):
    screen = config.screen

    config.screen_size = screen.get_size()
    config.tmx = resources.level.tropics

    # Debug things
    config.debug = True

    world = World(config)
    engine = Engine(world)
    renderer = Renderer(world)

    clock = pygame.time.Clock()

    timer = time.time()

    # TODO enable this later
    pygame.mixer.music.load("resources/audio/bgm/underwater2.mp3")
    pygame.mixer.music.play(-1)

    for i in range(10000000):
        ### Process events
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            event.keys = keys
            if event.type == pygame.QUIT:
                return

            # For movements
            engine.event(event)

            # For mostly debug handling
            renderer.event(event)

        engine.update(keys)
        renderer.update(keys)
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
            logging.debug(f"fps: {60/(time.time() - timer)}")
            timer = time.time()
