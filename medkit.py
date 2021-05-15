import pyasge

class Medkit:
    def __init__(self, spawn: pyasge.Point2D):
        self.id = 2
        self.sprite = pyasge.Sprite()
        self.sprite.loadTexture("/data/images/medkit.png")
        self.sprite.x = spawn.x - self.sprite.width * 0.5
        self.sprite.y = spawn.y - self.sprite.height * 0.5
        self.spawnGem = True

    def check_collision(self, player: pyasge.Sprite()):
        if (player.x + player.width > self.sprite.x) and (player.x < self.sprite.x + self.sprite.width):
            if (player.y + player.height > self.sprite.y) and (player.y < self.sprite.y + self.sprite.height):
                return True
        else:
            return False