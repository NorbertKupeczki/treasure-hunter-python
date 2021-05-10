import pyasge
from gamestate import GameState, GameStateID


class StartMenu(GameState):
    def __init__(self, data):
        super().__init__(data)
        self.id = GameStateID.START_MENU
        self.texts = [pyasge.Text(self.data.fonts['title_text'], "Start menu"),
                      pyasge.Text(self.data.fonts['main_text'], "Start game"),
                      pyasge.Text(self.data.fonts['main_text'], "Quit"),
                      pyasge.Text(self.data.fonts['hud_text'], "Navigate the menu with the Q and S keys, "
                                                               "press SPACE to select.")]

        self.set_texts_position()

        self.data.inputs.addCallback(pyasge.EventType.E_KEY, self.input)

        self.start_selected = True

        self.keys = {
            pyasge.KEYS.KEY_SPACE: False,
            pyasge.KEYS.KEY_W: False,
            pyasge.KEYS.KEY_S: False
        }

    def input(self, event: pyasge.KeyEvent) -> None:
        if event.action is not pyasge.KEYS.KEY_REPEATED:
            self.keys[event.key] = event.action is pyasge.KEYS.KEY_PRESSED

        if event.key is pyasge.KEYS.KEY_W or event.key is pyasge.KEYS.KEY_S:
            if event.action is pyasge.KEYS.KEY_PRESSED:
                self.start_selected = not self.start_selected

    def update(self, game_time: pyasge.GameTime) -> GameStateID:
        if self.keys[pyasge.KEYS.KEY_SPACE] and self.start_selected:
            return GameStateID.GAMEPLAY
        elif self.keys[pyasge.KEYS.KEY_SPACE] and not self.start_selected:
            return GameStateID.EXIT
        else:
            return GameStateID.START_MENU

    def render(self, game_time: pyasge.GameTime) -> None:
        self.data.renderer.setProjectionMatrix(self.data.camera.default_view)
        if self.start_selected:
            self.texts[1].colour = pyasge.COLOURS.GOLD
            self.texts[2].colour = pyasge.COLOURS.BLACK
        else:
            self.texts[1].colour = pyasge.COLOURS.BLACK
            self.texts[2].colour = pyasge.COLOURS.GOLD

        for text in self.texts:
            self.data.renderer.render(text)

    def set_texts_position(self):
        index = 0
        for text in self.texts:
            text.position = [self.data.screen_size[0] * 0.5 - text.width * 0.5,
                             self.data.screen_size[1] * 0.5 - text.height * 0.5 + 60 * index]
            text.colour = pyasge.COLOURS.BLACK
            index += 1
