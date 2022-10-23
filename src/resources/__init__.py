from types import SimpleNamespace

from managers import *

sfx = PygameSoundManager("resources/audio/sfx")

from lib import Player, PlayerCleaner, Image, SourceGif

images = ImageManager("resources/images")
bgm = PygameSoundManager("resources/audio/bgm")

level = TMXManager("resources/level")

images.player.walk = SourceGif(images.player.sheet.walk, 5).instance
images.player.run = SourceGif(images.player.sheet.run, 5).instance
images.player.idle = SourceGif(images.player.sheet.idle, 10).instance
images.player.fall = SourceGif(images.player.sheet.fall, 10).instance
images.player.dash = SourceGif(images.player.sheet.dash, 10).instance

images.cleaner.idle = SourceGif(images.cleaner.sheet.idle, 10).instance
images.cleaner.sucking = SourceGif(images.cleaner.sheet.sucking, 30).instance

images.trash.banana = Image(images.trash.banana)
images.trash.chum = Image(images.trash.chum)
images.trash.plasticrings = Image(images.trash.plasticrings)
images.trash.sodacan = Image(images.trash.sodacan)

# Load sprites here
sprites = SimpleNamespace()

cleaner = PlayerCleaner(images.cleaner.sucking)

sprites.player = Player(images.player.idle, cleaner)
sprites.player.hitbox = images.player.hitbox
