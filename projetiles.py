import pyasge
from bullet import Bullet, BulletType
from gem import Gem


class Projectiles:
    def __init__(self, data):
        self.data = data
        self.projectiles = []

    def shoot(self, spawn: pyasge.Point2D, direction: pyasge.Point2D):
        self.projectiles.append(Bullet(spawn, direction, 'player'))

    def zombie_shoot(self, spawn: pyasge.Point2D, direction: pyasge.Point2D):
        self.projectiles.append(Bullet(spawn, direction, 'enemy'))

    def update_projectiles(self, game_time: pyasge.GameTime, player):
        for bullet in self.projectiles:
            bullet.sprite.x = bullet.sprite.x + bullet.speed * bullet.velocity.x * game_time.fixed_timestep
            bullet.sprite.y = bullet.sprite.y + bullet.speed * bullet.velocity.y * game_time.fixed_timestep

            if bullet.bullet_type == BulletType.Player:

                for enemy in self.data.enemies:
                    if self.check_collision(bullet.centre(), enemy.sprite):
                        self.data.enemies.remove(enemy)
                        self.projectiles.remove(bullet)

                for vase in self.data.breakables:
                    if self.check_collision(bullet.centre(), vase.sprite) and vase.hp > 0:
                        vase.hp -= 1
                        print(vase.hp)
                        vase.update()
                        if vase.hp <= 0:
                            self.projectiles.remove(bullet)
                            x = int(vase.sprite.x / self.data.tile_size)
                            y = int(vase.sprite.y / self.data.tile_size)
                            self.data.map.cost_map[int(y)][int(x)] = 1
                            self.data.gems.append(Gem(pyasge.Point2D((x + 0.5) * self.data.tile_size,
                                                                     (y + 0.5) * self.data.tile_size)))
            elif bullet.bullet_type == BulletType.Enemy:
                if self.check_collision(bullet.centre(), player.sprite):
                    self.projectiles.remove(bullet)
                    return True

            if not self.is_passable(bullet.centre()):
                self.projectiles.remove(bullet)

    def is_passable(self, world_location: pyasge.Point2D()) -> bool:
        tile_loc = pyasge.Point2D(int(world_location.x / self.data.tile_size),
                                  int(world_location.y / self.data.tile_size))

        if self.data.map.cost_map[int(tile_loc.y)][int(tile_loc.x)] >= 10000:
            return False
        else:
            return True

    def check_collision(self, bullet: pyasge.Point2D, enemy: pyasge.Sprite) -> bool:
        if (enemy.x < bullet.x) and (bullet.x < enemy.x + enemy.width):
            if (enemy.y < bullet.y) and (bullet.y < enemy.y + enemy.height):
                return True
        else:
            return False
