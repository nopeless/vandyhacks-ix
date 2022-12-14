import numbers
import math
import functools
import importlib.util as iu
import logging
import os

import pygame
import config


def angle_to(pos1, pos2):
    p = pos2 - pos1
    return math.atan2(p.y, p.x)


def rot_center(image, angle, center):
    """
    Uses 1/64 increments to cache
    """
    return _rot_center(image, 32 / math.pi * angle // (math.pi / 32), center)


@functools.cache
def flip(image):
    return pygame.transform.flip(image, True, False)


@functools.cache
def _rot_center(image, angle, center):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(center=center).center)

    return rotated_image, new_rect


def clamp(s, n, l):
    if n < s:
        return s
    if n > l:
        return l
    return n


def load_module(filepath):
    file = os.path.basename(filepath)
    spec = iu.spec_from_file_location(file, filepath)
    if not spec:
        raise ImportError(f"{filepath} is not a valid module")

    module = iu.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def splice_image(source_img, width, height, x, y):
    rect = pygame.Rect(0, 0, width, height)
    surf = pygame.Surface(rect.size, pygame.SRCALPHA).convert_alpha()
    surf.blit(source_img, (0, 0), (x, y, x + width, y + height))
    return surf


def is_number(n):
    return isinstance(n, numbers.Number)


class Counter:
    """
    Supports floats as well
    """

    def __init__(self, loop):
        self._counter = 0
        self.loop = loop

    @property
    def counter(self):
        return self._counter

    @counter.setter
    def counter(self, value):
        self._counter = value % self.loop

    def __add__(self, other):
        self.counter += int(other)
        return self

    def __int__(self):
        return int(self.counter)

    def __float__(self):
        return float(self.counter)


def debug_arguments(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(e)
            logging.error(f"^ while calling {func.__name__}({args}, {kwargs})")

    return wrapper
