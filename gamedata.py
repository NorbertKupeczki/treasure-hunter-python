import pyasge


class GameData:
    """ GameData stores the data that needs to be shared

    When using multiple states in a game, you will find that
    some game data needs to be shared. In this instance GameData
    is used to share access to data that a the game and running
    states may need. You can think of this as a "blackboard" in
    UE terms.
    """

    def __init__(self) -> None:
        self.fonts = {}
        self.inputs = None
        self.renderer = None
        self.screen_size = {}

        self.camera = None
        self.map = None
        self.enemies = None
        self.enemy_projectiles = None
        self.breakables = None
        self.gems = None

        self.tile_size = int(64)
        self.world_loc = pyasge.Point2D(0, 0)
        self.tile_loc = pyasge.Point2D(0, 0)
        self.level_selected = 1
        self.score = 0
