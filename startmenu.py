import pyasge
from gamestate import GameState, GameStateID


class StartMenu(GameState):
    def __init__(self, data):
        super().__init__(data)
        self.id = GameStateID.START_MENU

        self.start_text = pyasge.Text(self.data.fonts['kenvector'], "Start menu!\n\n ENTER - Game\n ESC - Quit")
        self.start_text.position = [self.data.screen_size[0] * 0.5 - self.start_text.width * 0.5, self.data.screen_size[1] * 0.5 - self.start_text.height * 0.5]
        self.start_text.colour = pyasge.COLOURS.BLACK

        self.data.inputs.addCallback(pyasge.EventType.E_KEY, self.input)

        self.keys = {
            pyasge.KEYS.KEY_ENTER: False,
            pyasge.KEYS.KEY_ESCAPE: False
        }

    def input(self, event: pyasge.KeyEvent) -> None:
        if event.action is not pyasge.KEYS.KEY_REPEATED:
            self.keys[event.key] = event.action is pyasge.KEYS.KEY_PRESSED

    def update(self, game_time: pyasge.GameTime) -> GameStateID:
        if self.keys[pyasge.KEYS.KEY_ESCAPE]:
            return GameStateID.EXIT
        elif self.keys[pyasge.KEYS.KEY_ENTER]:
            return GameStateID.GAMEPLAY
        else:
            return GameStateID.START_MENU

    def render(self, game_time: pyasge.GameTime) -> None:
        self.data.renderer.setProjectionMatrix(self.data.camera.default_view)
        self.data.renderer.render(self.start_text)
