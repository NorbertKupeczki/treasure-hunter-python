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
        #self.goto = len(self.desired_path) - 1

        self.enemy_speed = 50    #movement things
        self.velocity = pyasge.Point2D()
        self.facing = pyasge.Point2D(0, 1)

        self.hp = 10   #state machine stuff
        self.fsm = FSM()
        self.fsm.setstate(self.update_healthy)
        self.current_condition = DamageStates.HEALTHY
        self.previous_condition = DamageStates.HEALTHY
        self.projectiles = Projectiles(self.data)

        self.reload = True
        self.timer = 1.0

        self.path_check = True
        self.timer_path = 3.0


        #evey tot amount of time check for the new path



    def update(self):
        self.fsm.update()

        if self.current_condition != self.previous_condition:
            self.redraw()
            self.previous_condition = self.current_condition


        # if self.reload is False:
        #     self.timer -= self.data.game_time.fixed_timestep
        #     if self.timer < 0:
        #         self.reload = True
        #         print("calleddadaa")



    def move_enemy(self, game_time: pyasge.GameTime, player_location: pyasge.Point2D, player_location_tile: pyasge.Point2D):

        if self.path_check is False:
            self.timer_path -= game_time.fixed_timestep
            if self.timer_path < 0:
                self.path_check = True
        else:
            temp_string_x = str(self.sprite.x / self.data.tile_size)   # the click position in pyASGE is relative to the world map instead of the size of the screen, if we divide it by 8 we get the tile number
            temp_string_x = int(temp_string_x.split(".")[0])   # it will most likely be a long float value, therefore by saving it as a string we are able to get the numbers before the "."
            temp_string_y = str(self.sprite.y / self.data.tile_size)
            temp_string_y = int(temp_string_y.split(".")[0])
            touple_coord = (temp_string_x, temp_string_y)       # save it as a touple to be sent off
            #print(touple_coord)

            self.desired_path = Pathfinding(touple_coord, (int(player_location_tile.x), int(player_location_tile.y)), self.data.map.cost_map, self.data.map.width, self.data.map.height).decided_path  # call the class to give the coordinates and save everything in the array







            for i in range(len(self.desired_path)):  # debugging purpose, prints out the values of the above array
                print(self.desired_path[i].tile)
            print("this")
            print("t--------------------------------------")
            self.path_check = False
            self.timer_path = 3.0






        if self.reload is False:
            self.timer -= game_time.fixed_timestep
            if self.timer < 0:
                self.reload = True

        #print(player_location)    # player location given in coord

        #mid_sprite_x = self.sprite.x + self.sprite.width/2
        #mid_sprite_y = self.sprite.y + self.sprite.height/2

        # player_location_x = player_location.x + 23
        # player_location_y = player_location.y + 31

        relation = self.side_check(self.sprite.x, self.sprite.y, player_location.x, player_location.y, 46, 62)
        # print("-------------------")
        # print("-------------------")
        #print(player_location_tile)

        if relation == 4:
            #then we want to minus the x by 5
            #print("the zmobie is on the left of the player ")
            self.facing = pyasge.Point2D(1, 0)
            player_location_tile.x = player_location_tile.x - 5

        elif relation == 2:
            # then we want to add the x by 5
            #print("the zmobie is on the right of the player ")
            self.facing = pyasge.Point2D(-1, 0)
            player_location_tile.x = player_location_tile.x + 5

        elif relation == 1:
            # then we want to add the y by 5
            #print("the zmobie is on the top of the player ")
            self.facing = pyasge.Point2D(0, 1)
            player_location_tile.y = player_location_tile.y - 5

        elif relation == 3:
            self.facing = pyasge.Point2D(0, -1)
            player_location_tile.y = player_location_tile.y + 5
            #print("the zmobie is on the bottom of the player ")
            # then we want to minus the y by 5




        if relation != 0:

            # print(player_location_tile)
            curr_pos_prev = (self.sprite.x, self.sprite.y)
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

            #delta_xy = self.check_collision(delta_x, delta_y) <-- Temporary disabled

            self.sprite.x = self.sprite.x + delta_x
            self.sprite.y = self.sprite.y + delta_y

            curr_pos_new = (self.sprite.x, self.sprite.y)


            if curr_pos_new == curr_pos_prev and self.reload:
                self.shoot()
                self.timer = 1
                self.reload = False





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

    def shoot(self):
        spawn_point = pyasge.Point2D(self.sprite.x + 35, self.sprite.y + 60)
        self.projectiles.shoot(spawn_point, self.facing)


    def tile_check(self, tile_x, tile_y):
        #this is where we can check if the tiles exist and possible pathfindg
        pass



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