import pyasge
from healthbar import HealthBar


class HUD:
    def __init__(self, data):
        self.data = data

        self.health_bar = HealthBar(data)

        self.ui_texts = [
            UIText(pyasge.Point2D(5, 20), pyasge.COLOURS.LIME, 'hud_text', "Score: " + str(self.data.score), self.data),
            UIText(pyasge.Point2D(120, 20), pyasge.COLOURS.LIME, 'hud_text', "World: ", self.data),
            UIText(pyasge.Point2D(300, 20), pyasge.COLOURS.LIME, 'hud_text', "Tile: ", self.data),
            UIText(pyasge.Point2D(self.data.screen_size[0] - 100, 20), pyasge.COLOURS.LIME, 'hud_text',
                   "Level: "+str(self.data.level_selected), self.data)
        ]
        self.ui_texts[1].visible = False
        self.ui_texts[2].visible = False

    def render_hud(self, corner: pyasge.Point2D):
        self.update_coordinates()

        for item in self.ui_texts:
            item.update_pos(corner)
            if item.visible:
                item.render()
        self.health_bar.render_health_bar(self.data.renderer, corner)

    def update_score(self, score: int):
        self.ui_texts[0].update_text("Score: "+str(score))

    def update_coordinates(self):
        self.ui_texts[1].update_text("World: " + str(int(self.data.world_loc.x)) + ':' + str(int(self.data.world_loc.y)))
        self.ui_texts[2].update_text("Tile: " + str(int(self.data.tile_loc.x)) + ':' + str(int(self.data.tile_loc.y)))

    def switch_coordinates(self):
        self.ui_texts[1].visible = not self.ui_texts[1].visible
        self.ui_texts[2].visible = not self.ui_texts[2].visible


class UIText:
    def __init__(self, position: pyasge.Point2D, colour: pyasge.Colour, font: str, text: str, data):
        self.data = data
        self.text = pyasge.Text(self.data.fonts[font], text)
        self.text.colour = colour
        self.text.z_order = self.data.z_order['UI']
        self.position = position
        self.visible = True

    def update_pos(self, corner: pyasge.Point2D):
        self.text.position = [corner.x + self.position.x, corner.y + self.position.y]

    def update_text(self, text: str):
        self.text.string = text

    def render(self):
        self.data.renderer.render(self.text)
