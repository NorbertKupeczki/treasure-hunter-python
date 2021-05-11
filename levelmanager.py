import pyasge
from gamestate import GameState, GameStateID


class LevelManager(GameState):
    def __init__(self, data):
        super().__init__(data)
        self.id = GameStateID.LEVEL_MANAGER

        self.keys = {
            pyasge.KEYS.KEY_SPACE: False,
            pyasge.KEYS.KEY_W: False,
            pyasge.KEYS.KEY_S: False
        }

        self.level_selected = self.data.level_selected

        self.levels = [pyasge.Text(self.data.fonts['title_text'], "Select a level:"),
                       pyasge.Text(self.data.fonts['main_text'], "Level 1"),
                       pyasge.Text(self.data.fonts['main_text'], "Level 2"),
                       pyasge.Text(self.data.fonts['main_text'], "Level 3"),
                       pyasge.Text(self.data.fonts['main_text'], "Level 4"),
                       pyasge.Text(self.data.fonts['main_text'], "Level 5"),
                       pyasge.Text(self.data.fonts['main_text'], "Level 6"),
                       pyasge.Text(self.data.fonts['main_text'], "Level 7"),
                       pyasge.Text(self.data.fonts['hud_text'], "Navigate with the W and S keys, "
                                                                "press SPACE to select a level.")]
        self.set_texts_position(self.levels, self.data.screen_size, 0.3)
        self.levels[self.data.level_selected].colour = pyasge.COLOURS.GOLD

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
                self.levels[self.level_selected].colour = pyasge.COLOURS.BLACK
                self.level_selected -= 1
                if self.level_selected < 1:
                    self.level_selected = 7
                self.levels[self.level_selected].colour = pyasge.COLOURS.GOLD
        elif event.key is pyasge.KEYS.KEY_S:
            if event.action is pyasge.KEYS.KEY_PRESSED:
                self.levels[self.level_selected].colour = pyasge.COLOURS.BLACK
                self.level_selected += 1
                if self.level_selected > 7:
                    self.level_selected = 1
                self.levels[self.level_selected].colour = pyasge.COLOURS.GOLD

    def update(self, game_time: pyasge.GameTime) -> GameStateID:
        if self.keys[pyasge.KEYS.KEY_SPACE]:
            self.data.level_selected = self.level_selected
            return GameStateID.START_MENU
        else:
            return GameStateID.LEVEL_MANAGER

    def render(self, game_time: pyasge.GameTime) -> None:
        self.data.renderer.setProjectionMatrix(self.data.camera.default_view)
        for text in self.levels:
            self.data.renderer.render(text)
