import pyasge

class Layer:
    def __init__(self):
        self.name = ""
        self.tiles = []
        self.num_tiles = 0
        self.layer_cost = 0


    def initTilePos(self) -> None:


        if self.num_tiles == 0:

            for row in self.tiles:
                for tile in row:
                    tile.sprite.y = 8 * tile.coordinate[1]
                    tile.sprite.x = 8 * tile.coordinate[0]

        else:
            for x in self.tiles:
                x.sprite.y = 8 * x.coordinate[1]
                x.sprite.x = 8 * x.coordinate[0]


    def render(self, renderer: pyasge.Renderer) -> None:

        if self.num_tiles == 0:
            for row in self.tiles:
                for tile in row:
                    renderer.render(tile.sprite)

        else:
            for tile in self.tiles:
                renderer.render(tile.sprite)
