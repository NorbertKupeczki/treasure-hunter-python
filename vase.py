import pyasge
from gem import Gem
from layer import Layer

class Vase:
    def __init__(self, spawn: pyasge.Point2D):
        self.sprite = pyasge.Sprite()
        self.sprite.loadTexture("/data/images/vaseDamage0.png")
        self.sprite.x = spawn.x - self.sprite.width * 0.5
        self.sprite.y = spawn.y - self.sprite.height * 0.5
        self.imageList = ["/data/images/vaseDamage0.png", "/data/images/vaseDamage1.png", "/data/images/vaseDamage2.png"]
        self.gem = Gem(spawn)
        self.health = 2
