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
                                                               "press SPACE to select.")]
        self.menu_selected = MenuID.START
        self.set_texts_position(self.texts, self.data.screen_size, 0.4)
        self.texts[self.menu_selected.value].colour = pyasge.COLOURS.GOLD

        self.data.score = 0

        self.data.inputs.addCallback(pyasge.EventType.E_KEY, self.input)
        self.keys = {
            pyasge.KEYS.KEY_SPACE: False,
            pyasge.KEYS.KEY_W: False,
            pyasge.KEYS.KEY_S: False
        }

    def input(self, event: pyasge.KeyEvent) -> None:
        if event.action is not pyasge.KEYS.KEY_REPEATED:
            self.keys[event.key] = event.action is pyasge.KEYS.KEY_PRESSED

        if event.key is pyasge.KEYS.KEY_W:
            if event.action is pyasge.KEYS.KEY_PRESSED:
                self.texts[self.menu_selected.value].colour = pyasge.COLOURS.BLACK
                if self.menu_selected == MenuID.START:
                    self.menu_selected = MenuID.QUIT
                elif self.menu_selected == MenuID.LEVEL_SELECT:
                    self.menu_selected = MenuID.START
                else:
                    self.menu_selected = MenuID.LEVEL_SELECT
                self.texts[self.menu_selected.value].colour = pyasge.COLOURS.GOLD
        elif event.key is pyasge.KEYS.KEY_S:
            if event.action is pyasge.KEYS.KEY_PRESSED:
                self.texts[self.menu_selected.value].colour = pyasge.COLOURS.BLACK
                if self.menu_selected == MenuID.START:
                    self.menu_selected = MenuID.LEVEL_SELECT
                elif self.menu_selected == MenuID.LEVEL_SELECT:
                    self.menu_selected = MenuID.QUIT
                else:
                    self.menu_selected = MenuID.START
                self.texts[self.menu_selected.value].colour = pyasge.COLOURS.GOLD

    def update(self, game_time: pyasge.GameTime) -> GameStateID:
        if self.keys[pyasge.KEYS.KEY_SPACE] and self.menu_selected == MenuID.START:
            return GameStateID.GAMEPLAY
        elif self.keys[pyasge.KEYS.KEY_SPACE] and self.menu_selected == MenuID.LEVEL_SELECT:
            return GameStateID.LEVEL_MANAGER
        elif self.keys[pyasge.KEYS.KEY_SPACE] and self.menu_selected == MenuID.QUIT:
            return GameStateID.EXIT
        else:
            return GameStateID.START_MENU

    def render(self, game_time: pyasge.GameTime) -> None:
        self.data.renderer.setProjectionMatrix(self.data.camera.default_view)

        for text in self.texts:
            self.data.renderer.render(text)


class MenuID(Enum):
    UNKNOWN = -1
    START = 1
    LEVEL_SELECT = 2
    QUIT = 3
