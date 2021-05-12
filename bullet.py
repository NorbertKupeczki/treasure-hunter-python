import pyasge


class Bullet:
    def __init__(self, spawn: pyasge.Point2D, direction: pyasge.Point2D):
        self.speed = 500
        self.velocity = pyasge.Point2D(direction)
        self.sprite = pyasge.Sprite()
        self.sprite.loadTexture("/data/images/bullet2.png")
        self.set_facing(direction)
        self.sprite.x = spawn.x - self.sprite.width * 0.5
        self.sprite.y = spawn.y - self.sprite.height * 0.5
        self.traveled_distance = 0.0

    def centre(self) -> pyasge.Point2D:
        sprite_centre = pyasge.Point2D(self.sprite.x + self.sprite.width * 0.5, self.sprite.y + self.sprite.height * 0.5)
        return sprite_centre

    def set_facing(self, direction: pyasge.Point2D):
        if direction.x > 0:
            pass
        elif direction.x < 0:
            self.sprite.flip_flags = pyasge.Sprite.FlipFlags.FLIP_X
        elif direction.y > 0:
            self.sprite.rotation = 90 * 3.1415 / 180
        else:
            self.sprite.rotation = - 90 * 3.1415 / 180

