import pyasge
from map import Map
from gem import Gem
from rangedEnemy import EnemyR
from enemy import Enemy
from vase import Vase


class MapLoader:
    def __init__(self):
        pass

    @staticmethod
    def load_game_map(data) -> None:
        data.map = Map(str(data.level_selected))
        data.gems = []
        data.enemies = []
        data.breakables = []
        data.collectibles = []

        for gem in data.map.layers[2].tiles:
            data.gems.append(Gem(pyasge.Point2D((gem.coordinate[0] + 0.5) * data.tile_size,
                                                (gem.coordinate[1] + 0.5) * data.tile_size),
                                 data.z_order['collectibles']))

        ranged_enemy_counter = 0
        for enemy in data.map.layers[3].tiles:
            ranged_enemy_counter += 1
            if ranged_enemy_counter == 3:
                data.enemies.append(EnemyR(data, pyasge.Point2D(enemy.coordinate[0], enemy.coordinate[1])))
                ranged_enemy_counter = 0
            else:
                data.enemies.append(Enemy(data, pyasge.Point2D(enemy.coordinate[0], enemy.coordinate[1])))

        for breakable in data.map.layers[4].tiles:
            data.breakables.append(Vase(pyasge.Point2D(breakable.coordinate[0] * data.tile_size,
                                                       breakable.coordinate[1] * data.tile_size),
                                        data.z_order['wall']))
