import pyasge
from player import Player

class Gem:
    def __init__(self, spawn: pyasge.Point2D):
        self.value = 15
        self.sprite = pyasge.Sprite()
        self.sprite.loadTexture("/data/images/jewel.png")
        self.sprite.x = spawn.x - self.sprite.width * 0.5
        self.sprite.y = spawn.y - self.sprite.height * 0.5
        self.hasBeenCollected = False
        self.scoreFlag = False


    def collectGem(self, player : pyasge.Sprite()):

        if (self.hasBeenCollected == False):
            if (player.x + player.width > self.sprite.x) and (player.x < self.sprite.x + self.sprite.width):
                if (player.y + player.height > self.sprite.y) and (player.y < self.sprite.y + self.sprite.height):
                    self.hasBeenCollected = True
                    self.scoreFlag = True
        else:
            self.scoreFlag = False



