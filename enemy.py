import pyasge
from fsm import FSM
from player import Player
from projetiles import Projectiles


class Enemy:
    def __init__(self, start_pos: pyasge.Point2D):
        self.sprite = pyasge.Sprite()
        self.sprite.loadTexture("/data/images/character_zombie_idle.png")

        self.player_location = Player.get_sprite()
        self.enemy_location.x = start_pos.x
        self.enemy_location.y = start_pos.y

        self.enemy_speed = 150
        self.velocity = pyasge.Point2D()
        self.facing = pyasge.Point2D(0, 1)

        self.projectiles = Projectiles()

    def update(self):
        self.player_location = Player.get_sprite()

    def move_enemy(self, game_time: pyasge.GameTime):
        if self.player_location.x > self.enemy_location.x:
            self.velocity.x = -1
        elif self.player_location.x < self.enemy_location.x:
            self.velocity.x = 1
        else:
            self.velocity.x = 0

        if self.player_location.y > self.enemy_location.y:
            self.velocity.y = -1
        elif self.player_location < self.enemy_location.y:
            self.velocity.y = 1
        else:
            self.velocity.y = 0

        delta_x = self.enemy_speed * self.velocity.x * game_time.fixed_timestep
        delta_y = self.enemy_speed * self.velocity.y * game_time.fixed_timestep

        delta_xy = self.check_collision(delta_x, delta_y)

        self.sprite.x = self.sprite.x + delta_xy.x
        self.sprite.y = self.sprite.y + delta_xy.y

    ## Will be removed when implementating the A* Pathfinding script
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
