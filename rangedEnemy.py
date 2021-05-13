import pyasge
from fsm import FSM
from damagestates import DamageStates
from A_star_pathfinding import Pathfinding
import math

from projetiles import Projectiles


class EnemyR:
    def __init__(self, data, start_pos: pyasge.Point2D) -> None:

        self.states = ["/data/images/character_zombie_dead.png",
                       "/data/images/character_zombie_damaged.png",
                       "/data/images/character_zombie_verydamaged.png",
                       "/data/images/character_zombie_neardead.png",
                       "/data/images/character_zombie_healthy.png"]

        self.sprite = pyasge.Sprite()
        self.sprite.loadTexture(self.states[0])
        self.sprite.scale = 0.35

        self.data = data  # data of the game

        self.sprite.x = start_pos.x  # starting pos
        self.sprite.y = start_pos.y

        self.desired_path = []  # pathfinding stuff

        self.enemy_speed = 60  # movement things
        self.velocity = pyasge.Point2D()
        self.facing = pyasge.Point2D(0, 1)

        self.hp = 10  # state machine stuff
        self.fsm = FSM()
        self.fsm.setstate(self.update_healthy)
        self.current_condition = DamageStates.HEALTHY
        self.previous_condition = DamageStates.HEALTHY
        self.projectiles = Projectiles(self.data)

        self.reload = True
        self.timer = 1.0

        self.old_player_pos = pyasge.Point2D(0, 0)

    def update(self):
        self.fsm.update()

        if self.current_condition != self.previous_condition:
            self.redraw()
            self.previous_condition = self.current_condition

    def move_enemy(self, game_time: pyasge.GameTime, player_location: pyasge.Point2D,
                   player_location_tile: pyasge.Point2D):

        if self.reload is False:
            self.timer -= game_time.fixed_timestep
            if self.timer < 0:
                self.reload = True

        temp_string_x = str((self.sprite.x + 35) / self.data.tile_size)
        temp_string_x = int(temp_string_x.split(".")[0])
        temp_string_y = str((self.sprite.y + 60) / self.data.tile_size)
        temp_string_y = int(temp_string_y.split(".")[0])
        enemy_curr_tile_cord = (temp_string_x, temp_string_y)

        distance = self.heuristic(player_location_tile.x, player_location_tile.y, enemy_curr_tile_cord)


        if distance < 5.5:
            curr_pos_prev = (self.sprite.x, self.sprite.y)

            player_pos = player_location

            if int(self.old_player_pos.x) != int(player_location_tile.x) or int(self.old_player_pos.y) != int(player_location_tile.y):

                self.desired_path.clear()
                self.old_player_pos = player_location_tile


                if int(enemy_curr_tile_cord[0]) == int(player_location_tile.x) and int(enemy_curr_tile_cord[1]) == int(player_location_tile.y):

                    self.desired_path.clear()



                    if self.data.map.cost_map[int(enemy_curr_tile_cord[1]) + 1][int(enemy_curr_tile_cord[0])] < 1000:  # go to the bottom
                        self.desired_path = Pathfinding(enemy_curr_tile_cord, (int(enemy_curr_tile_cord[0]), int(enemy_curr_tile_cord[1]) + 1), self.data.map.cost_map, self.data.map.width, self.data.map.height).decided_path

                        self.facing = pyasge.Point2D(0, -1)

                    elif self.data.map.cost_map[int(enemy_curr_tile_cord[1]) - 1][int(enemy_curr_tile_cord[0])] < 1000:  # go to the top
                        self.desired_path = Pathfinding(enemy_curr_tile_cord, (int(enemy_curr_tile_cord[0]), int(enemy_curr_tile_cord[1]) - 1), self.data.map.cost_map, self.data.map.width, self.data.map.height).decided_path
                        self.facing = pyasge.Point2D(0, 1)

                    elif self.data.map.cost_map[int(enemy_curr_tile_cord[1])][int(enemy_curr_tile_cord[0]) - 1] < 1000:  # go to the left
                        self.desired_path = Pathfinding(enemy_curr_tile_cord, (int(enemy_curr_tile_cord[0]) - 1, int(enemy_curr_tile_cord[1])), self.data.map.cost_map, self.data.map.width, self.data.map.height).decided_path
                        self.facing = pyasge.Point2D(1, 0)

                    elif self.data.map.cost_map[int(enemy_curr_tile_cord[1])][int(enemy_curr_tile_cord[0]) + 1] < 1000:  # go to the right
                        self.desired_path = Pathfinding(enemy_curr_tile_cord, (int(enemy_curr_tile_cord[0]) + 1, int(enemy_curr_tile_cord[1])), self.data.map.cost_map, self.data.map.width, self.data.map.height).decided_path
                        self.facing = pyasge.Point2D(-1, 0)

                else:
                    player_pos = player_location

                    relation = self.side_check(self.sprite.x, self.sprite.y, player_pos.x, player_pos.y, 46, 62)

                    if relation != 0:
                        goal_tile = self.tile_check(player_location_tile.x, player_location_tile.y, relation)
                        self.desired_path.clear()

                        self.desired_path = Pathfinding(enemy_curr_tile_cord,(int(goal_tile[0]), int(goal_tile[1])),self.data.map.cost_map, self.data.map.width, self.data.map.height).decided_path

                        self.desired_path.pop()


            else:
                pass

            if len(self.desired_path) > 0:

                player_pos.y = int(self.desired_path[len(self.desired_path) - 1].tile[1] * 64)
                player_pos.x = int(self.desired_path[len(self.desired_path) - 1].tile[0] * 64)

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
        # the zmobie is on the .... of the player meaning

        if main_x_pos < square_x:  # left
            side_touched = 4
        elif (main_x_pos > square_x + square_width):  # right
            side_touched = 2

        if (main_y_pos < square_y):  # top
            side_touched = 1
        elif (main_y_pos > square_y + rh):  # bottom
            side_touched = 3

        return side_touched

    def shoot(self):
        spawn_point = pyasge.Point2D(self.sprite.x + 35, self.sprite.y + 60)
        self.projectiles.shoot(spawn_point, self.facing)

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

    def redraw(self):
        if self.current_condition < DamageStates.DEAD:
            if self.current_condition == DamageStates.HEALTHY:
                self.sprite.loadTexture(self.states[0])
            elif self.current_condition == DamageStates.DAMAGED:
                self.sprite.loadTexture(self.states[1])
            elif self.current_condition == DamageStates.VERY_DAMAGED:
                self.sprite.loadTexture(self.states[2])
            elif self.current_condition == DamageStates.NEAR_DEAD:
                self.sprite.loadTexture(self.states[3])
        else:
            self.sprite.loadTexture(self.states[4])

    def update_healthy(self):
        self.current_condition = DamageStates.HEALTHY
        if self.hp <= 7:
            self.fsm.setstate(self.update_damaged)

    def update_damaged(self):
        self.current_condition = DamageStates.DAMAGED
        if self.hp <= 4:
            self.fsm.setstate(self.update_damaged)

    def update_verydamaged(self):
        self.current_condition = DamageStates.VERY_DAMAGED
        if self.hp <= 2:
            self.fsm.setstate(self.update_damaged)

    def update_neardead(self):
        self.current_condition = DamageStates.NEAR_DEAD
        if self.hp <= 0:
            self.fsm.setstate(self.update_damaged)

    def update_dead(self):
        self.current_condition = DamageStates.DEAD

    def render_bullets(self, renderer):
        for bullets in self.projectiles.projectiles:
            renderer.render(bullets.sprite)

    def heuristic(self, x, y, enemy_tile):  #distance from the player

        dx = abs(x - enemy_tile[0])
        dy = abs(y - enemy_tile[1])

        return math.sqrt(dx * dx + dy * dy)
