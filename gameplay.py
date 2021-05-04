import pyasge
from gamestate import GameState, GameStateID
from player import Player

from map import Map
from A_star_pathfinding import Pathfinding


class GamePlay(GameState):
    def __init__(self, data):
        super().__init__(data)
        self.id = GameStateID.GAMEPLAY

        self.map = Map('1') # added
        self.desired_path = [] # added

        # register the key handler for this class
        self.data.inputs.addCallback(pyasge.EventType.E_KEY, self.input)
        self.player = Player(self.data.screen_size)

        # register the mouse handler for this class # added
        self.data.inputs.addCallback(pyasge.EventType.E_MOUSE_CLICK, self.click_event)  # added

        # create ui text instance
        self.ui_text = pyasge.Text(self.data.fonts['kenvector'], "DEMO")
        self.ui_text.position = [self.data.screen_size[0] * 0.5 - self.ui_text.width * 0.5, self.data.screen_size[1] - 5]
        self.ui_text.colour = pyasge.COLOURS.RED
        self.ui_text.z_order = 2

        # track key states
        self.keys = {
            pyasge.KEYS.KEY_A: False,
            pyasge.KEYS.KEY_D: False,
            pyasge.KEYS.KEY_W: False,
            pyasge.KEYS.KEY_S: False,
            pyasge.KEYS.KEY_1: False,
            pyasge.KEYS.KEY_2: False,
            pyasge.KEYS.KEY_ESCAPE: False
        }

    def click_event(self, event: pyasge.ClickEvent) -> None: # added
        if event.button is pyasge.MOUSE.MOUSE_BTN1:
            if event.action is pyasge.MOUSE.BUTTON_PRESSED:   # if the left click is detected
                temp_string_x = str(event.x / 8)   # the click position in pyASGE is relative to the world map instead of the size of the screen, if we divide it by 8 we get the tile number
                temp_string_x = int(temp_string_x.split(".")[0])   # it will most likely be a long float value, therefore by saving it as a string we are able to get the numbers before the "."
                temp_string_y = str(event.y / 8)
                temp_string_y = int(temp_string_y.split(".")[0])
                touple_coord = (temp_string_x, temp_string_y)       #save it as a touple to be sent off

                if 0 <= temp_string_x < self.map.width:  # check if the coordinates were in the actually map and not outside of the map
                    if 0 <= temp_string_y < self.map.height:
                        if self.map.cost_map[temp_string_y][temp_string_x] < 10000:    # if the cost of the thing clicked on is higher than this amount that means
                                                                                        # the player clicked on a wall or something so don't initiate the pathfinding
                            self.desired_path = Pathfinding((0, 0), touple_coord, self.map.cost_map, self.map.width, self.map.height).decided_path   # call the class to give the coordinates and save everything in the array

                            for i in range(len(self.desired_path)):    # debugging purpose, prints out the values of the above array
                                print(self.desired_path[i].tile)

    def input(self, event: pyasge.KeyEvent) -> None:
        if event.action is not pyasge.KEYS.KEY_REPEATED:
            self.keys[event.key] = event.action is pyasge.KEYS.KEY_PRESSED

    def update(self, game_time: pyasge.GameTime) -> GameStateID:
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

        self.map.render(self.data.renderer)  # added
        self.data.renderer.render(self.player.sprite)
        self.data.renderer.render(self.ui_text)
