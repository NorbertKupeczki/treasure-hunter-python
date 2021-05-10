import pyasge

from fsm import FSM
from projetiles import Projectiles

class Enemy:
    def __init__(self):
        self.sprite = pyasge.Sprite()
        self.sprite.loadTexture("/data/images/character_zombie_idle.png")