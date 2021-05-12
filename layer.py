import pyasge


class Layer:
    def __init__(self):
        self.name = ""
        self.tiles = []
        self.layer_cost = 0
        self.passable_t = 1
        self.show = 1

    def initTilePos(self) -> None:

        if self.passable_t == 0:
            for x in self.tiles:
                x.passable = False

        for x in self.tiles:
            x.sprite.y = 64 * x.coordinate[1]
            x.sprite.x = 64 * x.coordinate[0]

    def render(self, renderer: pyasge.Renderer) -> None:

        if self.show != 0:
            for tile in self.tiles:
                renderer.render(tile.sprite)