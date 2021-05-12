# -*- coding: utf-8 -*-
import pyasge
from gamedata import GameData
from gameplay import GamePlay
from startmenu import StartMenu
from gameover import GameOver
from winnerwinner import WinnerWinner
from levelmanager import LevelManager
from nextlevel import NextLevel
from gamestate import GameStateID
from camera import Camera


class MyASGEGame(pyasge.ASGEGame):

    def __init__(self, settings):
        """
        Initialises the game and sets up the shared data.
        @param settings: The initial game and window settings.
        """
        pyasge.ASGEGame.__init__(self, settings)
        self.data = GameData()
        self.data.inputs = self.inputs
        self.data.renderer = self.renderer
        self.data.fonts['title_text'] = self.renderer.loadFont("/data/fonts/oblivion-font.ttf", 60)
        self.data.fonts['main_text'] = self.renderer.loadFont("/data/fonts/oblivion-font.ttf", 40)
        self.data.fonts['hud_text'] = self.renderer.loadFont("/data/fonts/oblivion-font.ttf", 18)
        self.data.screen_size = settings.window_width, settings.window_height
        self.data.camera = Camera(self.data)
        self.active_state = StartMenu(self.data)

    def update(self, game_time: pyasge.GameTime) -> None:
        """
        This is the fixed time-step update function. Fixed
        time-steps are useful for simulations and physics
        calculations where behaviour should be deterministic
        over time. Use ``fixed_timestep`` to ensure simulations
        are consistent over time.
        @param game_time: The tick and frame deltas.
        """

        # if self.active_state:
        #     self.active_state.update(game_time)

        new_state = self.active_state.update(game_time)
        if self.active_state.id != new_state:
            if new_state is GameStateID.EXIT:
                self.signalExit()
            elif new_state is GameStateID.START_MENU:
                self.active_state = StartMenu(self.data)
            elif new_state is GameStateID.GAMEPLAY:
                self.active_state = GamePlay(self.data)
            elif new_state is GameStateID.GAME_OVER:
                self.active_state = GameOver(self.data)
            elif new_state is GameStateID.WINNER_WINNER:
                self.active_state = WinnerWinner(self.data)
            elif new_state is GameStateID.LEVEL_MANAGER:
                self.active_state = LevelManager(self.data)
            elif new_state is GameStateID.NEXT_LEVEL:
                self.active_state = NextLevel(self.data)
            else:
                print("Unexpected error")
                self.signalExit()

    def render(self, game_time: pyasge.GameTime) -> None:
        """
        This is the variable time-step function. Use to update
        animations and to render the game-world. The use of
        ``frame_time`` is essential to ensure consistent performance.
        @param game_time: The tick and frame deltas.
        """
        if self.active_state:
            self.active_state.render(game_time)


def main():
    """
    Creates the game and runs it
    For ASGE Games to run they need settings. These settings
    allow changes to the way the game is presented, its
    simulation speed and also its dimensions. For this project
    the FPS and fixed updates are capped at 60hz and Vsync is
    set to adaptive.
    """
    settings = pyasge.GameSettings()
    settings.window_width = 1024
    settings.window_height = 768
    settings.fixed_ts = 60
    settings.fps_limit = 60
    settings.vsync = pyasge.Vsync.ADAPTIVE
    game = MyASGEGame(settings)
    game.run()


if __name__ == "__main__":
    main()
