import pyasge


class Door:
    def __init__(self, position: pyasge.Point2D):
        self.sprite = pyasge.Sprite()
        self.sprite.loadTexture("/data/images/door.png")
        self.door_states = {
            'closed': pyasge.Point2D(0, 0),
            'opening_1': pyasge.Point2D(0, 64),
            'opening_2': pyasge.Point2D(0, 128),
            'open': pyasge.Point2D(0, 192)
        }
        self.set_sprite(self.door_states['closed'])
        self.sprite.x = position.x - self.sprite.width * 0.25
        self.sprite.y = position.y - self.sprite.height * 0.25
        self.sprite.scale = 1.2
        self.sprite.z_order = 2
        self.door_open = False
        self.elapsed_time = 0.0

    def set_sprite(self, pos: pyasge.Point2D):
        self.sprite.src_rect[pyasge.Sprite.SourceRectIndex.START_Y] = int(pos.y) + 1
        self.sprite.src_rect[pyasge.Sprite.SourceRectIndex.LENGTH_Y] = int(self.sprite.getTexture().height) * 0.25 - 2
        self.sprite.height = int(self.sprite.getTexture().height * 0.25) - 2

    def get_centre(self) -> pyasge.Point2D:
        sprite_centre = pyasge.Point2D(self.sprite.x + self.sprite.width * 0.5, self.sprite.y + self.sprite.height * 0.5)
        return sprite_centre

    def update(self, game_time: pyasge.GameTime):
        if self.door_open and self.elapsed_time < 1.0:
            if self.elapsed_time < 0.25:
                self.set_sprite(self.door_states['closed'])
            elif self.elapsed_time < 0.5:
                self.set_sprite(self.door_states['opening_1'])
            elif self.elapsed_time < 0.75:
                self.set_sprite(self.door_states['opening_2'])
            else:
                self.set_sprite(self.door_states['open'])

            self.elapsed_time += game_time.fixed_timestep
