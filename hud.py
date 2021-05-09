import pyasge


class HUD:
    def __init__(self, data):
        self.data = data
        self.ui_text = pyasge.Text(self.data.fonts['kenvector'], "DEMO")
        self.ui_text.colour = pyasge.COLOURS.RED
        self.ui_text.z_order = 2

    def render_hud(self, corner: pyasge.Point2D):
        self.ui_text.position = [self.data.screen_size[0] * 0.5 - self.ui_text.width * 0.5 + corner.x,
                                 self.data.screen_size[1] - 5 + corner.y]
        self.data.renderer.render(self.ui_text)
