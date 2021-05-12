import pyasge
from fsm import FSM
from damagestates import DamageStates
from A_star_pathfinding import Pathfinding

from player import Player
from projetiles import Projectiles


class EnemyR:
    def __init__(self, data, start_pos: pyasge.Point2D) -> None:

        ## Filenames for each damage state zombie enemy can have
        self.states = ["/data/images/character_zombie_dead.png",
                       "/data/images/character_zombie_damaged.png",
                       "/data/images/character_zombie_verydamaged.png",
                       "/data/images/character_zombie_neardead.png",
                       "/data/images/character_zombie_healthy.png"]


        self.sprite = pyasge.Sprite()   # actuall sprite
        self.sprite.loadTexture(self.states[0])    # load the texture
        self.sprite.scale = 0.35     #change the size

        self.data = data    # data of the game

        # self.player_location = Player.get_sprite()
        self.sprite.x = start_pos.x  #starting pos
        self.sprite.y = start_pos.y

        self.desired_path = []    #pathfinding stuff
        self.goto = len(self.desired_path) - 1

        self.enemy_speed = 50    #movement things
        self.velocity = pyasge.Point2D()
        self.facing = pyasge.Point2D(0, 1)

        self.hp = 10   #state machine stuff
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




    #self.enemy.move_enemy(game_time, pyasge.Point2D(self.player.sprite.x, self.player.sprite.y))   #to turn back on

    def move_enemy(self, game_time: pyasge.GameTime, player_location: pyasge.Point2D, player_location_tile: pyasge.Point2D):


        #print(player_location)    # player location given in coord

        #mid_sprite_x = self.sprite.x + self.sprite.width/2
        #mid_sprite_y = self.sprite.y + self.sprite.height/2

        # player_location_x = player_location.x + 23
        # player_location_y = player_location.y + 31

        relation = self.side_check(self.sprite.x, self.sprite.y, player_location.x, player_location.y, 46, 62)
        print("-------------------")
        print("-------------------")
        #print(player_location_tile)

        if relation == 4:
            #then we want to minus the x by 5
            print("the zmobie is on the left of the player ")
            player_location_tile.x = player_location_tile.x - 5

        elif relation == 2:
            # then we want to add the x by 5
            print("the zmobie is on the right of the player ")
            player_location_tile.x = player_location_tile.x + 5

        elif relation == 1:
            # then we want to add the y by 5
            print("the zmobie is on the top of the player ")
            player_location_tile.y = player_location_tile.y - 5

        elif relation == 3:
            player_location_tile.y = player_location_tile.y + 5
            print("the zmobie is on the bottom of the player ")
            # then we want to minus the y by 5




        if relation != 0:

            # print(player_location_tile)

            # print(self.side_check(player_location.x, player_location.y, self.sprite.x, self.sprite.y, self.sprite.width, self.sprite.height))
            player_location.y = player_location_tile.y * 64
            player_location.x = player_location_tile.x * 64
            # print(player_location.y)

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

        # if self.current_condition != DamageStates.DEAD:
        #     self.desired_path = Pathfinding((int(self.sprite.x / self.data.tile_size), int(self.sprite.y / self.data.tile_size)),(int(player_location.x / self.data.tile_size), int(player_location.y / self.data.tile_size)), self.data.map.cost_map, self.data.map.width, self.data.map.height).decided_path
        #     self.goto = len(self.desired_path) - 1
        #     # self.sprite = self.goto[0]
        #
        #     # Checks if enemy sprite touches player sprite
        #     if abs(int(player_location.x) - int(self.sprite.x)) < 2 or abs(int(player_location.y) - int(self.sprite.y)) < 2:
        #         pass



    def side_check(self, main_x_pos, main_y_pos, square_x, square_y, square_width,  rh):

        side_touched = 0
        #the zmobie is on the .... of the player meaning

        if main_x_pos < square_x:   #left
            side_touched = 4
        elif (main_x_pos > square_x + square_width):   #right
            side_touched = 2

        if (main_y_pos < square_y) :   #top
            side_touched = 1
        elif (main_y_pos > square_y + rh):  #bottom
            side_touched = 3



        return side_touched



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