import pyasge
from gamestate import GameState, GameStateID
from player import Player
from enemy import Enemy
from door import Door
from hud import HUD

from map import Map
# from A_star_pathfinding import Pathfinding

from gem import Gem
from vase import Vase


class GamePlay(GameState):
    def __init__(self, data):
        super().__init__(data)
        self.id = GameStateID.GAMEPLAY

        self.update_list = []

        self.gems = []
        self.vases = []
        self.data.enemies = []
        self.data.breakables = []
        self.load_map(self.data.level_selected)

        # initialising HUD and the player
        self.hud = HUD(data)
        self.player = Player(data, self.data.map.starting_location)
        self.update_list.append(self.player)

        self.entrance_door = Door(self.data.map.starting_location)
        self.exit_door = Door(self.data.map.end_location)
        self.update_list.append(self.exit_door)

        # register the key handler for this class
        self.data.inputs.addCallback(pyasge.EventType.E_KEY, self.input)

        # register the mouse handler for this class # added
        self.data.inputs.addCallback(pyasge.EventType.E_MOUSE_CLICK, self.click_event)  # added

        # initialise gems array & score
        # self.gems = [Gem(pyasge.Point2D(140, 300)), Gem(pyasge.Point2D(720, 400)), Gem(pyasge.Point2D(500, 800))]
        self.score = 0

        # track key states
        self.keys = {
            pyasge.KEYS.KEY_A: False,
            pyasge.KEYS.KEY_D: False,
            pyasge.KEYS.KEY_W: False,
            pyasge.KEYS.KEY_S: False,
            pyasge.KEYS.KEY_EQUAL: False,
            pyasge.KEYS.KEY_MINUS: False,
            pyasge.KEYS.KEY_SPACE: False,
            pyasge.KEYS.KEY_G: False,
            pyasge.KEYS.KEY_C: False,
            pyasge.KEYS.KEY_1: False,
            pyasge.KEYS.KEY_2: False,
            pyasge.KEYS.KEY_ESCAPE: False,
        }

        self.game_pad = self.data.inputs.getGamePad(0)

    def load_map(self, level_num) -> None:    # create the wanted level
        self.data.map = Map(str(level_num))

        for gem in self.data.map.layers[2].tiles:
            self.gems.append(Gem(pyasge.Point2D((gem.coordinate[0] + 0.5) * self.data.tile_size,
                                                (gem.coordinate[1] + 0.5) * self.data.tile_size)))

        for enemy in self.data.map.layers[3].tiles:
            self.data.enemies.append(Enemy(self.data, pyasge.Point2D(enemy.coordinate[0] * self.data.tile_size,
                                                                     enemy.coordinate[1] * self.data.tile_size)))

        self.player = Player(self.data, self.data.map.starting_location)

        for x in self.data.map.layers[4].tiles:
            self.data.breakables.append((x.coordinate[0], x.coordinate[1]))
            self.vases.append(Vase(pyasge.Point2D(x.coordinate[0] * self.data.tile_size, x.coordinate[1] * self.data.tile_size)))

    def click_event(self, event: pyasge.ClickEvent) -> None:  # added
        if event.button is pyasge.MOUSE.MOUSE_BTN1:
            if event.action is pyasge.MOUSE.BUTTON_PRESSED:   # if the left click is detected
                # temp_string_x = str(event.x / self.data.tile_size)   # the click position in pyASGE is relative to the world map instead of the size of the screen, if we divide it by 8 we get the tile number
                # temp_string_x = int(temp_string_x.split(".")[0])   # it will most likely be a long float value, therefore by saving it as a string we are able to get the numbers before the "."
                # temp_string_y = str(event.y / self.data.tile_size)
                # temp_string_y = int(temp_string_y.split(".")[0])
                # touple_coord = (temp_string_x, temp_string_y)       # save it as a touple to be sent off
                #
                # if 0 <= temp_string_x < self.data.map.width:  # check if the coordinates were in the actually map and not outside of the map
                #     if 0 <= temp_string_y < self.data.map.height:
                #         if self.data.map.cost_map[temp_string_y][temp_string_x] < 10000:    # if the cost of the thing clicked on is higher than this amount that means
                #                                                                         # the player clicked on a wall or something so don't initiate the pathfinding
                #             self.desired_path = Pathfinding((0, 0), touple_coord, self.data.map.cost_map, self.data.map.width, self.data.map.height).decided_path   # call the class to give the coordinates and save everything in the array
                #
                for i in self.data.enemies:    # debugging purpose, prints out the values of the above array
                    print(int(i.sprite.x), int(i.sprite.y))

        # Testing different functions on pressing RMB - Norbert
        # elif event.button is pyasge.MOUSE.MOUSE_BTN2:
        #

    def input(self, event: pyasge.KeyEvent) -> None:
        if event.action is not pyasge.KEYS.KEY_REPEATED:
            self.keys[event.key] = event.action is pyasge.KEYS.KEY_PRESSED

        # Turn game pad ON/OFF if game pad is connected
        if self.keys[pyasge.KEYS.KEY_G]:
            if event.action is pyasge.KEYS.KEY_PRESSED:
                if self.game_pad.connected:
                    if self.player.toggle_game_pad():
                        print("Game pad controls enabled")
                    else:
                        print("Game pad controls disabled")
                else:
                    print("No game pad connected!")

        if self.keys[pyasge.KEYS.KEY_SPACE]:
            if event.action is pyasge.KEYS.KEY_PRESSED:
                self.player.shoot()

        if self.keys[pyasge.KEYS.KEY_C]:
            if event.action is pyasge.KEYS.KEY_PRESSED:
                self.hud.coords_on = not self.hud.coords_on

    def update(self, game_time: pyasge.GameTime) -> GameStateID:
        for item in self.update_list:
            item.update(game_time)



        self.player.move_player(game_time, self.keys, self.game_pad)

        if self.gems:
            for gem in self.gems:
                if gem.check_collision(self.player.sprite):
                    gem_loc = pyasge.Point2D((gem.sprite.x + gem.sprite.width * 0.5) / self.data.tile_size - 0.5,
                                             (gem.sprite.y + gem.sprite.height * 0.5) / self.data.tile_size - 0.5)
                    print(f"Gem picked up from ({int(gem_loc.x)},{int(gem_loc.y)})")
                    # for tile in self.data.map.layers[2].tiles:
                    #     if tile.coordinate[0] == int(gem_loc.x) and tile.coordinate[1] == int(gem_loc.y):
                    #         self.data.map.layers[2].tiles.remove(tile)
                    self.data.score += gem.value
                    self.hud.update_score(self.data.score)
                    self.gems.remove(gem)
        else:
            if not self.exit_door.door_open:
                self.exit_door.door_open = True

            if pyasge.Point2D.distance(self.player.get_sprite(), self.exit_door.get_centre()) <= self.data.tile_size:
                if self.data.level_selected == 7:
                    return GameStateID.WINNER_WINNER
                else:
                    return GameStateID.NEXT_LEVEL

        # Moving the enemy towards the player
        # self.enemy.move_enemy(game_time, pyasge.Point2D(self.player.sprite.x, self.player.sprite.y))  #to turn back on

        # damage and destroy the vases as bullets hit them

        for bullet in self.player.projectiles.projectiles:
            for vase in self.vases:
                if vase.check_collision(bullet.sprite):
                    vase.hp -= 1
                    print(vase.hp)
                    vase.update(game_time)


        if self.player.game_pad_enabled:
            if self.data.inputs.getGamePad(0).RIGHT_TRIGGER != -1.0:
                self.player.shoot()

        if self.keys[pyasge.KEYS.KEY_ESCAPE]:
            return GameStateID.EXIT
        elif self.keys[pyasge.KEYS.KEY_1]:
            return GameStateID.GAME_OVER
        elif self.keys[pyasge.KEYS.KEY_2]:
            return GameStateID.WINNER_WINNER
        else:
            return GameStateID.GAMEPLAY



    def render(self, game_time: pyasge.GameTime) -> None:
        corner = self.data.camera.look_at(self.player.get_sprite())
        self.data.renderer.setProjectionMatrix(self.data.camera.camera.view)
        self.hud.render_hud(corner)
        self.data.map.render(self.data.renderer)  # added
        self.data.renderer.render(self.entrance_door.sprite)
        self.data.renderer.render(self.exit_door.sprite)
        self.data.renderer.render(self.player.sprite)
        self.player.render_bullets()
        for enemy in self.data.enemies:
            self.data.renderer.render(enemy.sprite)
        for gem in self.gems:
            self.data.renderer.render(gem.sprite)
        for vase in self.vases:
            vase.redraw()
            self.data.renderer.render(vase.sprite)
            if vase.gem.spawnGem:
                self.data.renderer.render(vase.gem.sprite)
