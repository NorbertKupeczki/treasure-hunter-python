import pyasge
from fsm import FSM
from damagestates import DamageStates
from A_star_pathfinding import Pathfinding

from player import Player
from projetiles import Projectiles


class Enemy:
    def __init__(self, data, start_pos: pyasge.Point2D) -> None:

        # Filenames for each damage state zombie enemy can have
        self.states = ["/data/images/character_zombie_healthy.png",
                       "/data/images/character_zombie_damaged.png",
                       "/data/images/character_zombie_verydamaged.png",
                       "/data/images/character_zombie_neardead.png",
                       "/data/images/character_zombie_dead.png"]

        self.sprite = pyasge.Sprite()
        self.sprite.loadTexture(self.states[0])

        self.data = data

        # self.player_location = Player.get_sprite()
        self.sprite.x = start_pos.x
        self.sprite.y = start_pos.y
        self.desired_path = []
        self.current_index = -1
        self.goto_x = len(self.desired_path) + (self.current_index * 2)
        self.goto_y = len(self.desired_path) + self.current_index

        self.enemy_speed = 150
        self.velocity = pyasge.Point2D()
        self.facing = pyasge.Point2D(0, 1)

        self.hp = 10
        self.fsm = FSM()
        self.fsm.setstate(self.update_healthy)
        self.current_condition = DamageStates.HEALTHY
        self.previous_condition = DamageStates.HEALTHY
        # self.projectiles = Projectiles()

    def update(self):
        self.fsm.update()

        if self.current_condition != self.previous_condition:
            self.redraw()
            self.previous_condition = self.current_condition

    def move_enemy(self, game_time: pyasge.GameTime, player_location: pyasge.Point2D):
        print(str(abs(int(player_location.x) - int(self.sprite.x))))
        if abs(int(player_location.x) - int(self.sprite.x)) < 400 and abs(int(player_location.y) - int(self.sprite.y)) < 400:
            self.primitivePathfinding(game_time, player_location)
        ## Checks if enemy sprite touches player sprite
        if abs(int(player_location.x) - int(self.sprite.x)) < 2 or abs(int(player_location.y) - int(self.sprite.y)) < 2:
            pass

    def primitivePathfinding(self, game_time: pyasge.GameTime, player_location: pyasge.Point2D):
        if abs(int(player_location.x) - int(self.sprite.x)) < 2:
            self.velocity.x = 0
        elif player_location.x > self.sprite.x:
            self.velocity.x = 1
        elif player_location.x < self.sprite.x:
            self.velocity.x = -1

        if abs(int(player_location.y) - int(self.sprite.y)) < 2:
            self.velocity.y = 0
        elif player_location.y > self.sprite.y:
            self.velocity.y = 1
        elif player_location.y < self.sprite.y:
            self.velocity.y = -1

        delta_x = self.enemy_speed * self.velocity.x * game_time.fixed_timestep
        delta_y = self.enemy_speed * self.velocity.y * game_time.fixed_timestep
        # delta_xy = self.check_collision(delta_x, delta_y) <-- Temporary disabled

        self.sprite.x = self.sprite.x + delta_x
        self.sprite.y = self.sprite.y + delta_y

    def aStarPathfinding(self, game_time: pyasge.GameTime, player_location: pyasge.Point2D):
        temp_string_x = str(self.sprite.x / self.data.tile_size)
        temp_string_x = int(temp_string_x.split(".")[0])
        temp_string_y = str(self.sprite.y / self.data.tile_size)
        temp_string_y = int(temp_string_y.split(".")[0])
        touple_coord = (temp_string_x, temp_string_y)
        self.desired_path = Pathfinding(touple_coord, (
        int(player_location.x / self.data.tile_size), int(player_location.y / self.data.tile_size)),
                                        self.data.map.cost_map, self.data.map.width, self.data.map.height).decided_path

        self.goto_x = len(self.desired_path) + (self.current_index * 2)
        self.goto_y = len(self.desired_path) + self.current_index
        self.goto_x = self.goto_x * self.data.tile_size
        self.goto_y = self.goto_y * self.data.tile_size
        self.desired_path = 0
        # Debugging purposes
        print(str(self.goto_x) + "= goto x")
        print(str(self.goto_y) + "= goto y")
        print(str(player_location.x) + "= player x")
        print(str(player_location.y) + "= player y")
        print(str(self.sprite.x) + "= sprite x")
        print(str(self.sprite.y) + "= sprite y")

        if abs(int(self.goto_x) - int(self.sprite.x)) < 2:
            self.velocity.x = 0
        elif abs(int(self.goto_y) - int(self.sprite.y)) < 2:
            self.velocity.y = 0
        else:
            if self.goto_x > self.sprite.x:
                self.velocity.x = 1
            elif self.goto_x < self.sprite.x:
                self.velocity.x = -1
            if self.goto_y > self.sprite.y:
                self.velocity.y = 1
            elif self.goto_y < self.sprite.y:
                self.velocity.y = -1
            delta_x = self.enemy_speed * self.velocity.x * game_time.fixed_timestep
            delta_y = self.enemy_speed * self.velocity.y * game_time.fixed_timestep

            self.sprite.x = self.sprite.x + delta_x
            self.sprite.y = self.sprite.y + delta_y

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
