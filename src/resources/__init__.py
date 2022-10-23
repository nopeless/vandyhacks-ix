from types import SimpleNamespace

from managers import *

from lib import Player

images = ImageManager("resources/images")
sfx = PygameSoundManager("resources/audio/sfx")

level = TMXManager("resources/level")

# Load sprites here
sprites = SimpleNamespace()

sprites.player = Player(images.player.hitbox)
sprites.player.hitbox = images.player.hitbox
