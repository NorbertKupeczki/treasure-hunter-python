import pyasge


class Bullet:
    def __init__(self, spawn: pyasge.Point2D, direction: pyasge.Point2D):
        self.speed = 500
        self.velocity = pyasge.Point2D(direction)
        self.sprite = pyasge.Sprite()
        self.sprite.loadTexture("/data/images/bullet.png")
        self.sprite.x = spawn.x - self.sprite.width * 0.5
        self.sprite.y = spawn.y - self.sprite.height * 0.5
        self.traveled_distance = 0.0



