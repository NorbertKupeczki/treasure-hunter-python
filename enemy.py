import pyasge
from fsm import FSM
from damagestates import DamageStates

from player import Player
from projetiles import Projectiles


class Enemy:
    def __init__(self, data, start_pos: pyasge.Point2D):
        self.data = data
        self.sprite = pyasge.Sprite()
        self.sprite.loadTexture("/data/images/character_zombie_idle.png")
        self.sprite.scale = 0.35

        # self.player_location = Player.get_sprite()
        self.sprite.x = start_pos.x
        self.sprite.y = start_pos.y

        self.enemy_speed = 150
        self.velocity = pyasge.Point2D()
        self.facing = pyasge.Point2D(0, 1)

        self.hp = 10
        self.fsm = FSM()
        # self.projectiles = Projectiles()

    def update(self):
        # self.player_location = Player.get_sprite()
        self.fsm.update()
        pass

    def move_enemy(self, game_time: pyasge.GameTime, player_location: pyasge.Point2D):

        if abs(int(player_location.x) - int(self.sprite.x)) < 2:
            self.velocity.x = 0
        elif player_location.x > self.sprite.x:
            self.velocity.x = 1
        elif player_location.x < self.sprite.x:
            self.velocity.x = -1

        if abs(int(player_location.y) - int(self.sprite.y)) < 2:
            self.velocity.y = 0
        elif player_location.y > self.sprite.y:
            self.velocity.y = 1
        elif player_location.y < self.sprite.y:
            self.velocity.y = -1

        delta_x = self.enemy_speed * self.velocity.x * game_time.fixed_timestep
        delta_y = self.enemy_speed * self.velocity.y * game_time.fixed_timestep

        # delta_xy = self.check_collision(delta_x, delta_y) <-- Temporary disabled

        self.sprite.x = self.sprite.x + delta_x
        self.sprite.y = self.sprite.y + delta_y

    ## Will be removed when implementation of the A* Pathfinding script is done
    def check_collision(self, dx: float, dy: float) -> pyasge.Point2D():
        bounds = [self.sprite.getWorldBounds().v1,
                  self.sprite.getWorldBounds().v2,
                  self.sprite.getWorldBounds().v3,
                  self.sprite.getWorldBounds().v4]

        for x in bounds:
            if not self.is_passable(pyasge.Point2D(x.x + dx, x.y)):
                dx = 0
            if not self.is_passable(pyasge.Point2D(x.x, x.y + dy)):
                dy = 0

        return pyasge.Point2D(dx, dy)
