import pyasge
from enum import Enum


class Bullet:
    def __init__(self, spawn: pyasge.Point2D, direction: pyasge.Point2D, bullet_type: str):
        self.speed = 600
        self.velocity = pyasge.Point2D(direction)
        self.sprite = pyasge.Sprite()
        self.sprite.loadTexture("/data/images/bullet2.png")
        self.sprite.z_order = 3
        self.set_facing(direction)
        self.sprite.x = spawn.x - self.sprite.width * 0.5
        self.sprite.y = spawn.y - self.sprite.height * 0.5
        self.bullet_type = None
        if bullet_type == 'player':
            self.bullet_type = BulletType.Player
        elif bullet_type == 'enemy':
            self.bullet_type = BulletType.Enemy

    def centre(self) -> pyasge.Point2D:
        sprite_centre = pyasge.Point2D(self.sprite.x + self.sprite.width * 0.5,
                                       self.sprite.y + self.sprite.height * 0.5)
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


class BulletType(Enum):
    Enemy = 0,
    Player = 1
