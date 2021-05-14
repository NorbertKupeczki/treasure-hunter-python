
import math





class EnemyMain:

    def distanceToPlayer(self, x, y, enemy_tile):  # distance from the player in tile form

        dx = abs(x - enemy_tile[0])
        dy = abs(y - enemy_tile[1])

        return math.sqrt(dx * dx + dy * dy)






    pass