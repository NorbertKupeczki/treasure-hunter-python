import pyasge
from A_star_pathfinding import Pathfinding
from enemyMain import EnemyMain

from projetiles import Projectiles

class EnemyR(EnemyMain):
    def __init__(self, data, start_pos: pyasge.Point2D, Range, health, speed) -> None:
        super().__init__(data, start_pos, Range, health, speed)

        self.projectiles = Projectiles(self.data)

        self.reload = True
        self.timer = 1.0


    def move_enemy(self, game_time: pyasge.GameTime, player_location: pyasge.Point2D,player_location_tile: pyasge.Point2D):


        if self.reload is False:
            self.timer -= game_time.fixed_timestep
            if self.timer < 0:
                self.reload = True


        self.enemy_curr_tile_cord = (int(((self.sprite.x + self.sprite.width * 0.5) / self.data.tile_size)),
                                int((self.sprite.y + self.sprite.height * 0.5) / self.data.tile_size))

        distance = EnemyMain.distanceToPlayer(self, player_location_tile.x, player_location_tile.y, self.enemy_curr_tile_cord) # this si inhertied

        if distance < self.range:
            curr_pos_prev = (self.sprite.x, self.sprite.y)
            player_pos = player_location

            if int(self.old_player_pos.x) != int(player_location_tile.x) or int(self.old_player_pos.y) != int(player_location_tile.y):

                self.desired_path.clear()
                self.old_player_pos = player_location_tile


                if int(self.enemy_curr_tile_cord[0]) == int(player_location_tile.x) and int(self.enemy_curr_tile_cord[1]) == int(player_location_tile.y):

                    # self.re_path()
                    self.desired_path.clear()

                    if self.data.map.cost_map[int(self.enemy_curr_tile_cord[1]) + 1][int(self.enemy_curr_tile_cord[0])] < 1000:  # go to the bottom
                        self.desired_path = Pathfinding(self.enemy_curr_tile_cord, (int(self.enemy_curr_tile_cord[0]), int(self.enemy_curr_tile_cord[1]) + 1), self.data.map.cost_map, self.data.map.width, self.data.map.height).decided_path
                        self.facing = pyasge.Point2D(0, -1)

                    elif self.data.map.cost_map[int(self.enemy_curr_tile_cord[1]) - 1][int(self.enemy_curr_tile_cord[0])] < 1000:  # go to the top
                        self.desired_path = Pathfinding(self.enemy_curr_tile_cord, (int(self.enemy_curr_tile_cord[0]), int(self.enemy_curr_tile_cord[1]) - 1), self.data.map.cost_map, self.data.map.width, self.data.map.height).decided_path
                        self.facing = pyasge.Point2D(0, 1)

                    elif self.data.map.cost_map[int(self.enemy_curr_tile_cord[1])][int(self.enemy_curr_tile_cord[0]) - 1] < 1000:  # go to the left
                        self.desired_path = Pathfinding(self.enemy_curr_tile_cord, (int(self.enemy_curr_tile_cord[0]) - 1, int(self.enemy_curr_tile_cord[1])), self.data.map.cost_map, self.data.map.width, self.data.map.height).decided_path
                        self.facing = pyasge.Point2D(1, 0)

                    elif self.data.map.cost_map[int(self.enemy_curr_tile_cord[1])][int(self.enemy_curr_tile_cord[0]) + 1] < 1000:  # go to the right
                        self.desired_path = Pathfinding(self.enemy_curr_tile_cord, (int(self.enemy_curr_tile_cord[0]) + 1, int(self.enemy_curr_tile_cord[1])), self.data.map.cost_map, self.data.map.width, self.data.map.height).decided_path
                        self.facing = pyasge.Point2D(-1, 0)

                else:
                    player_pos = player_location

                    relation = self.side_check(self.sprite.x, self.sprite.y, player_pos.x, player_pos.y, 46, 62)

                    if relation != 0:

                        goal_tile = self.tile_check(player_location_tile.x, player_location_tile.y, relation)

                        self.desired_path.clear()

                        self.desired_path = Pathfinding(self.enemy_curr_tile_cord, (int(goal_tile[0]), int(goal_tile[1])), self.data.map.cost_map, self.data.map.width, self.data.map.height).decided_path
                        if len(self.desired_path) > 30:
                            self.desired_path.clear()

                        self.desired_path.pop()


            if len(self.desired_path) > 0:
                self.saved_tile = (self.desired_path[len(self.desired_path)-1].tile[0], self.desired_path[len(self.desired_path)-1].tile[1])

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
            else:
                if self.reload is True:
                    self.shoot()
                    self.timer = 1
                    self.reload = False
                    self.desired_path.clear()

    def side_check(self, main_x_pos, main_y_pos, square_x, square_y, square_width, rh):

        side_touched = 0

        if main_x_pos < square_x:  # left
            side_touched = 4
        elif main_x_pos > square_x + square_width:  # right
            side_touched = 2
        if main_y_pos < square_y:  # top
            side_touched = 1
        elif main_y_pos > square_y + rh:  # bottom
            side_touched = 3

        return side_touched

    def shoot(self):
        spawn_point = pyasge.Point2D(self.sprite.x + self.sprite.width * 0.5,
                                     self.sprite.y + self.sprite.height * 0.5)
        self.data.enemy_projectiles.zombie_shoot(spawn_point, self.facing)

    def tile_check(self, player_x, player_y, relation):

        player_curr_tile_y = player_y
        player_curr_tile_x = player_x

        player_saved_tile = (player_x, player_y)

        found = False
        for z in range(5):
            if z == 0:
                pass
            else:
                if not found:

                    if relation == 4:
                        player_curr_tile_x = player_x - z
                        self.facing = pyasge.Point2D(1, 0)

                    elif relation == 2:
                        player_curr_tile_x = player_x + z
                        self.facing = pyasge.Point2D(-1, 0)

                    elif relation == 1:
                        player_curr_tile_y = player_y - z
                        self.facing = pyasge.Point2D(0, 1)

                    elif relation == 3:
                        player_curr_tile_y = player_y + z
                        self.facing = pyasge.Point2D(0, -1)

                    if self.data.map.cost_map[int(player_curr_tile_y)][int(player_curr_tile_x)] > 10000:
                        found = True
                        break
                    else:
                        player_saved_tile = (player_curr_tile_x, player_curr_tile_y)

        return player_saved_tile

    def render_bullets(self, renderer):
        for bullets in self.projectiles.projectiles:
            renderer.render(bullets.sprite)


