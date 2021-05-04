import pyasge
from typing import Tuple
from projetiles import Projectiles


class Player:
    def __init__(self, screen_size: Tuple[int, int]):
        self.sprite = pyasge.Sprite()
        self.screen_size = screen_size
        self.sprite.loadTexture("/data/images/man_spritesheet.png")
        self.set_sprite(402, 50)
        self.sprite.x = screen_size[0] * 0.5 - self.sprite.width * 0.5
        self.sprite.y = screen_size[1] * 0.5 - self.sprite.height * 0.5
        self.player_speed = 300
        self.velocity = pyasge.Point2D()
        self.game_pad_enabled = False  # <-- Change this to true to switch to game pad controls instead of keyboard
        self.facing = pyasge.Point2D(0, 1)
        self.projectiles = Projectiles()

    def move_player(self, game_time: pyasge.GameTime, keys, game_pad):
        if keys[pyasge.KEYS.KEY_W]:
            self.velocity.y = -1
            self.facing = pyasge.Point2D(0, -1)
        elif keys[pyasge.KEYS.KEY_S]:
            self.velocity.y = 1
            self.facing = pyasge.Point2D(0, 1)
        else:
            self.velocity.y = 0

        if keys[pyasge.KEYS.KEY_A]:
            self.velocity.x = -1
            self.facing = pyasge.Point2D(-1, 0)
        elif keys[pyasge.KEYS.KEY_D]:
            self.velocity.x = 1
            self.facing = pyasge.Point2D(1, 0)
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

        delta_xy = self.check_collision(delta_x, delta_y)

        self.sprite.x = self.sprite.x + delta_xy[0]
        self.sprite.y = self.sprite.y + delta_xy[1]

    def set_sprite(self, x_start, width):
        self.sprite.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = x_start
        self.sprite.src_rect[pyasge.Sprite.SourceRectIndex.LENGTH_X] = width
        self.sprite.width = width

    def check_collision(self, dx: float, dy: float) -> Tuple[float, float]:  # <--- Checks collision with the edge of the screen
        if self.sprite.x + dx > (self.screen_size[0] - self.sprite.width):
            self.sprite.x = self.screen_size[0] - self.sprite.width
            dx = 0
        elif self.sprite.x + dx < 0:
            self.sprite.x = 0
            dx = 0

        if self.sprite.y + dy > (self.screen_size[1] - self.sprite.height):
            self.sprite.y = self.screen_size[1] - self.sprite.height
            dy = 0
        elif self.sprite.y + dy < 0:
            self.sprite.y = 0
            dy = 0

        return dx, dy

    def toggle_game_pad(self) -> bool:
        self.game_pad_enabled = not self.game_pad_enabled
        return self.game_pad_enabled

    def shoot(self):
        spawn_point = pyasge.Point2D(self.sprite.x + self.sprite.width * 0.5, self.sprite.y + self.sprite.height * 0.5)
        self.projectiles.shoot(spawn_point, self.facing)

    def render_bullets(self, renderer):
        for bullets in self.projectiles.projectiles:
            renderer.render(bullets.sprite)

