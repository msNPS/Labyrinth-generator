import cv2
import numpy
from maze_generator import Maze


def draw_maze(height, width):
    maze = Maze(height, width)
    img = numpy.zeros((height * 6 + 1, width * 6 + 1, 3), numpy.uint8)
    for y, row in enumerate(maze.maze):
        for x, cell in enumerate(row):
            if not (x, y - 1) in cell:
                cv2.line(img, (x * 6, y * 6), (x * 6 + 6, y * 6), (255, 255, 255), 1)
            if not (x - 1, y) in cell:
                cv2.line(img, (x * 6, y * 6), (x * 6, y * 6 + 6), (255, 255, 255), 1)
    for y in range(height):
        cv2.line(img, (width * 6, y * 6), (width * 6, y * 6 + 6), (255, 255, 255), 1)
    for x in range(width):
        cv2.line(img, (x * 6, height * 6), (x * 6 + 6, height * 6), (255, 255, 255), 1)
    img[height * 6][width * 6] = (255, 255, 255)

    path = maze.shortest_path((0, 0), (width - 1, height - 1))
    for i in range(len(path) - 1):
        cv2.line(img, (path[i][0] * 6 + 3, path[i][1] * 6 + 3), (path[i + 1][0] * 6 + 3, path[i + 1][1] * 6 + 3), (0, 255, 0), 2)

    img = cv2.resize(img, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_AREA)

    cv2.imwrite("data\maze.png", img)


def show(img):
    cv2.imshow("image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
