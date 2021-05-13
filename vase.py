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

        self.prev_vase_condition = VaseConditions.INTACT
        self.current_vase_condition = VaseConditions.INTACT

        self.fsm = FSM()
        self.fsm.setstate(self.update_intact)

    def check_collision(self, bullet: pyasge.Sprite()):
        if (bullet.x + bullet.width > self.sprite.x) and (bullet.x < self.sprite.x + self.sprite.width):
            if (bullet.y + bullet.height > self.sprite.y) and (bullet.y < self.sprite.y + self.sprite.height):
                return True
        else:
            return False

    def update(self, dt: float) -> None:

        #updating the state machine
        self.fsm.update()

        if self.current_vase_condition != self.prev_vase_condition:
            self.prev_vase_condition = self.current_vase_condition
            self.redraw()

    def redraw(self):
        if self.current_vase_condition < 4:
            self.sprite.loadTexture(self.imageList[self.current_vase_condition])

    def update_intact(self):
        self.current_vase_condition = VaseConditions.INTACT
        # self.sprite.loadTexture("/data/images/vaseDamage0.png")
        if self.hp < 5:
            self.fsm.setstate(self.update_cracked)

    def update_cracked(self):
        self.current_vase_condition = VaseConditions.CRACKED
        # self.sprite.loadTexture("/data/images/vaseDamage1.png")
        if self.hp < 3:
            self.fsm.setstate(self.update_very_cracked)

    def update_very_cracked(self):
        self.current_vase_condition = VaseConditions.VERY_CRACKED
        # self.sprite.loadTexture("/data/images/vaseDamage2.png")
        if self.hp < 1:
            self.fsm.setstate(self.update_broken)

    def update_broken(self):
        self.current_vase_condition = VaseConditions.BROKEN
        self.gem.spawnGem = True
        # self.sprite.loadTexture("/data/images/vaseDamage3.png")



