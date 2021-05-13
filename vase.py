import pyasge
from fsm import FSM
from enum import IntEnum


class Vase:
    def __init__(self, spawn: pyasge.Point2D):
        self.sprite = pyasge.Sprite()
        self.sprite.x = spawn.x - self.sprite.width * 0.5
        self.sprite.y = spawn.y - self.sprite.height * 0.5
        self.imageList = ["/data/images/vaseDamage0.png",
                          "/data/images/vaseDamage2.png",
                          "/data/images/vaseDamage3.png"]
        self.sprite.loadTexture(self.imageList[0])
        self.hp = 2

        self.prev_vase_condition = VaseConditions.INTACT
        self.current_vase_condition = VaseConditions.INTACT

        self.fsm = FSM()
        self.fsm.setstate(self.update_intact)

    def update(self) -> None:
        self.fsm.update()

        if self.current_vase_condition != self.prev_vase_condition:
            self.redraw()
            self.prev_vase_condition = self.current_vase_condition

    def redraw(self):
        self.sprite.loadTexture(self.imageList[self.current_vase_condition])

    def update_intact(self):
        if self.hp <= 1:
            self.fsm.setstate(self.update_cracked)
            self.current_vase_condition = VaseConditions.CRACKED

    def update_cracked(self):
        if self.hp <= 0:
            self.fsm.setstate(self.update_broken())
            self.current_vase_condition = VaseConditions.BROKEN

    def update_broken(self):
        self.current_vase_condition = VaseConditions.BROKEN


class VaseConditions(IntEnum):
    INTACT = 0
    CRACKED = 1
    BROKEN = 2

