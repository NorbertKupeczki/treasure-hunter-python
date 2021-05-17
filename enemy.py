import pyasge
from A_star_pathfinding import Pathfinding
from pathfinder import PathFinder

from enemyMain import EnemyMain


class Enemy(EnemyMain):

    def __init__(self, data, start_pos: pyasge.Point2D) -> None:
        super().__init__(data, start_pos)
        self.range = 5
        self.current_hp = 5
        self.starting_hp = 5
        self.enemy_speed = 60
        self.pf = PathFinder(self.data)
        self.destination = None

    def move_enemy(self, game_time: pyasge.GameTime, player_location: pyasge.Point2D, player_location_tile: pyasge.Point2D):

        self.enemy_curr_tile_cord = (int(((self.sprite.x + self.sprite.width * 0.5) / self.data.tile_size)),
                                     int((self.sprite.y + self.sprite.height * 0.5) / self.data.tile_size))

        distance = EnemyMain.distanceToPlayer(self, player_location_tile.x, player_location_tile.y, self.enemy_curr_tile_cord)

        if distance < self.range:
            player_pos = player_location

            if (int(self.old_player_pos.x) != int(player_location_tile.x) or
               int(self.old_player_pos.y) != int(player_location_tile.y)) or self.re_calc:

                self.re_calc = False
                self.desired_path.clear()
                self.old_player_pos = player_location_tile

                if int(self.enemy_curr_tile_cord[0]) == int(player_location_tile.x) and int(self.enemy_curr_tile_cord[1]) == int(player_location_tile.y):
                    self.desired_path.clear()
                    self.destination = None

                else:
                    goal_tile = (int(player_location_tile.x), int(player_location_tile.y))
                    start_tile = (int(self.enemy_curr_tile_cord[0]), int(self.enemy_curr_tile_cord[1]))

                    # self.desired_path = Pathfinding(self.enemy_curr_tile_cord, (int(goal_tile[0]), int(goal_tile[1])),
                    #                                 self.data.map.cost_map, self.data.map.width,
                    #                                 self.data.map.height).decided_path
                    self.desired_path = self.pf.pathfinder(start_tile, goal_tile)

                    # if len(self.desired_path) > 30:
                    #     self.desired_path.clear()
                    #     pass
                    # else:
                    self.desired_path.pop()

            if self.desired_path:
                if self.destination is None:
                    self.destination = self.desired_path.pop(0)

            if self.destination is not None:
                player_pos.y = int(self.destination[1] * self.data.tile_size)
                player_pos.x = int(self.destination[0] * self.data.tile_size)

                if abs(int(self.destination[0] * self.data.tile_size) - int(self.sprite.x)) < 2:
                    self.velocity.x = 0
                elif player_pos.x > self.sprite.x:
                    self.velocity.x = 1
                elif player_pos.x < self.sprite.x:
                    self.velocity.x = -1

                if abs(int(self.destination[1] * self.data.tile_size) - int(self.sprite.y)) < 2:
                    self.velocity.y = 0
                elif player_pos.y > self.sprite.y:
                    self.velocity.y = 1
                elif player_pos.y < self.sprite.y:
                    self.velocity.y = -1

                delta_x = self.enemy_speed * self.velocity.x * game_time.fixed_timestep
                delta_y = self.enemy_speed * self.velocity.y * game_time.fixed_timestep

                self.sprite.x = self.sprite.x + delta_x
                self.sprite.y = self.sprite.y + delta_y

                curr_pos = pyasge.Point2D(self.sprite.x, self.sprite.y)
                dest_pos = pyasge.Point2D(self.destination[0] * self.data.tile_size,
                                          self.destination[1] * self.data.tile_size)

                if pyasge.Point2D.distance(curr_pos, dest_pos) <= 1.5:
                    self.destination = None
