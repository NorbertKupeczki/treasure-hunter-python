from queue import PriorityQueue
from math import sqrt
from typing import Tuple


class PathFinder:
    def __init__(self, data):
        self.cost_map = data.map.cost_map

    def pathfinder(self, start, end):
        frontier = PriorityQueue()
        frontier.put((0, start))
        came_from = dict()
        cost_so_far = dict()
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            coordinates = frontier.get()[1]
            current = Node(coordinates[1], coordinates[0])
            current.update_neighbors(self.cost_map)

            if current.get_position() == end:
                break

            for next in current.neighbors:
                new_cost = cost_so_far[current.get_position()] + self.cost_map[next.get_position()[1]][
                    next.get_position()[0]]
                if next.get_position() not in cost_so_far or new_cost < cost_so_far[next.get_position()]:
                    cost_so_far[next.get_position()] = new_cost
                    priority = new_cost + self.heuristics(end, next.get_position())
                    frontier.put((priority, next.get_position()))
                    came_from[next.get_position()] = current.get_position()

        return self.reconstruct_path(came_from, start, end)

    def heuristics(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)
        return sqrt(dx * dx + dy * dy)

    def reconstruct_path(self, came_from, start, end):
        current = end
        path = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()
        return path


class Node:
    def __init__(self, col, row) -> None:
        self.x = row
        self.y = col
        self.neighbors = []
        self.WIDTH = 60
        self.HEIGHT = 60

    def get_position(self) -> Tuple[int, int]:
        return self.x, self.y

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.x < self.WIDTH - 1 and not grid[self.y][self.x + 1] > 100:
            self.neighbors.append(Node(self.y, self.x + 1))

        if self.x < self.WIDTH - 1 and self.y < self.HEIGHT - 1 and not grid[self.y + 1][self.x + 1] > 100:
            self.neighbors.append(Node(self.y + 1, self.x + 1))

        if self.y < self.HEIGHT - 1 and not grid[self.y + 1][self.x] > 100:
            self.neighbors.append(Node(self.y + 1, self.x))

        if self.y < self.HEIGHT - 1 and self.x > 0 and not grid[self.y + 1][self.x - 1] > 100:
            self.neighbors.append(Node(self.y + 1, self.x - 1))

        if self.x > 0 and not grid[self.y][self.x - 1] > 100:
            self.neighbors.append(Node(self.y, self.x - 1))

        if self.x > 0 and self.y > 0 and not grid[self.y - 1][self.x - 1] > 100:
            self.neighbors.append(Node(self.y - 1, self.x - 1))

        if self.y > 0 and not grid[self.y - 1][self.x] > 100:
            self.neighbors.append(Node(self.y - 1, self.x))

        if self.y > 0 and self.x < self.WIDTH - 1 and not grid[self.y - 1][self.x + 1] > 100:
            self.neighbors.append(Node(self.y - 1, self.x + 1))
