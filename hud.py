import pyasge
from healthbar import HealthBar


class HUD:
    def __init__(self, data):
        self.data = data

        self.health_bar = HealthBar(data)

        self.ui_text = pyasge.Text(self.data.fonts['main_text'], "DEMO")
        self.ui_text.colour = pyasge.COLOURS.RED
        self.ui_text.z_order = 5

        self.world_coordinates = pyasge.Text(self.data.fonts['hud_text'], "World: ")
        self.world_coordinates.colour = pyasge.COLOURS.LIME
        self.world_coordinates.z_order = 5

        self.tile_coordinates = pyasge.Text(self.data.fonts['hud_text'], "Tile: ")
        self.tile_coordinates.colour = pyasge.COLOURS.LIME
        self.tile_coordinates.z_order = 5

        self.score = pyasge.Text(self.data.fonts['hud_text'], "Score: "+str(self.data.score))
        self.score.colour = pyasge.COLOURS.LIME
        self.score.z_order = 5

        self.coords_on = False

    def render_hud(self, corner: pyasge.Point2D):
        self.ui_text.position = [self.data.screen_size[0] * 0.5 - self.ui_text.width * 0.5 + corner.x,
                                 self.data.screen_size[1] - 5 + corner.y]
        self.score.position = [corner.x + 5, corner.y + 25]
        self.world_coordinates.position = [corner.x + 5, corner.y + 45]
        self.tile_coordinates.position = [corner.x + 5, corner.y + 65]

        self.world_coordinates.string = "World: " + str(int(self.data.world_loc.x)) + ':' + str(int(self.data.world_loc.y))
        self.tile_coordinates.string = "Tile: " + str(int(self.data.tile_loc.x)) + ':' + str(int(self.data.tile_loc.y))
        if self.coords_on:
            self.data.renderer.render(self.tile_coordinates)
            self.data.renderer.render(self.world_coordinates)
        self.data.renderer.render(self.ui_text)
        self.data.renderer.render(self.score)
        self.health_bar.render_health_bar(self.data.renderer, corner)

    def update_score(self, score: int):
        self.score.string = "Score: "+str(score)
