import pyasge


class Camera:
    def __init__(self, data):
        self.data = data
        self.camera = pyasge.Camera(self.data.screen_size[0], self.data.screen_size[1])

        self.default_view = pyasge.CameraView()
        self.default_view.min_x = 0
        self.default_view.max_x = self.data.screen_size[0]
        self.default_view.min_y = 0
        self.default_view.max_y = self.data.screen_size[1]

    def look_at(self, player_sprite: pyasge.Point2D) -> pyasge.Point2D:
        camera_x = player_sprite.x
        camera_y = player_sprite.y

        if camera_x <= self.data.screen_size[0] * 0.5:
            camera_x = self.data.screen_size[0] * 0.5
        elif camera_x >= self.data.map.width * self.data.tile_size - self.data.screen_size[0] * 0.5:
            camera_x = self.data.map.width * self.data.tile_size - self.data.screen_size[0] * 0.5

        if camera_y <= self.data.screen_size[1] * 0.5:
            camera_y = self.data.screen_size[1] * 0.5
        elif camera_y >= self.data.map.height * self.data.tile_size - self.data.screen_size[1] * 0.5:
            camera_y = self.data.map.height * self.data.tile_size - self.data.screen_size[1] * 0.5

        self.camera.lookAt(pyasge.Point2D(round(camera_x), round(camera_y)))

        return pyasge.Point2D(self.camera.view.min_x, self.camera.view.min_y)
