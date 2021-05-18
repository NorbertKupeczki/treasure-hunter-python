import math
import pyasge
from fsm import FSM
from enum import IntEnum
from A_star_pathfinding import Pathfinding


class EnemyMain:
    def __init__(self, data, start_pos: pyasge.Point2D) -> None:
        self.data = data
        self.states = ["/data/images/character_zombie_healthy.png",
                       "/data/images/character_zombie_damaged.png",
                       "/data/images/character_zombie_verydamaged.png",
                       "/data/images/character_zombie_neardead.png",
                       "/data/images/character_zombie_dead.png"]

        self.sprite = pyasge.Sprite()
        self.desired_path = []

        self.old_player_pos = pyasge.Point2D(0, 0)

        self.starting_hp = 1
        self.current_hp = 1
        self.hpPercentage = (self.current_hp / self.starting_hp) * 100
        self.fsm = FSM()
        self.fsm.setstate(self.update_healthy)
        self.current_enemy_condition = DamageStates.HEALTHY
        self.previous_enemy_condition = DamageStates.HEALTHY

        self.velocity = pyasge.Point2D()
        self.facing = pyasge.Point2D(0, 1)

        self.sprite.loadTexture(self.states[0])
        self.sprite.z_order = self.data.z_order['enemy']

        self.enemy_speed = None

        self.sprite.x = start_pos.x * self.data.tile_size
        self.sprite.y = start_pos.y * self.data.tile_size

        self.range = None
        self.enraged = False
        self.re_calc = False
        self.saved_tile = (self.sprite.x, self.sprite.y)
        self.enemy_curr_tile_cord = (self.sprite.x, self.sprite.y)

    def distanceToPlayer(self, x, y, enemy_tile):  # distance from the player in tile form

        dx = abs(x - enemy_tile[0])
        dy = abs(y - enemy_tile[1])

        return math.sqrt(dx * dx + dy * dy)

    def playerZombieCollision(self, player_location_tile: pyasge.Sprite()):
        if player_location_tile.x == self.enemy_curr_tile_cord[0]\
                and player_location_tile.y == self.enemy_curr_tile_cord[1]:
            return True
        else:
            return False

    def update(self):
        self.hpPercentage = (self.current_hp / self.starting_hp) * 100
        self.fsm.update()

        if self.hpPercentage < 100 and not self.enraged:
            self.range *= 2
            self.enraged = True

        if self.current_enemy_condition != self.previous_enemy_condition:
            self.redraw()
            self.previous_enemy_condition = self.current_enemy_condition

    def redraw(self):
        self.sprite.loadTexture(self.states[self.current_enemy_condition])

    def update_healthy(self):
        self.current_enemy_condition = DamageStates.HEALTHY
        if self.hpPercentage < 100:
            self.current_enemy_condition = DamageStates.DAMAGED
            self.fsm.setstate(self.update_damaged)

    def update_damaged(self):
        if self.hpPercentage <= 70:
            self.current_enemy_condition = DamageStates.VERY_DAMAGED
            self.fsm.setstate(self.update_verydamaged)

    def update_verydamaged(self):
        if self.hpPercentage <= 30:
            self.current_enemy_condition = DamageStates.NEAR_DEAD
            self.fsm.setstate(self.update_neardead)

    def update_neardead(self):
        if self.current_hp <= 0:
            self.current_enemy_condition = DamageStates.DEAD
            self.fsm.setstate(self.update_dead)

    def update_dead(self):
        self.current_enemy_condition = DamageStates.DEAD

    def re_path(self , x, y):
        self.desired_path.clear()
        if (self.data.map.cost_map[int(self.enemy_curr_tile_cord[1]) + 1][int(self.enemy_curr_tile_cord[0])] < 1000) and (int(self.enemy_curr_tile_cord[1] +1) != y and int(self.enemy_curr_tile_cord[0]) != x):  # go to the bottom
            self.desired_path = Pathfinding(self.enemy_curr_tile_cord, (int(self.enemy_curr_tile_cord[0]), int(self.enemy_curr_tile_cord[1]) + 1),self.data.map.cost_map, self.data.map.width, self.data.map.height).decided_path
            self.facing = pyasge.Point2D(0, -1)

        elif (self.data.map.cost_map[int(self.enemy_curr_tile_cord[1]) - 1][int(self.enemy_curr_tile_cord[0])] < 1000 and (int(self.enemy_curr_tile_cord[1] - 1) != y and int(self.enemy_curr_tile_cord[0]) != x)):  # go to the top
            self.desired_path = Pathfinding(self.enemy_curr_tile_cord, (int(self.enemy_curr_tile_cord[0]), int(self.enemy_curr_tile_cord[1]) - 1), self.data.map.cost_map, self.data.map.width,self.data.map.height).decided_path
            self.facing = pyasge.Point2D(0, 1)

        elif (self.data.map.cost_map[int(self.enemy_curr_tile_cord[1])][int(self.enemy_curr_tile_cord[0]) - 1] < 1000 and (int(self.enemy_curr_tile_cord[1]) != y and int(self.enemy_curr_tile_cord[0] -1) != x)):  # go to the left
            self.desired_path = Pathfinding(self.enemy_curr_tile_cord, (int(self.enemy_curr_tile_cord[0]) - 1, int(self.enemy_curr_tile_cord[1])), self.data.map.cost_map, self.data.map.width, self.data.map.height).decided_path
            self.facing = pyasge.Point2D(1, 0)

        elif (self.data.map.cost_map[int(self.enemy_curr_tile_cord[1])][int(self.enemy_curr_tile_cord[0]) + 1] < 1000 and (int(self.enemy_curr_tile_cord[1]) != y and int(self.enemy_curr_tile_cord[0] +1 ) != x)) :  # go to the right
            self.desired_path = Pathfinding(self.enemy_curr_tile_cord,
                                            (int(self.enemy_curr_tile_cord[0]) + 1, int(self.enemy_curr_tile_cord[1])),
                                            self.data.map.cost_map, self.data.map.width,
                                            self.data.map.height).decided_path
            self.facing = pyasge.Point2D(-1, 0)

    def check_collision(self, delta: pyasge.Point2D) -> pyasge.Point2D():
        bounds = [self.sprite.getWorldBounds().v1,
                  self.sprite.getWorldBounds().v2,
                  self.sprite.getWorldBounds().v3,
                  self.sprite.getWorldBounds().v4]

        for x in bounds:
            if not self.is_passable(pyasge.Point2D(x.x + delta.x, x.y)):
                delta.x = 0
            if not self.is_passable(pyasge.Point2D(x.x, x.y + delta.y)):
                delta.y = 0

        return delta

    def is_passable(self, world_location: pyasge.Point2D()) -> bool:
        tile_loc = pyasge.Point2D(int(world_location.x / self.data.tile_size),
                                  int(world_location.y / self.data.tile_size))
        return not self.data.map.cost_map[int(tile_loc.y)][int(tile_loc.x)] >= 10000


class DamageStates(IntEnum):
    HEALTHY = 0
    DAMAGED = 1
    VERY_DAMAGED = 2
    NEAR_DEAD = 3
    DEAD = 4