import pyasge
from fsm import FSM
from player import Player
from projetiles import Projectiles


class Enemy:
    def __init__(self, start_pos: pyasge.Point2D):
        self.sprite = pyasge.Sprite()
        self.sprite.loadTexture("/data/images/character_zombie_idle.png")
        self.sprite.scale = 0.35

        # self.player_location = Player.get_sprite()
        self.sprite.x = start_pos.x
        self.sprite.y = start_pos.y

        self.enemy_speed = 150
        self.velocity = pyasge.Point2D()
        self.facing = pyasge.Point2D(0, 1)

        # self.projectiles = Projectiles()

    def update(self):
        # self.player_location = Player.get_sprite()
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

        self.sprite.x = self.sprite.x + delta_x
        self.sprite.y = self.sprite.y + delta_y
