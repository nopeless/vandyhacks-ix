import math
import random

from .animation import BaseAnimation


class EaseOut(BaseAnimation):
    """
    0 to 1
    """

    def __init__(self, duration):
        def func(clock):
            return 1 - (self.clock / duration) ** 2

        super().__init__(func=func, loop=duration, once=True)


class Bounce(BaseAnimation):
    def __init__(self, loop, low, high):
        def func(clock):
            return low + (high - low) * abs(math.sin(2 * math.pi * clock / loop))

        super().__init__(func=func)


class Shake(BaseAnimation):
    def __init__(self, left, right):
        def func(clock):
            if clock % 3 == 0:
                return left + (right - left) * random.random()
            return self.value

        super().__init__(func=func)
