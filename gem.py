import pyasge

class Gem:
    def __init__(self, data, spawn: pyasge.Point2D):
        self.value = 15
        self.sprite = pyasge.Sprite()
        self.sprite.loadTexture("/data/images/jewel.png")
        self.sprite.x = spawn.x - self.sprite.width * 0.5
        self.sprite.y = spawn.y - self.sprite.height * 0.5
        self.hasBeenCollected = False