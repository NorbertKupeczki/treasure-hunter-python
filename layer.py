import pyasge

class Layer:
    def __init__(self):
        self.name = ""
        self.tiles = []
        self.layer_cost = 0


    def initTilePos(self) -> None:

        for x in self.tiles:
            x.sprite.y = 8 * x.coordinate[1]
            x.sprite.x = 8 * x.coordinate[0]


    def render(self, renderer: pyasge.Renderer) -> None:

        for tile in self.tiles:
            renderer.render(tile.sprite)