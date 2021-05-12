import pyasge
from bullet import Bullet


class Projectiles:
    def __init__(self, data):
        self.data = data
        self.projectiles = []

    def shoot(self, spawn: pyasge.Point2D, direction: pyasge.Point2D):
        self.projectiles.append(Bullet(spawn, direction))

    def update_projectiles(self, game_time: pyasge.GameTime):
        for bullet in self.projectiles:
            bullet.sprite.x = bullet.sprite.x + bullet.speed * bullet.velocity.x * game_time.fixed_timestep
            bullet.sprite.y = bullet.sprite.y + bullet.speed * bullet.velocity.y * game_time.fixed_timestep

            if not self.is_passable(bullet.centre()):
                self.projectiles.remove(bullet)

    def is_passable(self, world_location: pyasge.Point2D()) -> bool:
        tile_loc = pyasge.Point2D(int(world_location.x / self.data.tile_size),
                                  int(world_location.y / self.data.tile_size))

        if self.data.map.cost_map[int(tile_loc.y)][int(tile_loc.x)] >= 10000:
            return False
        else:
            return True
