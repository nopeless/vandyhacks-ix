from types import SimpleNamespace

from managers import *

images = ImageManager("resources/images")
sfx = PygameSoundManager("resources/audio/sfx")

level = TMXManager("resources/level")

# Load sprites here
sprites = SimpleNamespace()