import cv2
import numpy


def draw_maze(maze):
    img = numpy.zeros((maze.height * 6 + 1, maze.width * 6 + 1, 3), numpy.uint8)
    for y, row in enumerate(maze.maze):
        for x, cell in enumerate(row):
            if not (x, y - 1) in cell:
                cv2.line(img, (x * 6, y * 6), (x * 6 + 6, y * 6), (255, 255, 255), 1)
            if not (x - 1, y) in cell:
                cv2.line(img, (x * 6, y * 6), (x * 6, y * 6 + 6), (255, 255, 255), 1)
    for y in range(maze.height):
        cv2.line(img, (maze.width * 6, y * 6), (maze.width * 6, y * 6 + 6), (255, 255, 255), 1)
    for x in range(maze.width):
        cv2.line(img, (x * 6, maze.height * 6), (x * 6 + 6, maze.height * 6), (255, 255, 255), 1)
    img[maze.height * 6][maze.width * 6] = (255, 255, 255)

    # path = maze.shortest_path((0, 0), (maze.width - 1, maze.height - 1))
    # for i in range(len(path) - 1):
    #     cv2.line(img, (path[i][0] * 6 + 3, path[i][1] * 6 + 3), (path[i + 1][0] * 6 + 3, path[i + 1][1] * 6 + 3), (0, 255, 0), 2)

    img = cv2.resize(img, (800, 800), interpolation=cv2.INTER_AREA)
    return img


def show(img):
    cv2.imshow("image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
