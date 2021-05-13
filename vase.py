import pyasge
from gem import Gem
from fsm import FSM
from vaseconditions import VaseConditions

class Vase:
    def __init__(self, spawn: pyasge.Point2D):
        self.sprite = pyasge.Sprite()
        self.sprite.x = spawn.x - self.sprite.width * 0.5
        self.sprite.y = spawn.y - self.sprite.height * 0.5
        self.imageList = ["/data/images/vaseDamage0.png", "/data/images/vaseDamage1.png", "/data/images/vaseDamage2.png", "/data/images/vaseDamage3.png"]
        self.sprite.loadTexture("/data/images/vaseDamage0.png")
        self.gem = Gem(spawn)
        self.gem.spawnGem = False
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

    def redraw(self):
        index = int(self.condition)
        self.sprite.loadTexture(self.imageList[index])

    def update_intact(self):
        self.condition = VaseConditions.INTACT
        self.sprite.loadTexture("/data/images/vaseDamage0.png")
        if self.hp < 5:
            self.fsm.setstate(self.update_cracked())

    def update_cracked(self):
        self.condition = VaseConditions.CRACKED
        self.sprite.loadTexture("/data/images/vaseDamage1.png")
        if self.hp < 4:
            self.fsm.setstate(self.update_very_cracked())

    def update_very_cracked(self):
        self.condition = VaseConditions.VERY_CRACKED
        self.sprite.loadTexture("/data/images/vaseDamage2.png")
        if self.hp < 1:
            self.fsm.setstate(self.update_broken())

    def update_broken(self):
        self.condition = VaseConditions.BROKEN
        self.gem.spawnGem = True
        self.sprite.loadTexture("/data/images/vaseDamage3.png")



