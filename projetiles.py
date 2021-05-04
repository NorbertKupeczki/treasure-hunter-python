import pyasge
from bullet import Bullet


class Projectiles:
    def __init__(self):
        self.projectiles = []

    def shoot(self, spawn: pyasge.Point2D, direction: pyasge.Point2D):
        self.projectiles.append(Bullet(spawn, direction))

    def update_projectiles(self, game_time: pyasge.GameTime):
        for bullet in self.projectiles:
            bullet.sprite.x = bullet.sprite.x + bullet.speed * bullet.velocity.x * game_time.fixed_timestep
            bullet.sprite.y = bullet.sprite.y + bullet.speed * bullet.velocity.y * game_time.fixed_timestep
            bullet.traveled_distance += bullet.speed * bullet.velocity.x * game_time.fixed_timestep + bullet.sprite.y + bullet.speed * bullet.velocity.y * game_time.fixed_timestep

            if bullet.traveled_distance > 15000:
                self.projectiles.remove(bullet)
