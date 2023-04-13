import random
import sys


sys.setrecursionlimit(10**9)
random.seed(random.random())


class Maze:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.generate()

    def dfs_generate(self, x, y):
        self.used[y][x] = True
        neighbours = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        random.shuffle(neighbours)
        for nx, ny in neighbours:
            if nx < 0 or nx >= self.width or ny < 0 or ny >= self.height or self.used[ny][nx]:
                continue
            self.maze[y][x].append((nx, ny))
            self.maze[ny][nx].append((x, y))
            self.dfs_generate(nx, ny)

    def generate(self):
        self.maze = [[[] for x in range(self.width)] for y in range(self.height)]
        self.used = [[False for x in range(self.width)] for y in range(self.height)]
        self.dfs_generate(0, 0)
        for y in range(1, self.width + 1):
            for x in range(1, self.height + 1):
                continue

    def shortest_path_dfs(self, cur, finish, prev, path):
        if cur == finish:
            return path
        for next in self.maze[cur[1]][cur[0]]:
            if next == prev:
                continue
            path.append(next)
            res = self.shortest_path_dfs(next, finish, cur, path)
            if res:
                return res
            path.pop(-1)
        return None

    def shortest_path(self, start, finish):
        return self.shortest_path_dfs(start, finish, start, [start])
