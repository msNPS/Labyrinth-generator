import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
import os
from PIL import Image
from .archiver import export_maze, import_maze
from .maze_generator import Maze


BUTTON_COLOR = ("#68b885", "#31604e")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Change accent color in customtkinter.py

        self.width = 10
        self.height = 10

        self.title("Maze generator")
        self.iconbitmap("static/icon.ico")
        self.geometry("1000x600")

        # Set grid layout 1x2
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Generate Frame
        self.generate_frame = ctk.CTkFrame(
            self,
            corner_radius=10,
        )
        self.generate_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nwe")
        self.generate_frame.grid_rowconfigure(7, weight=1)

        self.generate_button = ctk.CTkButton(
            self.generate_frame,
            corner_radius=8,
            height=40,
            border_spacing=10,
            text="🎲 Generate Maze",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="center",
            command=self.generate_new_maze,
            fg_color=BUTTON_COLOR,
        )
        self.generate_button.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=16,
            pady=16,
        )

        self.width_label = ctk.CTkLabel(self.generate_frame, text=f"Width: ", width=200, corner_radius=0, anchor="w")
        self.width_label.grid(row=1, column=0, padx=20, sticky="w")

        self.width_entry = ctk.CTkEntry(
            master=self.generate_frame, placeholder_text=f"{self.width}", width=120, height=25, border_width=2, corner_radius=10
        )
        self.width_entry.grid(row=1, column=0, sticky="e", padx=10, pady=10)

        self.height_label = ctk.CTkLabel(self.generate_frame, text=f"Height: ", width=200, corner_radius=0, anchor="w")
        self.height_label.grid(row=2, column=0, padx=20, sticky="w")

        self.height_entry = ctk.CTkEntry(
            master=self.generate_frame, placeholder_text=f"{self.width}", width=120, height=25, border_width=2, corner_radius=10
        )
        self.height_entry.grid(row=2, column=0, sticky="e", padx=10, pady=10)

        # Import/Export File Frame
        self.file_frame = ctk.CTkFrame(
            self,
            corner_radius=10,
        )
        self.file_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nwe")
        self.file_frame.grid_columnconfigure(0, weight=1)
        self.file_frame.grid_rowconfigure(3, weight=1)

        self.import_label = ctk.CTkLabel(self.file_frame, text=f"No imported maze", width=200, corner_radius=0, anchor="center")
        self.import_label.grid(row=0, column=0, padx=16, pady=10, sticky="swe")

        self.import_button = ctk.CTkButton(
            self.file_frame,
            corner_radius=8,
            height=40,
            border_spacing=10,
            text="Import Maze",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="center",
            command=self.import_button_event,
            fg_color=BUTTON_COLOR,
        )
        self.import_button.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=16,
            pady=10,
        )

        self.export_button = ctk.CTkButton(
            self.file_frame,
            corner_radius=8,
            height=40,
            border_spacing=10,
            text="Export Maze",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            anchor="center",
            command=self.export_button_event,
            fg_color=BUTTON_COLOR,
        )
        self.export_button.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=16,
            pady=10,
        )

        # Apperance Frame
        self.appearance_frame = ctk.CTkFrame(
            self,
            corner_radius=10,
        )
        self.appearance_frame.grid(row=2, column=0, padx=20, pady=20, sticky="swe")
        self.appearance_frame.grid_columnconfigure(0, weight=1)
        self.appearance_frame.grid_rowconfigure(0, weight=1)
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(
            self.appearance_frame,
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event,
            fg_color=BUTTON_COLOR,
        )
        self.appearance_mode_optionemenu.set("System")
        self.appearance_mode_optionemenu.grid(row=0, column=0, padx=20, pady=(10, 10))

        # Maze Frame
        self.maze_frame = ctk.CTkFrame(self, corner_radius=10, width=500, height=500)
        self.maze_frame.grid(row=0, column=1, rowspan=3, sticky="nsew", padx=20, pady=20)
        self.maze_frame.grid_rowconfigure(0, weight=1)
        self.maze_frame.grid_columnconfigure(0, weight=1)

        self.maze_label = ctk.CTkLabel(self.maze_frame, fg_color="transparent", text="", width=500, height=500, anchor="center")
        self.maze_label.grid(row=0, column=0, columnspan=3, sticky="nsew")

        self.generate_new_maze()

    def draw_maze(self, width, height, seed=None):
        self.maze = Maze(width, height, seed)
        if width > height:
            size_x, size_y = 500, 500 // width * height
        else:
            size_x, size_y = 500 // height * width, 500
        self.maze_image = ctk.CTkImage(Image.fromarray(self.maze.draw_path((2, 2), (9, 7))), size=(size_y, size_x))
        self.maze_label.configure(image=self.maze_image, text="")

    def generate_new_maze(self):
        try:
            if self.width_entry.get() != "":
                self.width = int(self.width_entry.get())
            if self.height_entry.get() != "":
                self.height = int(self.height_entry.get())
        except:
            self.maze_label.configure(text="Width and height must be integers less than 100", image="")
            return
        if self.width >= 100 or self.height >= 100:
            self.maze_label.configure(text="Width and height must be integers less than 100", image="")
            return
        self.import_label.configure(text="No imported maze")
        self.draw_maze(self.width, self.height)

    def import_button_event(self):
        filename = filedialog.askopenfilename(
            initialdir=os.getcwd(), title="Select maze file", filetypes=(("Maze file", "*.maze"),)
        )
        if filename == "":
            return
        self.import_label.configure(text=f"Imported maze: {filename.split('/')[-1]}")
        width, height, seed = import_maze(filename)
        self.width_entry.insert(0, str(width))
        self.height_entry.insert(0, str(height))
        self.draw_maze(width, height, seed)

    def export_button_event(self):
        filename = filedialog.asksaveasfilename(
            initialdir=os.getcwd(), title="Select maze file", filetypes=(("Maze file", "*.maze"),)
        )
        if filename == "":
            return
        export_maze(self.maze, filename)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
        self.draw_maze(self.width, self.height)


if __name__ == "__main__":
    app = App()
    app.mainloop()
