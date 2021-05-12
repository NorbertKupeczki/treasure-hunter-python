import pyasge
from gem import Gem
from fsm import FSM
from vaseconditions import VaseConditions

class Vase:
    def __init__(self, spawn: pyasge.Point2D, IntEnum):
        self.sprite = pyasge.Sprite()
        self.sprite.x = spawn.x - self.sprite.width * 0.5
        self.sprite.y = spawn.y - self.sprite.height * 0.5
        self.imageList = ["/data/images/vaseDamage0.png", "/data/images/vaseDamage1.png", "/data/images/vaseDamage2.png"]
        self.sprite.loadTexture([self.imageList[0]])
        self.gem = Gem(spawn)
        self.hp = 5
        self.HEALTHY = 0
        self.DAMAGED = 1
        self.DESTROYED = 2
        self.condition = VaseConditions

    def check_collision(self, bullet: pyasge.Sprite()):
        if (bullet.x + bullet.width > self.sprite.x) and (bullet.x < self.sprite.x + self.sprite.width):
            if (bullet.y + bullet.height > self.sprite.y) and (bullet.y < self.sprite.y + self.sprite.height):
                return True
        else:
            return False

    def update_intact(self):
        self.condition = VaseConditions.INTACT
        self.sprite.loadTexture([self.imageList[0]])
        if self.hp < 5:
            self.condition = VaseConditions.CRACKED

    def update_cracked(self):
        self.condition = VaseConditions.CRACKED
        self.sprite.loadTexture([self.imageList[1]])
        if self.hp < 4:
            self.condition = VaseConditions.VERY_CRACKED

    def update_very_cracked(self):
        self.condition = VaseConditions.VERY_CRACKED
        self.sprite.loadTexture([self.imageList[2]])
        if self.hp < 1:
            self.condition = VaseConditions.BROKEN



