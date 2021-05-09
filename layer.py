import pyasge

class Layer:
    def __init__(self):
        self.name = ""
        self.tiles = []
        self.layer_cost = 0
        self.passable_t = 1


    def initTilePos(self) -> None:

        if self.passable_t == 0:
            for x in self.tiles:
                x.passable = False

        for x in self.tiles:
            x.sprite.y = 64 * x.coordinate[1]  # Magnified for testing purposes, original scalar was 8 - Norbert
            x.sprite.x = 64 * x.coordinate[0]  # Magnified for testing purposes, original scalar was 8 - Norbert


    def render(self, renderer: pyasge.Renderer) -> None:

        for tile in self.tiles:
            renderer.render(tile.sprite)