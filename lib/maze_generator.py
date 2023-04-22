import random
import sys
import time
import cv2
import numpy
from config import *

sys.setrecursionlimit(10**9)


class Maze:
    def __init__(self, width, height, algorithm="DFS", seed=None):
        self.width = width
        self.height = height
        if seed:
            self.seed = seed
        else:
            self.seed = time.time()
        self.algorithm = algorithm
        random.seed(self.seed)
        self.maze = [[[] for x in range(self.width)] for y in range(self.height)]

        if algorithm == "DFS":
            self.generate_dfs()
        elif algorithm == "BFS":
            self.generate_bfs()
        elif algorithm == "Kraskal":
            self.generate_kruskal()
        self.draw_base()

    def generate_dfs(self):
        def dfs(x, y):
            self.used[y][x] = True
            neighbours = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            random.shuffle(neighbours)
            for nx, ny in neighbours:
                if nx < 0 or nx >= self.width or ny < 0 or ny >= self.height or self.used[ny][nx]:
                    continue
                self.maze[y][x].append((nx, ny))
                self.maze[ny][nx].append((x, y))
                dfs(nx, ny)

        self.used = [[False for x in range(self.width)] for y in range(self.height)]
        x = random.randint(0, self.width - 1)
        y = random.randint(0, self.height - 1)
        dfs(x, y)

    def generate_bfs(self):
        queue = [(random.randint(0, self.width - 1), random.randint(0, self.height - 1))]
        self.used = [[False for x in range(self.width)] for y in range(self.height)]
        while queue:
            x, y = queue.pop()
            self.used[y][x] = True
            neighbours = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            random.shuffle(neighbours)
            for nx, ny in neighbours:
                if nx < 0 or nx >= self.width or ny < 0 or ny >= self.height or not self.used[ny][nx]:
                    continue
                self.maze[y][x].append((nx, ny))
                self.maze[ny][nx].append((x, y))
                break

            for nx, ny in neighbours:
                if (
                    nx >= 0
                    and nx < self.width
                    and ny >= 0
                    and ny < self.height
                    and not self.used[ny][nx]
                    and not (nx, ny) in queue
                ):
                    queue.append((nx, ny))

    def generate_kruskal(self):
        cells = [[(x, y)] for x in range(self.width) for y in range(self.height)]
        for _ in range(self.width * (self.height + 1) + self.height * (self.width + 1)):
            random.shuffle(cells)
            group0 = cells[0]
            for group1 in cells[1:]:
                connected = False
                for (x, y) in group0:
                    if group0 == [(0, 0)] and group1 == [(1, 0)]:
                        pass
                    neighbours = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
                    random.shuffle(neighbours)
                    for (nx, ny) in neighbours:
                        if (nx, ny) in group1:
                            self.maze[y][x].append((nx, ny))
                            self.maze[ny][nx].append((x, y))
                            cells.remove(group0)
                            cells.remove(group1)
                            cells.append(group0 + group1)
                            connected = True
                            break
                    if connected:
                        break
                if connected:
                    break

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

    def resize(self, img):
        if self.width > self.height:
            size_x, size_y = 800, 800 // self.width * self.height
        else:
            size_x, size_y = 800 // self.height * self.width, 800
        return cv2.resize(img, (size_x, size_y), interpolation=cv2.INTER_AREA)

    def draw_base(self):
        self.img = numpy.zeros((self.height * 6 + 1, self.width * 6 + 1, 3), numpy.uint8)
        for y, row in enumerate(self.maze):
            for x, cell in enumerate(row):
                if not (x, y - 1) in cell:
                    cv2.line(self.img, (x * 6, y * 6), (x * 6 + 6, y * 6), (255, 255, 255), 1)
                if not (x - 1, y) in cell:
                    cv2.line(self.img, (x * 6, y * 6), (x * 6, y * 6 + 6), (255, 255, 255), 1)
        for y in range(self.height):
            cv2.line(self.img, (self.width * 6, y * 6), (self.width * 6, y * 6 + 6), (255, 255, 255), 1)
        for x in range(self.width):
            cv2.line(self.img, (x * 6, self.height * 6), (x * 6 + 6, self.height * 6), (255, 255, 255), 1)
        self.img[self.height * 6][self.width * 6] = (255, 255, 255)

    def draw_maze(self, theme="Dark"):
        if theme == "Dark":
            self.last_draw = self.img
        elif theme == "Light":
            self.last_draw = self.invert_maze(self.img)
        return self.resize(self.last_draw)

    def draw_path(self, start, finish, theme="Dark"):
        self.last_draw = "path"
        if theme == "Dark":
            path_color = (110, 197, 140)
        else:
            path_color = (206, 159, 177)

        self.path_img = self.img.copy()
        path = self.shortest_path(start, finish)
        for i in range(len(path) - 1):
            cv2.line(
                self.path_img,
                (path[i][0] * 6 + 3, path[i][1] * 6 + 3),
                (path[i + 1][0] * 6 + 3, path[i + 1][1] * 6 + 3),
                path_color,
                2,
            )

        if theme == "Dark":
            self.last_draw = self.path_img
        elif theme == "Light":
            self.last_draw = self.invert_maze(self.path_img)
        return self.resize(self.last_draw), len(path)

    def invert_maze(self, img):
        return cv2.bitwise_not(img)

    def show_maze(self, img):
        cv2.imshow("image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
