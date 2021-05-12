import pyasge
from projetiles import Projectiles


class Player:
    def __init__(self, data, start_pos: pyasge.Point2D):
        self.data = data
        self.sprite = pyasge.Sprite()
        self.sprite.loadTexture("/data/images/man_spritesheet.png")
        self.set_sprite(int(402), int(50))
        self.sprite.z_order = 3
        self.sprite.x = start_pos.x
        self.sprite.y = start_pos.y
        self.player_speed = 300
        self.velocity = pyasge.Point2D()
        self.game_pad_enabled = False
        self.facing = pyasge.Point2D(0, 1)
        self.projectiles = Projectiles(data)

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
            self.facing = pyasge.Point2D(0, -1)
        elif self.velocity.y > 0:
            self.set_sprite(402, 50)
            self.facing = pyasge.Point2D(0, 1)

        if self.velocity.x < 0:
            self.set_sprite(268, 46)
            self.facing = pyasge.Point2D(-1, 0)
        elif self.velocity.x > 0:
            self.set_sprite(226, 46)
            self.facing = pyasge.Point2D(1, 0)

        delta_x = self.player_speed * self.velocity.x * game_time.fixed_timestep
        delta_y = self.player_speed * self.velocity.y * game_time.fixed_timestep

        delta_xy = self.check_collision(delta_x, delta_y)

        self.sprite.x = self.sprite.x + delta_xy.x
        self.sprite.y = self.sprite.y + delta_xy.y

    def set_sprite(self, x_start: int, width: int):
        self.sprite.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = int(x_start)
        self.sprite.src_rect[pyasge.Sprite.SourceRectIndex.LENGTH_X] = int(width)
        self.sprite.width = int(width)

    def get_sprite(self) -> pyasge.Point2D:
        sprite_centre = pyasge.Point2D(self.sprite.x + self.sprite.width * 0.5, self.sprite.y + self.sprite.height * 0.5)
        self.data.world_loc = sprite_centre
        self.data.tile_loc = pyasge.Point2D(int(sprite_centre.x / self.data.tile_size), int(sprite_centre.y / self.data.tile_size))
        return sprite_centre

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

    def toggle_game_pad(self) -> bool:
        self.game_pad_enabled = not self.game_pad_enabled
        return self.game_pad_enabled

    def shoot(self):
        spawn_point = pyasge.Point2D(self.sprite.x + self.sprite.width * 0.5, self.sprite.y + self.sprite.height * 0.5)
        self.projectiles.shoot(spawn_point, self.facing)

    def render_bullets(self, renderer):
        for bullets in self.projectiles.projectiles:
            renderer.render(bullets.sprite)

    def is_passable(self, world_location: pyasge.Point2D()) -> bool:
        tile_loc = pyasge.Point2D(int(world_location.x / self.data.tile_size),
                                  int(world_location.y / self.data.tile_size))

        if self.data.map.cost_map[int(tile_loc.y)][int(tile_loc.x)] >= 10000:
            return False
        else:
            return True
