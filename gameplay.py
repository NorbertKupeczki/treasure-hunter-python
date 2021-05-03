import pyasge
from gamestate import GameState, GameStateID
from player import Player

from map import Map
from A_star_pathfinding import Pathfinding

class GamePlay(GameState):
    def __init__(self, data):
        super().__init__(data)

        self.map = Map('1') # added
        self.desired_path = [] # added

        # register the key handler for this class
        self.data.inputs.addCallback(pyasge.EventType.E_KEY, self.input)
        self.player = Player(self.data.screen_size)
        self.player.set_sprite(402, 50)

        # register the mouse handler for this class # added
        self.data.inputs.addCallback(pyasge.EventType.E_MOUSE_CLICK, self.click_event)  # added

        # create ui text instance
        self.ui_text = pyasge.Text(self.data.fonts['kenvector'], "BRAINZZZZ!!!")
        self.ui_text.position = [512 - self.ui_text.width * 0.5, 35]
        self.ui_text.colour = pyasge.COLOURS.AQUA


        # create a list of bullets
        self.bullets_list = []
        self.bullets_index = 0
        self.bullets_max = 5

        # track key states
        self.keys = {
            pyasge.KEYS.KEY_A: False,
            pyasge.KEYS.KEY_D: False,
            pyasge.KEYS.KEY_W: False,
            pyasge.KEYS.KEY_S: False,
            pyasge.KEYS.KEY_EQUAL: False,
            pyasge.KEYS.KEY_MINUS: False,
            pyasge.KEYS.KEY_SPACE: False,
        }


    def click_event(self, event: pyasge.ClickEvent) -> None: # added
        if event.button is pyasge.MOUSE.MOUSE_BTN1:
            if event.action is pyasge.MOUSE.BUTTON_PRESSED:
                temp_string_x = str(event.x / 8)
                temp_string_x = int(temp_string_x[0])
                temp_string_y = str(event.y / 8)
                temp_string_y = int(temp_string_y[0])
                touple_coord = (temp_string_x, temp_string_y)

                if 0 <= temp_string_x < self.map.width:
                    if 0 <= temp_string_y < self.map.height:
                        if self.map.cost_map[temp_string_y][temp_string_x] < 10000:
                            self.desired_path = Pathfinding((0, 0), touple_coord, self.map.cost_map, self.map.width, self.map.height).decided_path

                            for i in range(len(self.desired_path)):
                                print(self.desired_path[i].tile)


    def input(self, event: pyasge.KeyEvent) -> None:
        if event.action is not pyasge.KEYS.KEY_REPEATED:
            self.keys[event.key] = event.action is pyasge.KEYS.KEY_PRESSED

    def update(self, game_time: pyasge.GameTime) -> GameStateID:
        self.player.move_player(game_time, self.keys, self.data.inputs.getGamePad(0))
        return GameStateID.GAMEPLAY

    def render(self, game_time: pyasge.GameTime) -> None:

        self.map.render(self.data.renderer) # added

        self.data.renderer.render(self.player.sprite)
        self.data.renderer.render(self.ui_text)
