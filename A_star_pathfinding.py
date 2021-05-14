import math



class Node:

    def __init__(self, Tile):

        self.parent = None  # a reference to the parent which will be type node
        self.tile = Tile

        self.h_score = 0
        self.g_score = 0
        self.f_score = 0



class Pathfinding:

    #send the start and the goal

    def __init__(self, Start, Goal, Costs, width, height) -> None:
        self.costs = Costs
        self.start = Node(Start)
        self.goal = Node(Goal)

        self.widht = width
        self.height = height

        self.decided_path = []

        self.decided_path = self.A_path(self.start, self.goal)
        self.decided_path.insert(0, self.goal)



    def heuristic(self, current_node, goal):

        dx = abs(current_node.tile[0] - goal.tile[0])
        dy = abs(current_node.tile[1] - goal.tile[1])

        return math.sqrt(dx * dx + dy * dy)



    def lowest_node(self, list, goal):

        smallest = 10000000000

        for i in range(len(list)):

            list[i].f_score = list[i].g_score + self.costs[list[i].tile[1]][list[i].tile[0]] + self.heuristic(list[i], goal)

            if list[i].f_score < smallest:
                smallest = list[i].g_score + self.heuristic(list[i], goal)

                saved_index = i

        return list[saved_index]


    def final_path(self, node):
        path = []

        while node.parent is not None:
            node = node.parent
            path.append(node)

        return path



    def get_neighbours(self, current_node):

        neighbours = []

        if current_node.tile[0] + 1 <= self.widht - 1:
            neighbours.append(Node((current_node.tile[0] + 1, current_node.tile[1]))) # right

        if current_node.tile[0] - 1 >= 0:
            neighbours.append(Node((current_node.tile[0] - 1, current_node.tile[1]))) # left

        if current_node.tile[1] + 1 <= self.height - 1:
            neighbours.append(Node((current_node.tile[0], current_node.tile[1] + 1))) # bot

        if current_node.tile[1] - 1 >= 0:
            neighbours.append(Node((current_node.tile[0], current_node.tile[1] - 1)))   # top

        for i in range(len(neighbours)):
            neighbours[i].g_score = current_node.g_score + 1
            neighbours[i].parent = current_node
        return neighbours



    def A_path(self, start, goal):

        open_List = []

        open_List.append(start)

        closed_List = []

        while len(open_List) != 0:

            current_node = self.lowest_node(open_List, goal)

            if current_node.tile == goal.tile:
                return self.final_path(current_node)

            open_List.remove(current_node)
            closed_List.append(current_node)

            neighbour = self.get_neighbours(current_node)

            for i in range(len(neighbour)):

                present = False

                for j in range(len(closed_List)):

                    if neighbour[i].tile == closed_List[j].tile:

                        present = True


                if present:
                    pass
                else:
                    neighbour[i].g_score = neighbour[i].parent.g_score + self.costs[neighbour[i].tile[1]][neighbour[i].tile[0]]
                    neighbour[i].f_score = neighbour[i].g_score + self.heuristic(neighbour[i], goal)

                    present = False

                    for x in range(len(open_List)):

                        if neighbour[i].tile == open_List[x].tile:
                            present = True


                    if present:
                        open_neighbour = neighbour[i]
                        if neighbour[i].g_score < open_neighbour.g_score:
                            open_neighbour.g_score = neighbour[i].g_score
                            open_neighbour.parent = neighbour[i].parent

                    else:
                        open_List.append(neighbour[i])


        return False

    def pop(self):
        value = self.decided_path.pop()
        return value