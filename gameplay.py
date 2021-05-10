import pyasge
from gamestate import GameState, GameStateID
from player import Player
from hud import HUD

from map import Map
from A_star_pathfinding import Pathfinding

from gem import Gem



class GamePlay(GameState):
    def __init__(self, data):
        super().__init__(data)
        self.id = GameStateID.GAMEPLAY

        self.data.map = Map('2')  # added
        self.desired_path = []  # added

        # initialising HUD and the player
        self.hud = HUD(data)
        self.player = Player(data, pyasge.Point2D(128, 128))

        # register the key handler for this class
        self.data.inputs.addCallback(pyasge.EventType.E_KEY, self.input)

        # register the mouse handler for this class # added
        self.data.inputs.addCallback(pyasge.EventType.E_MOUSE_CLICK, self.click_event)  # added

        # initialise gems array & score
        self.gemsArray = [Gem(pyasge.Point2D(140, 300)), Gem(pyasge.Point2D(720, 400)), Gem(pyasge.Point2D(500, 800))]
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

    def click_event(self, event: pyasge.ClickEvent) -> None: # added
        if event.button is pyasge.MOUSE.MOUSE_BTN1:
            if event.action is pyasge.MOUSE.BUTTON_PRESSED:   # if the left click is detected
                temp_string_x = str(event.x / self.data.tile_size)   # the click position in pyASGE is relative to the world map instead of the size of the screen, if we divide it by 8 we get the tile number
                temp_string_x = int(temp_string_x.split(".")[0])   # it will most likely be a long float value, therefore by saving it as a string we are able to get the numbers before the "."
                temp_string_y = str(event.y / self.data.tile_size)
                temp_string_y = int(temp_string_y.split(".")[0])
                touple_coord = (temp_string_x, temp_string_y)       # save it as a touple to be sent off

                if 0 <= temp_string_x < self.data.map.width:  # check if the coordinates were in the actually map and not outside of the map
                    if 0 <= temp_string_y < self.data.map.height:
                        if self.data.map.cost_map[temp_string_y][temp_string_x] < 10000:    # if the cost of the thing clicked on is higher than this amount that means
                                                                                        # the player clicked on a wall or something so don't initiate the pathfinding
                            self.desired_path = Pathfinding((0, 0), touple_coord, self.data.map.cost_map, self.data.map.width, self.data.map.height).decided_path   # call the class to give the coordinates and save everything in the array

                            for i in range(len(self.desired_path)):    # debugging purpose, prints out the values of the above array
                                print(self.desired_path[i].tile)
        # Testing different functions on pressing RMB - Norbert
        # elif event.button is pyasge.MOUSE.MOUSE_BTN2:
        #

    def input(self, event: pyasge.KeyEvent) -> None:
        if event.action is not pyasge.KEYS.KEY_REPEATED:
            self.keys[event.key] = event.action is pyasge.KEYS.KEY_PRESSED

        if event.key is pyasge.KEYS.KEY_Q:
            if event.action is pyasge.KEYS.KEY_PRESSED:
                print("loading map 1")
                self.data.map = Map('1')

        if event.key is pyasge.KEYS.KEY_E:
            if event.action is pyasge.KEYS.KEY_PRESSED:
                print("loading map 2")
                self.data.map = Map('2')

        # Turn game pad ON/OFF if game pad is connected
        if self.keys[pyasge.KEYS.KEY_G]:
            if event.action is pyasge.KEYS.KEY_PRESSED:
                if self.data.inputs.getGamePad(0).connected:
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

        print("SCORE: " + str(self.score))

        for i in range (0, len(self.gemsArray)):
            self.gemsArray[i].collectGem(self.player.sprite)
            if (self.gemsArray[i].scoreFlag == True):
                self.score += self.gemsArray[i].value

        self.player.projectiles.update_projectiles(game_time)
        if self.keys[pyasge.KEYS.KEY_ESCAPE]:
            return GameStateID.EXIT
        elif self.keys[pyasge.KEYS.KEY_1]:
            return GameStateID.GAME_OVER
        elif self.keys[pyasge.KEYS.KEY_2]:
            return GameStateID.WINNER_WINNER
        else:
            self.player.move_player(game_time, self.keys, self.data.inputs.getGamePad(0))
        return GameStateID.GAMEPLAY

    def render(self, game_time: pyasge.GameTime) -> None:
        corner = self.data.camera.look_at(self.player.get_sprite())
        self.data.renderer.setProjectionMatrix(self.data.camera.camera.view)
        self.hud.render_hud(corner)

        self.data.map.render(self.data.renderer)  # added
        self.player.render_bullets(self.data.renderer)
        self.data.renderer.render(self.player.sprite)
        for i in range (0, len(self.gemsArray)):
            if (self.gemsArray[i].hasBeenCollected == False):
                self.data.renderer.render(self.gemsArray[i].sprite)
