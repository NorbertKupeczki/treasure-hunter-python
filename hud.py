import pyasge
from healthbar import HealthBar
from abc import ABC, abstractmethod


class HUD:
    def __init__(self, data):
        self.data = data

        self.health_bar = HealthBar(data)

        self.ui = [
            UIText(pyasge.Point2D(5, 20), pyasge.COLOURS.LIME, 'hud_text', "Score: " + str(self.data.score), self.data),
            UIText(pyasge.Point2D(120, 20), pyasge.COLOURS.LIME, 'hud_text', "World: ", self.data),
            UIText(pyasge.Point2D(300, 20), pyasge.COLOURS.LIME, 'hud_text', "Tile: ", self.data),
            UIText(pyasge.Point2D(self.data.screen_size[0] - 100, 20), pyasge.COLOURS.LIME, 'hud_text',
                   "Level: "+str(self.data.level_selected), self.data),
            UIImage(pyasge.Point2D(0, 0), "/data/images/bar.png", 0, data),
            UIImage(pyasge.Point2D(0, self.data.screen_size[1] - self.data.tile_size * 0.5),
                    "/data/images/bar.png", 180, data)
        ]
        self.ui[1].visible = False
        self.ui[2].visible = False

    def render_hud(self, corner: pyasge.Point2D):
        self.update_coordinates()

        for item in self.ui:
            item.update_pos(corner)
            if item.visible:
                item.render()
        self.health_bar.render_health_bar(self.data.renderer, corner)

    def update_score(self, score: int):
        self.ui[0].update_text("Score: "+str(score))

    def update_coordinates(self):
        self.ui[1].update_text("World: " + str(int(self.data.world_loc.x)) + ':' + str(int(self.data.world_loc.y)))
        self.ui[2].update_text("Tile: " + str(int(self.data.tile_loc.x)) + ':' + str(int(self.data.tile_loc.y)))

    def switch_coordinates(self):
        self.ui[1].visible = not self.ui[1].visible
        self.ui[2].visible = not self.ui[2].visible


class UIElement(ABC):
    def __init__(self):
        self.visible = True
        self.data = None
        self.position = pyasge.Point2D

    @abstractmethod
    def update_pos(self, corner: pyasge.Point2D):
        pass

    @abstractmethod
    def render(self):
        pass


class UIText(UIElement):
    def __init__(self, position: pyasge.Point2D, colour: pyasge.Colour, font: str, text: str, data):
        super().__init__()
        self.data = data
        self.text = pyasge.Text(self.data.fonts[font], text)
        self.text.colour = colour
        self.text.z_order = self.data.z_order['UI']
        self.position = position

    def update_pos(self, corner: pyasge.Point2D):
        self.text.position = [corner.x + self.position.x, corner.y + self.position.y]

    def update_text(self, text: str):
        self.text.string = text

    def render(self):
        self.data.renderer.render(self.text)


class UIImage(UIElement):
    def __init__(self, position: pyasge.Point2D, path: str, rotation: int, data):
        super().__init__()
        self.data = data
        self.sprite = pyasge.Sprite()
        self.sprite.loadTexture(path)
        self.sprite.rotation = rotation * 3.1415 / 180
        self.sprite.z_order = self.data.z_order['UI'] - 1
        self.position = position

    def update_pos(self, corner: pyasge.Point2D):
        self.sprite.x = corner.x + self.position.x
        self.sprite.y = corner.y + self.position.y

    def render(self):
        self.data.renderer.render(self.sprite)

