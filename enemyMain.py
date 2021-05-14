import math
import pyasge
from fsm import FSM
from damagestates import DamageStates





class EnemyMain:
    def __init__(self, data, start_pos: pyasge.Point2D, Range, health, speed) -> None:

        self.states = ["/data/images/character_zombie_healthy.png",
                       "/data/images/character_zombie_damaged.png",
                       "/data/images/character_zombie_verydamaged.png",
                       "/data/images/character_zombie_neardead.png",
                       "/data/images/character_zombie_dead.png"]

        self.sprite = pyasge.Sprite()
        self.desired_path = []

        self.old_player_pos = pyasge.Point2D(0, 0)

        self.hp = health  # state machine stuff
        self.fsm = FSM()
        self.fsm.setstate(self.update_healthy)
        self.current_condition = DamageStates.HEALTHY
        self.previous_condition = DamageStates.HEALTHY

        self.velocity = pyasge.Point2D()
        self.facing = pyasge.Point2D(0, 1)

        self.sprite.loadTexture(self.states[0])

        self.enemy_speed = speed

        self.data = data

        self.sprite.x = start_pos.x
        self.sprite.y = start_pos.y

        self.range = Range


    def distanceToPlayer(self, x, y, enemy_tile):  # distance from the player in tile form

        dx = abs(x - enemy_tile[0])
        dy = abs(y - enemy_tile[1])

        return math.sqrt(dx * dx + dy * dy)


    def update(self):
        self.fsm.update()

        if self.current_condition != self.previous_condition:

            self.previous_condition = self.current_condition
            self.redraw()

    def redraw(self):
        if self.current_condition < DamageStates.DEAD:
            if self.current_condition == DamageStates.HEALTHY:
                self.sprite.loadTexture(self.states[0])
            elif self.current_condition == DamageStates.DAMAGED:
                self.sprite.loadTexture(self.states[1])
            elif self.current_condition == DamageStates.VERY_DAMAGED:
                self.sprite.loadTexture(self.states[2])
            elif self.current_condition == DamageStates.NEAR_DEAD:
                self.sprite.loadTexture(self.states[3])
        else:
            self.sprite.loadTexture(self.states[4])

    def update_healthy(self):
        self.current_condition = DamageStates.HEALTHY
        if self.hp <= 7:
            self.fsm.setstate(self.update_damaged)

    def update_damaged(self):
        self.current_condition = DamageStates.DAMAGED
        if self.hp <= 4:
            self.fsm.setstate(self.update_verydamaged)

    def update_verydamaged(self):
        self.current_condition = DamageStates.VERY_DAMAGED
        if self.hp <= 2:
            self.fsm.setstate(self.update_neardead)

    def update_neardead(self):
        self.current_condition = DamageStates.NEAR_DEAD
        if self.hp <= 0:
            self.fsm.setstate(self.update_dead)

    def update_dead(self):
        self.current_condition = DamageStates.DEAD