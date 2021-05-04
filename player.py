import pyasge
from typing import Tuple


class Player:
    def __init__(self, screen_size: Tuple[int, int]):
        self.sprite = pyasge.Sprite()
        self.screen_size = screen_size
        self.sprite.loadTexture("/data/images/man_spritesheet.png")
        self.set_sprite(402, 50)
        self.sprite.x = screen_size[0] * 0.5 - self.sprite.width * 0.5
        self.sprite.y = screen_size[1] * 0.5 - self.sprite.height * 0.5
        self.player_speed = 500
        self.velocity = pyasge.Point2D()
        self.game_pad_enabled = False  # <-- Change this to true to switch to game pad controls instead of keyboard

    def move_player(self, game_time: pyasge.GameTime, keys, game_pad):
        if keys[pyasge.KEYS.KEY_W]:
            self.velocity.y = -1
        elif keys[pyasge.KEYS.KEY_S]:
            self.velocity.y = 1
        else:
            self.velocity.y = 0

        if keys[pyasge.KEYS.KEY_A]:
            self.velocity.x = -1
        elif keys[pyasge.KEYS.KEY_D]:
            self.velocity.x = 1
        else:
            self.velocity.x = 0

        if game_pad.connected and self.game_pad_enabled:
            self.velocity.x = game_pad.x
            self.velocity.y = game_pad.y

        if self.velocity.y < 0:
            self.set_sprite(47, 46)
        elif self.velocity.y > 0:
            self.set_sprite(402, 50)

        if self.velocity.x < 0:
            self.set_sprite(268, 46)
        elif self.velocity.x > 0:
            self.set_sprite(226, 46)

        delta_x = self.player_speed * self.velocity.x * game_time.fixed_timestep
        delta_y = self.player_speed * self.velocity.y * game_time.fixed_timestep

        self.check_collision(delta_x, delta_y)

        self.sprite.x = self.sprite.x + self.player_speed * self.velocity.x * game_time.fixed_timestep
        self.sprite.y = self.sprite.y + self.player_speed * self.velocity.y * game_time.fixed_timestep

    def set_sprite(self, x_start, width):
        self.sprite.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = x_start
        self.sprite.src_rect[pyasge.Sprite.SourceRectIndex.LENGTH_X] = width
        self.sprite.width = width

    def check_collision(self, dx, dy):  # <--- Checks collision with the edge of the screen
        if self.sprite.x + dx > (self.screen_size[0] - 46):
            self.sprite.x = self.screen_size[0] - 46
            self.velocity.x = 0
        elif self.sprite.x + dx < 0:
            self.sprite.x = 0
            self.velocity.x = 0

        if self.sprite.y + dy > (self.screen_size[1] - 62):
            self.sprite.y = self.screen_size[1] - 62
            self.velocity.y = 0
        elif self.sprite.y + dy < 0:
            self.sprite.y = 0
            self.velocity.y = 0
