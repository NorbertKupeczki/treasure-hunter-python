import pyasge


class MapTile:
    def __init__(self, coords):
        self.sprite = pyasge.Sprite()
        self.coordinate = coords
        self.passable = True  #  to implement

    def load(self, filename: str, text_x: int) -> None:
        self.sprite.loadTexture(filename)

        text_x -= 1

        temp_string_x = str(text_x / 14)
        temp_string_x = int(temp_string_x.split(".")[0])
        text_x = text_x - (14 * temp_string_x)
        self.sprite.src_rect[pyasge.Sprite.SourceRectIndex.START_X] = text_x * 8
        self.sprite.src_rect[pyasge.Sprite.SourceRectIndex.LENGTH_X] = 8

        self.sprite.src_rect[pyasge.Sprite.SourceRectIndex.START_Y] = temp_string_x * 8
        self.sprite.src_rect[pyasge.Sprite.SourceRectIndex.LENGTH_Y] = 8

        self.sprite.width = 64  # Magnified for testing purposes, original scalar was 8 - Norbert
        self.sprite.height = 64  # Magnified for testing purposes, original scalar was 8 - Norbert

