import pyasge
from gamestate import GameState, GameStateID


class WinnerWinner(GameState):
    def __init__(self, data):
        super().__init__(data)
        self.id = GameStateID.WINNER_WINNER

        self.texts = [pyasge.Text(self.data.fonts['title_text'], "Winner winner,\nchicken dinner!\n"),
                      pyasge.Text(self.data.fonts['main_text'], "Main Menu"),
                      pyasge.Text(self.data.fonts['main_text'], "Quit"),
                      pyasge.Text(self.data.fonts['hud_text'], "Navigate the menu with the Q and S keys, "
                                                               "press SPACE to select.")]

        self.set_texts_position(self.texts, self.data.screen_size, 0.4)
        self.texts[1].colour = pyasge.COLOURS.GOLD

        self.quit_selected = False

        self.data.inputs.addCallback(pyasge.EventType.E_KEY, self.input)
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
                self.quit_selected = not self.quit_selected
                if self.quit_selected:
                    self.texts[1].colour = pyasge.COLOURS.BLACK
                    self.texts[2].colour = pyasge.COLOURS.GOLD
                else:
                    self.texts[2].colour = pyasge.COLOURS.BLACK
                    self.texts[1].colour = pyasge.COLOURS.GOLD

    def update(self, game_time: pyasge.GameTime) -> GameStateID:
        if self.keys[pyasge.KEYS.KEY_SPACE] and self.quit_selected:
            return GameStateID.EXIT
        elif self.keys[pyasge.KEYS.KEY_SPACE] and not self.quit_selected:
            return GameStateID.START_MENU
        else:
            return GameStateID.WINNER_WINNER

    def render(self, game_time: pyasge.GameTime) -> None:
        self.data.renderer.setProjectionMatrix(self.data.camera.default_view)
        for text in self.texts:
            self.data.renderer.render(text)
