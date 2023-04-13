import customtkinter
import os
from PIL import Image
from vizualizer import draw_maze


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Maze generator.py")
        self.geometry("960x540")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        draw_maze(10, 10)

        self.control_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.control_frame.grid(row=0, column=1, sticky="nsew")
        self.control_frame.grid_rowconfigure(4, weight=1)

        self.maze_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.maze_frame.grid_columnconfigure(0, weight=1)
        self.maze_image = customtkinter.CTkImage(Image.open(os.path.join("data", "maze.png")), size=(26, 26))
        self.navigation_frame_label = customtkinter.CTkLabel(
            self.maze_frame,
            text="Image Example",
            image=self.maze_image,
            compound="left",
            font=customtkinter.CTkFont(size=15, weight="bold"),
        )


if __name__ == "__main__":
    app = App()
    app.mainloop()
