import pyasge
from enum import Enum


class Bullet:
    def __init__(self, spawn: pyasge.Point2D, direction: pyasge.Point2D, bullet_type: str, z_order: int):
        self.speed = 600
        self.velocity = pyasge.Point2D(direction)
        self.sprite = pyasge.Sprite()
        self.bullet_type = None
        self.textures = {
            'player': "/data/images/bullet2.png",
            'enemy': "/data/images/acid.png"
        }
        self.set_bullet_type(bullet_type)
        self.sprite.z_order = z_order
        self.set_facing(direction)
        self.sprite.x = spawn.x - self.sprite.width * 0.5
        self.sprite.y = spawn.y - self.sprite.height * 0.5

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
            # self.sprite.z_order = self.sprite.z_order + 3
        else:
            self.sprite.rotation = - 90 * 3.1415 / 180

    def set_bullet_type(self, bullet_type: str):
        if bullet_type == 'player':
            self.bullet_type = BulletType.Player
            self.sprite.loadTexture(self.textures['player'])
        elif bullet_type == 'powerup':
            self.bullet_type = BulletType.PowerUp
            self.sprite.loadTexture(self.textures['player'])
        elif bullet_type == 'enemy':
            self.bullet_type = BulletType.Enemy
            self.sprite.loadTexture(self.textures['enemy'])
            self.speed = 300


class BulletType(Enum):
    Enemy = 0
    Player = 1
    PowerUp = 2
