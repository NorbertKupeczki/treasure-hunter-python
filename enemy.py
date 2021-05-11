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

        self.sprite.x = self.sprite.x + delta_x
        self.sprite.y = self.sprite.y + delta_y
