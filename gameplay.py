import pyasge
from gamestate import GameState, GameStateID
from player import Player
from enemy import Enemy
from rangedEnemy import EnemyR
from door import Door
from hud import HUD
from projetiles import Projectiles

from map import Map

from gem import Gem
from vase import Vase


class GamePlay(GameState):
    def __init__(self, data):
        super().__init__(data)
        self.id = GameStateID.GAMEPLAY
        self.data.enemy_projectiles = Projectiles(data)
        self.update_list = []

        self.data.gems = []
        self.data.enemies = []
        self.data.breakables = []
        self.load_game_map(self.data.level_selected)

        # initialising HUD and the player
        self.hud = HUD(data)
        self.player = Player(data, self.data.map.starting_location)
        self.update_list.append(self.player)

        self.entrance_door = Door(self.data.map.starting_location)
        self.exit_door = Door(self.data.map.end_location)
        self.update_list.append(self.exit_door)

        # register the key handler for this class
        self.data.inputs.addCallback(pyasge.EventType.E_KEY, self.input)

        # track key states
        self.keys = {
            pyasge.KEYS.KEY_A: False,
            pyasge.KEYS.KEY_D: False,
            pyasge.KEYS.KEY_W: False,
            pyasge.KEYS.KEY_S: False,
            pyasge.KEYS.KEY_EQUAL: False,
            pyasge.KEYS.KEY_MINUS: False,
            pyasge.KEYS.KEY_SPACE: False,
            pyasge.KEYS.KEY_G: False,
            pyasge.KEYS.KEY_C: False,
            pyasge.KEYS.KEY_ESCAPE: False,
            pyasge.KEYS.KEY_Q: False,  # To test player health system
            pyasge.KEYS.KEY_E: False  # To test player health system
        }

        self.game_pad = self.data.inputs.getGamePad(0)

        self.enemies_left = 0


    def load_game_map(self, level_num) -> None:
        self.data.map = Map(str(level_num))

        for gem in self.data.map.layers[2].tiles:
            self.data.gems.append(Gem(pyasge.Point2D((gem.coordinate[0] + 0.5) * self.data.tile_size,(gem.coordinate[1] + 0.5) * self.data.tile_size)))

        ranged_enemy_counter = 0
        for enemy in self.data.map.layers[3].tiles:
            ranged_enemy_counter += 1
            if ranged_enemy_counter == 3:
                self.data.enemies.append(EnemyR(self.data, pyasge.Point2D(enemy.coordinate[0] * self.data.tile_size,enemy.coordinate[1] * self.data.tile_size), 8, 10, 80))   # the 3 numbers at the end mean the range of vision range, the health, the speed
                ranged_enemy_counter = 0
            else:
                self.data.enemies.append(Enemy(self.data, pyasge.Point2D(enemy.coordinate[0] * self.data.tile_size, enemy.coordinate[1] * self.data.tile_size), 5, 10, 60))

        self.enemies_left = len(self.data.enemies)



        for breakable in self.data.map.layers[4].tiles:
            self.data.breakables.append(Vase(pyasge.Point2D(breakable.coordinate[0] * self.data.tile_size,
                                                            breakable.coordinate[1] * self.data.tile_size)))

    def input(self, event: pyasge.KeyEvent) -> None:
        if event.action is not pyasge.KEYS.KEY_REPEATED:
            self.keys[event.key] = event.action is pyasge.KEYS.KEY_PRESSED

        # Turn game pad ON/OFF if game pad is connected
        if self.keys[pyasge.KEYS.KEY_G]:
            if event.action is pyasge.KEYS.KEY_PRESSED:
                if self.game_pad.connected:
                    if self.player.toggle_game_pad():
                        print("Game pad controls enabled")
                    else:
                        print("Game pad controls disabled")
                else:
                    print("No game pad connected!")

        if self.keys[pyasge.KEYS.KEY_SPACE]:
            if event.action is pyasge.KEYS.KEY_PRESSED:
                self.player.shoot()

        if self.keys[pyasge.KEYS.KEY_C]:
            if event.action is pyasge.KEYS.KEY_PRESSED:
                self.hud.coords_on = not self.hud.coords_on

        # To test player health system
        if self.keys[pyasge.KEYS.KEY_Q]:
            if event.action is pyasge.KEYS.KEY_PRESSED:
                self.player.health -= 1
                self.hud.health_bar.lose_health(self.player.health)

        if self.keys[pyasge.KEYS.KEY_E]:
            if event.action is pyasge.KEYS.KEY_PRESSED:
                self.player.health = 5
                self.hud.health_bar.heal()

    def update(self, game_time: pyasge.GameTime) -> GameStateID:

        for item in self.update_list:
            item.update(game_time)

        self.player.move_player(game_time, self.keys, self.game_pad)
        """
        Updating the enemy array
        """

        if len(self.data.enemies) != self.enemies_left:
            self.enemies_left = len(self.data.enemies)
            for x in self.data.enemies:
                x.re_calc = True


        for enemy in self.data.enemies:
            enemy.move_enemy(game_time, pyasge.Point2D(self.data.world_loc.x, self.data.world_loc.y), pyasge.Point2D(self.data.tile_loc.x, self.data.tile_loc.y))
            enemy.update() # call the update function to change texture

        for x in range(len(self.data.enemies)):
            saved = x
            for z in range(len(self.data.enemies)):
                if z != saved:
                    if self.data.enemies[x].saved_tile[0] == self.data.enemies[z].enemy_curr_tile_cord[0] and self.data.enemies[x].saved_tile[1] == self.data.enemies[z].enemy_curr_tile_cord[1]:
                        self.data.enemies[x].re_path(self.data.enemies[z].enemy_curr_tile_cord[0], self.data.enemies[z].enemy_curr_tile_cord[1])  # should send the coords of the obstacle so they dont overlap by mistake

        """
        Updating enemy projectiles, if the function returns True,
        the player loses 1 HP and the health bar gets updated
        """
        if self.data.enemy_projectiles.update_projectiles(game_time, self.player):
            self.player.health -= 1
            self.hud.health_bar.lose_health(self.player.health)
        """
        Updating the gems, if all the gems are collected, the exit door opens
        If the player is close enough to the exit door, the game goes to the next level screen
        If the player was on the last level, the game goes to the win screen
        """
        if self.data.gems:
            for gem in self.data.gems:
                if gem.check_collision(self.player.sprite):
                    # gem_loc = pyasge.Point2D((gem.sprite.x + gem.sprite.width * 0.5) / self.data.tile_size - 0.5,
                    #                          (gem.sprite.y + gem.sprite.height * 0.5) / self.data.tile_size - 0.5)
                    # print(f"Gem picked up from ({int(gem_loc.x)},{int(gem_loc.y)})")
                    # for tile in self.data.map.layers[2].tiles:
                    #     if tile.coordinate[0] == int(gem_loc.x) and tile.coordinate[1] == int(gem_loc.y):
                    #         self.data.map.layers[2].tiles.remove(tile)
                    self.data.score += gem.value
                    self.hud.update_score(self.data.score)
                    self.data.gems.remove(gem)
        else:
            if not self.exit_door.door_open:
                self.exit_door.door_open = True

            if pyasge.Point2D.distance(self.player.get_sprite(), self.exit_door.get_centre()) <= self.data.tile_size:
                if self.data.level_selected == 7:
                    return GameStateID.WINNER_WINNER
                else:
                    return GameStateID.NEXT_LEVEL

        if self.player.game_pad_enabled:
            if self.data.inputs.getGamePad(0).RIGHT_TRIGGER != -1.0:
                self.player.shoot()

        if self.keys[pyasge.KEYS.KEY_ESCAPE]:
            return GameStateID.EXIT
        elif self.player.health <= 0:
            return GameStateID.GAME_OVER
        else:
            return GameStateID.GAMEPLAY

    def render(self, game_time: pyasge.GameTime) -> None:
        corner = self.data.camera.look_at(self.player.get_sprite())
        self.data.renderer.setProjectionMatrix(self.data.camera.camera.view)
        self.hud.render_hud(corner)
        self.data.map.render(self.data.renderer)
        self.data.renderer.render(self.entrance_door.sprite)
        self.data.renderer.render(self.exit_door.sprite)
        self.data.renderer.render(self.player.sprite)
        self.player.render_bullets()
        for enemy in self.data.enemies:
            self.data.renderer.render(enemy.sprite)
        for projectile in self.data.enemy_projectiles.projectiles:
            self.data.renderer.render(projectile.sprite)

        for gem in self.data.gems:
            self.data.renderer.render(gem.sprite)
        for vase in self.data.breakables:
            self.data.renderer.render(vase.sprite)

        for enemy in self.data.enemies:
            self.data.renderer.render(enemy.sprite)
