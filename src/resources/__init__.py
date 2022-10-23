from types import SimpleNamespace

from managers import *

sfx = PygameSoundManager("resources/audio/sfx")

from lib import Player, Image, SourceGif

images = ImageManager("resources/images")
bgm = PygameSoundManager("resources/audio/bgm")

level = TMXManager("resources/level")

images.player.walk = SourceGif(images.player.sheet.walk, 5).instance
images.player.run = SourceGif(images.player.sheet.run, 5).instance
images.player.idle = SourceGif(images.player.sheet.idle, 10).instance
# TODO fix this
images.player.fall = SourceGif(images.player.sheet.idle, 10).instance
images.player.dash = SourceGif(images.player.sheet.idle, 10).instance

# Load sprites here
sprites = SimpleNamespace()


sprites.player = Player(images.player.idle)
sprites.player.hitbox = images.player.hitbox
