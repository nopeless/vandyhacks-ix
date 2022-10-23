from types import SimpleNamespace

from managers import *

from lib import Player, Image, SourceGif

images = ImageManager("resources/images")
sfx = PygameSoundManager("resources/audio/sfx")
bgm = PygameSoundManager("resources/audio/bgm")

level = TMXManager("resources/level")

images.playerc_walking_test = SourceGif(images.player.moves_c.moves, 5).instance
images.playere_walking_test = SourceGif(images.player.moves_e.moves, 8).instance

# Load sprites here
sprites = SimpleNamespace()


sprites.player = Player(images.player.hitbox)
sprites.player.hitbox = images.player.hitbox
