import pyasge


class Camera:
    def __init__(self):
        self.camera = pyasge.Camera(1024, 768)

        self.default_view = pyasge.CameraView()
        self.default_view.min_x = 0
        self.default_view.max_x = 1024
        self.default_view.min_y = 0
        self.default_view.max_y = 768

    def look_at(self, player_sprite: pyasge.Point2D) -> pyasge.Point2D:
        camera_x = player_sprite.x
        camera_y = player_sprite.y

        if camera_x <= 512:
            camera_x = 512
        elif camera_x >= 3328:
            camera_x = 3328

        if camera_y <= 384:
            camera_y = 384
        elif camera_y >= 1792:
            camera_y = 1792

        self.camera.lookAt(pyasge.Point2D(camera_x, camera_y))

        return pyasge.Point2D(self.camera.view.min_x, self.camera.view.min_y)


