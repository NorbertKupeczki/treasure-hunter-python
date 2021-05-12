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
        self.gem.spawnGem = False
        self.health = 2
        self.spriteIndex = 0

    def destroyVase(self):
        pass

    def damage_vase(self):
        self.health -= 1


    def check_collision(self, bullet: pyasge.Sprite()):
        if (bullet.x + bullet.width > self.sprite.x) and (bullet.x < self.sprite.x + self.sprite.width):
            if (bullet.y + bullet.height > self.sprite.y) and (bullet.y < self.sprite.y + self.sprite.height):
                return True
        else:
            return False
