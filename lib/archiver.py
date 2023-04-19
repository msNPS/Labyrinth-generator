import struct


def import_maze(filename):
    with open(filename, "rb") as f:
        width = struct.unpack("<H", f.read(2))[0]
        height = struct.unpack("<H", f.read(2))[0]
        seed = struct.unpack("<d", f.read(8))[0]
    return width, height, seed


def export_maze(maze, filename):
    with open(filename + ".maze", "wb") as f:
        f.write(struct.pack("<H", maze.width))
        f.write(struct.pack("<H", maze.height))
        f.write(struct.pack("<d", maze.seed))
