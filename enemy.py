import pyasge
from A_star_pathfinding import Pathfinding

from enemyMain import EnemyMain


class Enemy(EnemyMain):

    def __init__(self, data, start_pos: pyasge.Point2D, Range,health, speed) -> None:
        super().__init__(data, start_pos, Range,health ,speed)


    def move_enemy(self, game_time: pyasge.GameTime, player_location: pyasge.Point2D, player_location_tile: pyasge.Point2D):

        enemy_curr_tile_cord = (int(((self.sprite.x + self.sprite.width * 0.5) / self.data.tile_size)),
                                int((self.sprite.y + self.sprite.height * 0.5) / self.data.tile_size))



        distance = EnemyMain.distanceToPlayer(self,player_location_tile.x, player_location_tile.y, enemy_curr_tile_cord)

        if distance < self.range:

            curr_pos_prev = (self.sprite.x, self.sprite.y)

            player_pos = player_location

            if int(self.old_player_pos.x) != int(player_location_tile.x) or int(self.old_player_pos.y) != int(player_location_tile.y):

                self.desired_path.clear()
                self.old_player_pos = player_location_tile

                if int(enemy_curr_tile_cord[0]) == int(player_location_tile.x) and int(enemy_curr_tile_cord[1]) == int(player_location_tile.y):
                    #attack function call
                    self.desired_path.clear()

                else:
                    goal_tile = (player_location_tile.x, player_location_tile.y)

                    self.desired_path = Pathfinding(enemy_curr_tile_cord, (int(goal_tile[0]), int(goal_tile[1])),
                                                    self.data.map.cost_map, self.data.map.width,
                                                    self.data.map.height).decided_path

                    self.desired_path.pop()


            if len(self.desired_path) > 0:

                player_pos.y = int(self.desired_path[len(self.desired_path) - 1].tile[1] * self.data.tile_size)
                player_pos.x = int(self.desired_path[len(self.desired_path) - 1].tile[0] * self.data.tile_size)

                if abs(int(self.desired_path[len(self.desired_path) - 1].tile[0] * 64) - int(self.sprite.x)) < 2:
                    self.velocity.x = 0
                elif player_pos.x > self.sprite.x:
                    self.velocity.x = 1
                elif player_pos.x < self.sprite.x:
                    self.velocity.x = -1

                if abs(int(self.desired_path[len(self.desired_path) - 1].tile[1] * 64) - int(self.sprite.y)) < 2:

                    self.velocity.y = 0
                elif player_pos.y > self.sprite.y:

                    self.velocity.y = 1
                elif player_pos.y < self.sprite.y:

                    self.velocity.y = -1

                delta_x = self.enemy_speed * self.velocity.x * game_time.fixed_timestep
                delta_y = self.enemy_speed * self.velocity.y * game_time.fixed_timestep

                self.sprite.x = self.sprite.x + delta_x
                self.sprite.y = self.sprite.y + delta_y

                curr_pos_new = (self.sprite.x, self.sprite.y)

                if curr_pos_new == curr_pos_prev:
                    self.desired_path.pop()
