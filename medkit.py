import pyasge
import random


class Medkit:
    def __init__(self, spawn: pyasge.Point2D):
        self.sprite = pyasge.Sprite()
        self.sprite.loadTexture("/data/images/medkit.png")
        self.sprite.x = spawn.x - self.sprite.width * 0.5
        self.sprite.y = spawn.y - self.sprite.height * 0.5

    def check_collision(self, player: pyasge.Sprite()):
        if (player.x + player.width > self.sprite.x) and (player.x < self.sprite.x + self.sprite.width):
            if (player.y + player.height > self.sprite.y) and (player.y < self.sprite.y + self.sprite.height):
                return True
        else:
            return False

    """
    Static methods can be called without the class being instantiated.
    The below method randomises the medkit drops based on the player's
    remaining health. - Norbert
    """
    @staticmethod
    def drop_medkit(player_hp: int):
        if player_hp < 5:
            chance = random.randint(1, 100)
            threshold = int((8 - player_hp * 1.5) * 10)
            if threshold > chance:
                return True
        else:
            return False
