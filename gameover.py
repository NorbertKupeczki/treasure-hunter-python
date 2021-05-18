import pyasge
from gamestate import GameState, GameStateID


class GameOver(GameState):
    def __init__(self, data):
        super().__init__(data)
        self.id = GameStateID.GAME_OVER

        self.texts = [pyasge.Text(self.data.fonts['Title_text'], "Try again!\n"),
                      pyasge.Text(self.data.fonts['main_text'], "Main Menu"),
                      pyasge.Text(self.data.fonts['main_text'], "Quit"),
                      pyasge.Text(self.data.fonts['hud_text'], "Navigate the menu with the W and S keys, "
                                                               "press SPACE to select."),
                      pyasge.Text(self.data.fonts['hud_text'], "With game pad, use the LEFT and RIGHT BUMPER "
                                                               "to navigate, and (A) to select")]

        self.set_texts_position(self.texts, self.data.screen_size, 0.4)
        self.texts[1].colour = self.colours['accent']

        self.quit_selected = False

        self.data.inputs.addCallback(pyasge.EventType.E_KEY, self.input)
        self.keys = {
            pyasge.KEYS.KEY_SPACE: False,
            pyasge.KEYS.KEY_W: False,
            pyasge.KEYS.KEY_S: False
        }
        self.background.loadTexture(self.backgrounds['game_over'])

    def input(self, event: pyasge.KeyEvent) -> None:
        if event.action is not pyasge.KEYS.KEY_REPEATED:
            self.keys[event.key] = event.action is pyasge.KEYS.KEY_PRESSED

        if event.key is pyasge.KEYS.KEY_W or event.key is pyasge.KEYS.KEY_S:
            if event.action is pyasge.KEYS.KEY_PRESSED:
                self.switch_options()

    def update(self, game_time: pyasge.GameTime) -> GameStateID:
        self.gp_cd_update(game_time)

        if (self.data.inputs.getGamePad(0).LEFT_BUMPER or self.data.inputs.getGamePad(0).RIGHT_BUMPER) \
                and not self.game_pad_cd:
            self.switch_options()
            self.game_pad_cd += self.GP_CD

        if self.keys[pyasge.KEYS.KEY_SPACE] or (self.data.inputs.getGamePad(0).A and not self.game_pad_cd):
            if self.quit_selected:
                return GameStateID.EXIT
            elif not self.quit_selected:
                return GameStateID.START_MENU
        else:
            return GameStateID.GAME_OVER

    def render(self, game_time: pyasge.GameTime) -> None:
        self.data.renderer.setProjectionMatrix(self.data.camera.default_view)
        self.data.renderer.render(self.background)
        for text in self.texts:
            self.data.renderer.render(text)

    def switch_options(self):
        self.quit_selected = not self.quit_selected
        if self.quit_selected:
            self.texts[1].colour = self.colours['main']
            self.texts[2].colour = self.colours['accent']
        else:
            self.texts[2].colour = self.colours['main']
            self.texts[1].colour = self.colours['accent']
