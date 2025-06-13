# maze_generator.py
import random


class MazeGenerator:

    def __init__(self, length):
        self.length = length
        self.num_of_nodes = length ** 2
        self.top = 0
        self.left = 1
        self.bottom = 2
        self.right = 3

    def create_mst(self):
        mst = [
            [0, 0, 0, 0] for _ in range(self.num_of_nodes)
        ]

        unvisited = [node for node in range(self.num_of_nodes)]
        node = unvisited[0]
        visited = [node]
        unvisited.remove(node)

        while len(unvisited) > 0:
            total_edges = self.edges(visited)
            random_edge = random.choice(total_edges)
            node, next_node = random_edge

            direction = self.get_neighbour_direction(node, next_node)
            mst[node][direction] = 1

            neighbour_direction = self.get_neighbour_direction(next_node, node)
            mst[next_node][neighbour_direction] = 1

            visited.append(next_node)
            unvisited.remove(next_node)

        return mst

    def edges(self, visited):
        total_edges = []

        for node in visited:
            row = node // self.length
            column = node % self.length

            if row > 0:
                node_above = node - self.length
                if node_above not in visited:
                    total_edges.append((node, node_above))

            if row < self.length - 1:
                node_below = node + self.length
                if node_below not in visited:
                    total_edges.append((node, node_below))

            if column > 0:
                left_node = node - 1
                if left_node not in visited:
                    total_edges.append((node, left_node))

            if column < self.length - 1:
                right_node = node + 1
                if right_node not in visited:
                    total_edges.append((node, right_node))

        return total_edges

    def get_neighbour_direction(self, node, next_node):
        if node - self.length == next_node:
            return self.top
        if node - 1 == next_node:
            return self.left
        if node + self.length == next_node:
            return self.bottom
        if node + 1 == next_node:
            return self.right
