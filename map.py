import pyasge
from layer import Layer
from tile import MapTile
import json


class Map:
    def __init__(self, level):
        self.layers = []
        self.width = 0
        self.height = 0
        self.cost_map = []
        self.starting_location = pyasge.Point2D()
        self.end_location = pyasge.Point2D()
        self.loadMap(level)

    def loadMap(self, level) -> None:  # takes the level we want to load in

        with open('Maps') as f:  # open the json type file named Maps
            data = json.load(f)

        for Data in data[level]:    # search in the json file for an array with the name of the level
            self.layers = [Layer() for i in range(Data['layer_nums'])]     # creates a number of Layer() obj depending on what is stated in the json file

            layer_index = 0    # needed to traverse the self.layers[] array so we can access the specific layer obj

            size_string = Data['size']  # the size of the map is saved as a string
            self.width = int(size_string.split()[0]) # python can split strings when it detects spaces
            self.height = int(size_string.split()[1])
            self.cost_map = [[0 for i in range(self.width)] for j in range(self.height)]  # creates a 2d map for the costs

            start_string = Data['start_pos']
            self.starting_location = pyasge.Point2D(int(start_string.split()[0]) * 64,
                                                    int(start_string.split()[1]) * 64)
            end_string = Data['end_pos']
            self.end_location = pyasge.Point2D((int(end_string.split()[0]) + 0.5) * 64,
                                               (int(end_string.split()[1]) + 0.5) * 64)

            for layer in Data['Layers']: # for every layer array in the Json file
                self.layers[layer_index].passable_t = layer['walk-through']
                self.layers[layer_index].name = layer['layer_name']
                self.layers[layer_index].layer_cost = layer['layer_cost']
                self.layers[layer_index].show = layer['show']

                x = 0
                y = 0
                iteration = 0

                for data in layer["data"]:

                    if data != 0:
                        self.layers[layer_index].tiles.append(MapTile((x, y)))

                        if self.layers[layer_index].show != 0:
                            self.layers[layer_index].tiles[iteration].load("data/tilesheet_complete.png", data)

                        self.cost_map[y][x] += self.layers[layer_index].layer_cost
                        iteration += 1

                    x += 1
                    if x == self.width:
                        x = 0
                        y += 1

                if self.layers[layer_index].show != 0:
                    self.layers[layer_index].initTilePos()

                layer_index += 1

    def render(self, renderer: pyasge.Renderer) -> None:

        for x in range(len(self.layers)):  # for every layer send the render to them
            self.layers[x].render(renderer)
