import pyasge


class HealthBar:
    def __init__(self, data):
        self.data = data
        self.hearts = [Heart(0),
                       Heart(1),
                       Heart(2),
                       Heart(3),
                       Heart(4)]

    def render_health_bar(self, renderer: pyasge.Renderer, corner: pyasge.Point2D):
        for heart in self.hearts:
            heart.sprite.x = heart.position.x + corner.x
            heart.sprite.y = corner.y + self.data.screen_size[1] - heart.sprite.height * 2 - 5
            renderer.render(heart.sprite)

    def heal(self):
        for heart in self.hearts:
            heart.heart_on()

    def lose_health(self, player_hp: int):
        if 0 <= player_hp < 5:
            self.hearts[player_hp].heart_off()


class Heart:
    def __init__(self, index: int):
        self.index = index
        self.sprite = pyasge.Sprite()
        self.SPRITE_SIZE = pyasge.Point2D(13, 12)
        self.position = pyasge.Point2D()
        self.init_hearts()

    def set_sprite(self, x: int, y: int, sprite: pyasge.Sprite()):
        sprite.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = int(x)
        sprite.src_rect[pyasge.Sprite.SourceRectIndex.START_Y] = int(y)
        sprite.src_rect[pyasge.Sprite.SourceRectIndex.LENGTH_X] = self.SPRITE_SIZE.x
        sprite.src_rect[pyasge.Sprite.SourceRectIndex.LENGTH_Y] = self.SPRITE_SIZE.y
        sprite.width = self.SPRITE_SIZE.x
        sprite.height = self.SPRITE_SIZE.y

    def init_hearts(self):
        self.sprite.loadTexture("/data/images/heart.png")
        self.sprite.scale = 2
        self.sprite.setMagFilter(pyasge.MagFilter.NEAREST)
        self.set_sprite(0, 0, self.sprite)
        self.position.x = 5 + self.index * (self.SPRITE_SIZE.x * 2 + 1)

    def heart_on(self):
        self.set_sprite(0, 0, self.sprite)

    def heart_off(self):
        self.set_sprite(13, 0, self.sprite)
