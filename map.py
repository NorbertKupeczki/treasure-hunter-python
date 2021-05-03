import pyasge
from layer import Layer
from tile import MapTile
import json

class Map:
    def __init__(self, level):
        self.layers = []
        self.width = 0
        self.height = 0
        self.cost_map =[]
        self.loadMap(level)


    def loadMap(self, level) -> None:

        with open('Maps') as f:
            data = json.load(f)

        for Data in data[level]:
            self.layers = [Layer() for i in range(Data['layer_nums'])]

            layer_index = 0

            size_string = Data['size']
            self.width = int(size_string.split()[0])
            self.height = int(size_string.split()[1])
            self.cost_map = [[0 for i in range(self.width)] for j in range(self.height)]

            for layer in Data['Layers']:

                self.layers[layer_index].name = layer['layer_name']

                self.layers[layer_index].num_tiles = layer['num_tiles']

                self.layers[layer_index].layer_cost = layer['layer_cost']

                if (str(layer['tile_cords']) == "all"):
                    self.layers[layer_index].tiles = [[MapTile((0, 0)) for i in range(self.width)] for j in range(self.height)]

                    for y in range(self.height):
                        for x in range(self.width):
                            self.layers[layer_index].tiles[y][x].coordinate = (x, y)
                            self.layers[layer_index].tiles[y][x].load(layer['tile_text_filename'])
                            self.cost_map[y][x] += self.layers[layer_index].layer_cost

                else:
                    self.layers[layer_index].tiles = [MapTile((0, 0)) for i in range(self.layers[layer_index].num_tiles)]

                    for x in range(int(layer['num_tiles'])):
                        temp_string = str(layer['tile_cords']).split()[x]
                        x_coord = int(temp_string[0])
                        y_coord = int(temp_string[2])

                        self.layers[layer_index].tiles[x].coordinate = (x_coord, y_coord)
                        self.layers[layer_index].tiles[x].load(layer['tile_text_filename'][layer['tile_text_index'][x]])
                        self.cost_map[y_coord][x_coord] += self.layers[layer_index].layer_cost

                self.layers[layer_index].initTilePos()
                layer_index += 1


    def render(self, renderer: pyasge.Renderer) -> None:

        for x in range(len(self.layers)):
            self.layers[x].render(renderer)