import pyasge
from gamestate import GameState, GameStateID
from enum import Enum


class StartMenu(GameState):
    def __init__(self, data):
        super().__init__(data)
        self.id = GameStateID.START_MENU
        self.texts = [pyasge.Text(self.data.fonts['title_text'], "Start menu"),
                      pyasge.Text(self.data.fonts['main_text'], "Start game"),
                      pyasge.Text(self.data.fonts['main_text'], "Level " + str(self.data.level_selected)),
                      pyasge.Text(self.data.fonts['main_text'], "Quit"),
                      pyasge.Text(self.data.fonts['hud_text'], "Navigate the menu with the W and S keys, "
                                                               "press SPACE to select."),
                      pyasge.Text(self.data.fonts['hud_text'], "With game pad, use the LEFT and RIGHT BUMPER "
                                                               "to navigate, and (A) to select")
                      ]
        self.menu_selected = MenuID.START
        self.set_texts_position(self.texts, self.data.screen_size, 0.4)
        self.texts[self.menu_selected.value].colour = self.colours['accent']

        self.data.score = 0

        self.data.inputs.addCallback(pyasge.EventType.E_KEY, self.input)
        self.keys = {
            pyasge.KEYS.KEY_SPACE: False,
            pyasge.KEYS.KEY_W: False,
            pyasge.KEYS.KEY_S: False
        }

        self.background.loadTexture(self.backgrounds['main'])

    def input(self, event: pyasge.KeyEvent) -> None:
        if event.action is not pyasge.KEYS.KEY_REPEATED:
            self.keys[event.key] = event.action is pyasge.KEYS.KEY_PRESSED

        if event.key is pyasge.KEYS.KEY_W:
            if event.action is pyasge.KEYS.KEY_PRESSED:
                self.menu_up()
        elif event.key is pyasge.KEYS.KEY_S:
            if event.action is pyasge.KEYS.KEY_PRESSED:
                self.menu_down()

    def update(self, game_time: pyasge.GameTime) -> GameStateID:
        self.gp_cd_update(game_time)

        if self.data.inputs.getGamePad(0).LEFT_BUMPER and not self.game_pad_cd:
            self.menu_up()
            self.game_pad_cd += self.GP_CD
        elif self.data.inputs.getGamePad(0).RIGHT_BUMPER and not self.game_pad_cd:
            self.menu_down()
            self.game_pad_cd += self.GP_CD

        if self.keys[pyasge.KEYS.KEY_SPACE] or (self.data.inputs.getGamePad(0).A and not self.game_pad_cd):
            if self.menu_selected == MenuID.START:
                return GameStateID.GAMEPLAY
            elif self.menu_selected == MenuID.LEVEL_SELECT:
                return GameStateID.LEVEL_MANAGER
            elif self.menu_selected == MenuID.QUIT:
                return GameStateID.EXIT
        else:
            return GameStateID.START_MENU

    def render(self, game_time: pyasge.GameTime) -> None:
        self.data.renderer.setProjectionMatrix(self.data.camera.default_view)
        self.data.renderer.render(self.background)
        for text in self.texts:
            self.data.renderer.render(text)

    def menu_up(self):
        self.texts[self.menu_selected.value].colour = self.colours['main']
        if self.menu_selected == MenuID.START:
            self.menu_selected = MenuID.QUIT
        elif self.menu_selected == MenuID.LEVEL_SELECT:
            self.menu_selected = MenuID.START
        else:
            self.menu_selected = MenuID.LEVEL_SELECT
        self.texts[self.menu_selected.value].colour = self.colours['accent']

    def menu_down(self):
        self.texts[self.menu_selected.value].colour = self.colours['main']
        if self.menu_selected == MenuID.START:
            self.menu_selected = MenuID.LEVEL_SELECT
        elif self.menu_selected == MenuID.LEVEL_SELECT:
            self.menu_selected = MenuID.QUIT
        else:
            self.menu_selected = MenuID.START
        self.texts[self.menu_selected.value].colour = self.colours['accent']


class MenuID(Enum):
    UNKNOWN = -1
    START = 1
    LEVEL_SELECT = 2
    QUIT = 3
