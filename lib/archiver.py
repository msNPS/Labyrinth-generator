import struct  # Imports
import cv2
import config


def import_maze(filename):  # Imports maze from file
    algorithm_dict = {0: "DFS", 1: "BFS", 2: "Kraskal"}  # Converts algorithm number to string to take less memory
    with open(filename, "rb") as f:
        width = struct.unpack("<H", f.read(2))[0]
        height = struct.unpack("<H", f.read(2))[0]
        algorithm = struct.unpack("<B", f.read(1))[0]
        seed = struct.unpack("<d", f.read(8))[0]
    return width, height, algorithm_dict[algorithm], seed


def export_maze(maze, filename):  # Exports maze to file
    if filename.endswith(".maze"):  # Checks if file is a .maze file
        algorithm_dict = {"DFS": 0, "BFS": 1, "Kraskal": 2}  # Converts algorithm string to number to take less memory
        with open(filename, "wb") as f:
            f.write(struct.pack("<H", maze.width))
            f.write(struct.pack("<H", maze.height))
            f.write(struct.pack("<B", algorithm_dict[maze.algorithm]))
            f.write(struct.pack("<d", maze.seed))
    elif filename.endswith(".png"):  # Checks if file is a .png file
        cv2.imwrite(filename, maze.resize(maze.last_draw))
