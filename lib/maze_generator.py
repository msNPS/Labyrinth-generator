import random
import sys
import time
import cv2
import numpy

sys.setrecursionlimit(10**9)


class Maze:
    def __init__(self, height, width, seed=None):
        self.height = height
        self.width = width
        if seed:
            self.seed = seed
        else:
            self.seed = time.time()
        random.seed(self.seed)
        self.maze = [[[] for x in range(self.width)] for y in range(self.height)]
        self.used = [[False for x in range(self.width)] for y in range(self.height)]
        self.dfs_generate(0, 0)
        self.draw_base()

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

    def draw_maze(self):
        return self.resize(self.img)

    def draw_path(self, start, finish):
        self.path_img = self.img
        path = self.shortest_path(start, finish)
        for i in range(len(path) - 1):
            cv2.line(
                self.img,
                (path[i][0] * 6 + 3, path[i][1] * 6 + 3),
                (path[i + 1][0] * 6 + 3, path[i + 1][1] * 6 + 3),
                (0, 255, 0),
                1,
            )
        return self.resize(self.path_img)

    def invert_maze(self):
        self.inverted_img = self.img
        self.inverted_img = cv2.bitwise_not(self.inverted_img)
        return self.resize(self.inverted_img)

    def show_maze(self, img):
        cv2.imshow("image", self.img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
