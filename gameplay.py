import pyasge
from gamestate import GameState, GameStateID
from player import Player
from door import Door
from hud import HUD
from projectiles import Projectiles
from maploader import MapLoader


class GamePlay(GameState):
    def __init__(self, data):
        super().__init__(data)
        self.id = GameStateID.GAMEPLAY
        self.data.enemy_projectiles = Projectiles(data)
        self.update_list = []

        MapLoader.load_game_map(self.data)

        # initialising HUD and the player
        self.hud = HUD(data)
        self.player = Player(data)
        self.update_list.append(self.player)

        self.exit_door = Door('end', data)
        self.update_list.append(Door('start', data))
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

        self.enemies_left = len(self.data.enemies)

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

        if self.keys[pyasge.KEYS.KEY_C]:
            if event.action is pyasge.KEYS.KEY_PRESSED:
                self.hud.switch_coordinates()

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
        Updating the enemy array, collision check between player and zombie is located here to reduce code complexity
        by removing another for loop
        """
        if len(self.data.enemies) != self.enemies_left:
            self.enemies_left = len(self.data.enemies)
            for enemy in self.data.enemies:
                enemy.re_calc = True

        for enemy in self.data.enemies:
            enemy.move_enemy(game_time, pyasge.Point2D(self.data.world_loc.x, self.data.world_loc.y),
                             pyasge.Point2D(self.data.tile_loc.x, self.data.tile_loc.y))
            enemy.update()  # call the update function to change texture
            if not self.player.invulnerable:
                if enemy.playerZombieCollision(pyasge.Point2D(self.data.tile_loc.x, self.data.tile_loc.y)):
                    self.player.suffer_damage(self.hud.health_bar)

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
            if not self.player.invulnerable:
                self.player.suffer_damage(self.hud.health_bar)

        for item in self.data.collectibles:
            if item.check_collision(self.player.sprite):
                self.player.max_heal()
                self.hud.health_bar.heal()
                self.data.collectibles.remove(item)
        """
        Updating the gems, if all the gems are collected, the exit door opens
        If the player is close enough to the exit door, the game goes to the next level screen
        If the player was on the last level, the game goes to the win screen
        """
        if self.data.gems:
            for gem in self.data.gems:
                if gem.check_collision(self.player.sprite):
                    self.data.score += gem.value
                    self.data.gems.remove(gem)
        else:
            if not self.exit_door.door_open:
                self.exit_door.door_open = True

            if pyasge.Point2D.distance(self.player.get_sprite(), self.exit_door.get_centre()) <= self.data.tile_size:
                if self.data.level_selected == 7:
                    return GameStateID.WINNER_WINNER
                else:
                    return GameStateID.NEXT_LEVEL

        self.hud.update_score(self.data.score)

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
        for item in self.update_list:
            item.render()
        for enemy in self.data.enemies:
            self.data.renderer.render(enemy.sprite)
        for projectile in self.data.enemy_projectiles.projectiles:
            self.data.renderer.render(projectile.sprite)

        for gem in self.data.gems:
            self.data.renderer.render(gem.sprite)

        for item in self.data.collectibles:
            self.data.renderer.render(item.sprite)

        for vase in self.data.breakables:
            self.data.renderer.render(vase.sprite)



