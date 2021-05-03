import pyasge


class MapTile:
    def __init__(self, coords):
        self.sprite = pyasge.Sprite()
        self.coordinate = coords
        self.passable = True  #  to implement

    def load(self, filename: str) -> None:
        self.sprite.loadTexture(filename)

