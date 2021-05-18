import pyasge
import math
from projectiles import Projectiles


class Player:
    def __init__(self, data):
        self.data = data
        self.sprite = pyasge.Sprite()
        self.sprite.loadTexture("/data/images/player_sh.png")
        self.SPRITE_SIZE = pyasge.Point2D(int(self.sprite.getTexture().width * 0.334),
                                          int(self.sprite.getTexture().height * 0.25))
        self.sprite_sheet = {
            'walk_up': 0,
            'walk_right': 62,
            'walk_left': 124,
            'walk_down': 186
        }
        self.set_sprite(int(46), int(self.sprite_sheet['walk_down']))
        self.sprite.z_order = self.data.z_order['player']
        self.sprite.x = self.data.map.starting_location.x
        self.sprite.y = self.data.map.starting_location.y
        self.player_speed = 300
        self.velocity = pyasge.Point2D()
        self.game_pad_sensitivity = 0.2
        self.facing = pyasge.Point2D(0, 1)
        self.projectiles = Projectiles(data)
        self.RELOAD_TIME = 0.5
        self.reload_time = self.RELOAD_TIME
        self.elapsed_time = 0.0

        self.HEALTH = 5
        self.health = self.HEALTH

        self.INV_TIME = 1.2
        self.invulnerable = 0.0

    def update(self, game_time: pyasge.GameTime):
        if self.reload_time < self.RELOAD_TIME:
            self.reload_time += game_time.fixed_timestep

        self.projectiles.update_projectiles(game_time, self)

        if self.invulnerable > 0.02:
            self.invulnerable -= game_time.fixed_timestep
        elif 0.0 < self.invulnerable <= 0.02 or self.invulnerable < 0.0:
            self.invulnerable = 0.0

    def move_player(self, game_time: pyasge.GameTime, keys, game_pad):
        if game_pad.connected and self.data.game_pad_enabled:
            if abs(game_pad.x) > self.game_pad_sensitivity:
                self.velocity.x = game_pad.x
            else:
                self.velocity.x = 0
            if abs(game_pad.y) > self.game_pad_sensitivity:
                self.velocity.y = game_pad.y
            else:
                self.velocity.y = 0
            if self.data.inputs.getGamePad(0).RIGHT_TRIGGER != -1.0:
                self.shoot()
        else:
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

            if keys[pyasge.KEYS.KEY_SPACE]:
                self.shoot()

        if self.velocity.x != 0 or self.velocity.y != 0:
            animation_speed = math.sqrt(pow(self.velocity.x, 2) + pow(self.velocity.y, 2))
            animation_index = self.animation_controller(game_time, animation_speed)
            if self.velocity.y < 0:
                self.set_sprite(animation_index, int(self.sprite_sheet['walk_up']))
                self.facing = pyasge.Point2D(0, -1)
            elif self.velocity.y > 0:
                self.set_sprite(animation_index, int(self.sprite_sheet['walk_down']))
                self.facing = pyasge.Point2D(0, 1)

            if self.velocity.x < 0:
                self.set_sprite(animation_index, int(self.sprite_sheet['walk_left']))
                self.facing = pyasge.Point2D(-1, 0)
            elif self.velocity.x > 0:
                self.set_sprite(animation_index, int(self.sprite_sheet['walk_right']))
                self.facing = pyasge.Point2D(1, 0)

        delta = pyasge.Point2D(self.player_speed * self.velocity.x * game_time.fixed_timestep,
                               self.player_speed * self.velocity.y * game_time.fixed_timestep)

        delta = self.check_collision(delta)

        self.sprite.x = self.sprite.x + delta.x
        self.sprite.y = self.sprite.y + delta.y

    def set_sprite(self, x: int, y: int):
        self.sprite.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = int(x)
        self.sprite.src_rect[pyasge.Sprite.SourceRectIndex.START_Y] = int(y)
        self.sprite.src_rect[pyasge.Sprite.SourceRectIndex.LENGTH_X] = self.SPRITE_SIZE.x
        self.sprite.src_rect[pyasge.Sprite.SourceRectIndex.LENGTH_Y] = self.SPRITE_SIZE.y
        self.sprite.width = self.SPRITE_SIZE.x
        self.sprite.height = self.SPRITE_SIZE.y

    def get_sprite(self) -> pyasge.Point2D:
        sprite_centre = pyasge.Point2D(self.sprite.x + self.SPRITE_SIZE.x * 0.5,
                                       self.sprite.y + self.SPRITE_SIZE.y * 0.5)
        self.data.world_loc = sprite_centre
        self.data.tile_loc = pyasge.Point2D(int(sprite_centre.x / self.data.tile_size),
                                            int(sprite_centre.y / self.data.tile_size))
        return sprite_centre

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

    def toggle_game_pad(self) -> bool:
        self.data.game_pad_enabled = not self.data.game_pad_enabled
        return self.data.game_pad_enabled

    def max_heal(self):
        self.health = self.HEALTH

    def suffer_damage(self, health_bar) -> bool:
        if self.invulnerable:
            return False
        else:
            self.health -= 1
            self.invulnerable = self.INV_TIME
            health_bar.lose_health(self.health)
            return True

    def shoot(self):
        spawn_point = pyasge.Point2D(self.sprite.x + self.sprite.width * 0.5 + self.facing.x * 10,
                                     self.sprite.y + self.sprite.height * 0.5 + self.facing.y * 10)
        if self.reload_time >= self.RELOAD_TIME:
            self.projectiles.shoot(spawn_point, self.facing)
            self.reload_time = 0.0

    def render_bullets(self):
        for bullets in self.projectiles.projectiles:
            self.data.renderer.render(bullets.sprite)

    def is_passable(self, world_location: pyasge.Point2D()) -> bool:
        tile_loc = pyasge.Point2D(int(world_location.x / self.data.tile_size),
                                  int(world_location.y / self.data.tile_size))
        return not self.data.map.cost_map[int(tile_loc.y)][int(tile_loc.x)] >= 10000

    def animation_controller(self, game_time: pyasge.GameTime, speed_mod: float) -> int:
        if self.elapsed_time >= 1.0:
            self.elapsed_time = 0.0
        else:
            self.elapsed_time += game_time.fixed_timestep * speed_mod

        index = int(self.elapsed_time * 4)
        if index % 2 == 0:
            return int(index * 46)
        else:
            return int(46)

    def render(self):
        self.data.renderer.render(self.sprite)
        self.render_bullets()
