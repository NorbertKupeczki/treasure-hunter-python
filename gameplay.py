import pyasge
from gamestate import GameState, GameStateID


class GamePlay(GameState):
    def __init__(self, data):
        super().__init__(data)

        # register the key handler for this class
        self.data.inputs.addCallback(pyasge.EventType.E_KEY, self.input)

        # create a zombie player sprite
        self.sprite = pyasge.Sprite()
        self.sprite.loadTexture("/data/images/character_zombie_idle.png")
        self.sprite.x = 512 - self.sprite.width * 0.5
        self.sprite.y = 384 - self.sprite.height * 0.5

        # create ui text instance
        self.ui_text = pyasge.Text(self.data.fonts['kenvector'], "BRAINZZZZ!!!")
        self.ui_text.position = [512 - self.ui_text.width * 0.5, 35]
        self.ui_text.colour = pyasge.COLOURS.AQUA

        # track key states
        self.keys = {
            pyasge.KEYS.KEY_A: False,
            pyasge.KEYS.KEY_D: False,
            pyasge.KEYS.KEY_W: False,
            pyasge.KEYS.KEY_S: False,
            pyasge.KEYS.KEY_EQUAL: False,
            pyasge.KEYS.KEY_MINUS: False,
        }

    def input(self, event: pyasge.KeyEvent) -> None:
        if event.action is not pyasge.KEYS.KEY_REPEATED:
            self.keys[event.key] = event.action is pyasge.KEYS.KEY_PRESSED

    def update(self, game_time: pyasge.GameTime) -> GameStateID:
        if self.keys[pyasge.KEYS.KEY_W]:
            self.sprite.y = self.sprite.y - 500 * game_time.fixed_timestep
        if self.keys[pyasge.KEYS.KEY_S]:
            self.sprite.y = self.sprite.y + 500 * game_time.fixed_timestep
        if self.keys[pyasge.KEYS.KEY_A]:
            self.sprite.x = self.sprite.x - 500 * game_time.fixed_timestep
        if self.keys[pyasge.KEYS.KEY_D]:
            self.sprite.x = self.sprite.x + 500 * game_time.fixed_timestep
        return GameStateID.GAMEPLAY

    def render(self, game_time: pyasge.GameTime) -> None:
        self.data.renderer.render(self.sprite)
        self.data.renderer.render(self.ui_text)
