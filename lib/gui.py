import customtkinter as ctk  # Imports
import tkinter as tk
from tkinter import filedialog
import os
from PIL import Image
from .archiver import export_maze, import_maze
from .maze_generator import Maze
from config import *


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.width = 10  # Default values
        self.height = 10
        self.algorithm = "DFS"
        self.seed = None

        self.title("Maze generator")  # Window initialisation
        self.iconbitmap("static/icon.ico")
        self.geometry(WINDOW_SIZE)

        self.grid_rowconfigure(3, weight=1)  # Set grid layout 1x2
        self.grid_columnconfigure(1, weight=1)

        # Generation Frame
        self.generate_frame = ctk.CTkFrame(
            self,
            corner_radius=10,
        )
        self.generate_frame.grid(row=0, column=0, padx=16, pady=16, sticky="nwe")
        self.generate_frame.grid_rowconfigure(4, weight=1)
        self.generate_frame.grid_columnconfigure(0, weight=1)

        self.generate_button = ctk.CTkButton(
            self.generate_frame,
            corner_radius=8,
            height=50,
            border_spacing=10,
            text="🎲 Generate Maze",
            text_color=TEXT_COLOR,
            hover_color=HOVER_COLOR,
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

        self.algorithm_label = ctk.CTkLabel(
            self.generate_frame, text=f"Generation alorithm:", width=200, corner_radius=0, anchor="center"
        )
        self.algorithm_label.grid(row=1, column=0, padx=16, sticky="nsew")
        self.algorithm_options = ctk.CTkOptionMenu(
            self.generate_frame,
            values=["DFS", "BFS", "Kraskal"],
            variable=ctk.StringVar(self, value="DFS"),
            width=150,
            height=30,
            corner_radius=10.0,
            command=self.algorithm_selection_event,
            fg_color=BUTTON_COLOR,
            text_color=TEXT_COLOR,
            button_color=OPTION_COLOR,
            button_hover_color=OPTION_HOVER_COLOR,
        )
        self.algorithm_options.grid(row=2, column=0, padx=16, pady=10, sticky="nsew")

        self.width_label = ctk.CTkLabel(self.generate_frame, text=f"Width: ", width=200, corner_radius=0, anchor="w")
        self.width_label.grid(row=3, column=0, padx=16)

        self.width_entry = ctk.CTkEntry(
            master=self.generate_frame, placeholder_text=f"{self.width}", width=120, height=25, border_width=2, corner_radius=10
        )
        self.width_entry.grid(row=3, column=0, padx=16, pady=10, sticky="e")

        self.height_label = ctk.CTkLabel(self.generate_frame, text=f"Height: ", width=200, corner_radius=0, anchor="w")
        self.height_label.grid(row=4, column=0, padx=16)

        self.height_entry = ctk.CTkEntry(
            master=self.generate_frame, placeholder_text=f"{self.width}", width=120, height=25, border_width=2, corner_radius=10
        )
        self.height_entry.grid(row=4, column=0, padx=16, pady=10, sticky="e")

        # Path Finding Frame
        self.path_frame = ctk.CTkFrame(
            self,
            corner_radius=10,
        )
        self.path_frame.grid(row=2, column=0, padx=16, pady=10, sticky="nwe")
        self.path_frame.grid_columnconfigure(5, weight=1)
        self.path_frame.grid_rowconfigure(3, weight=1)

        self.path_label = ctk.CTkLabel(self.path_frame, text=f"Maze Path", width=200, corner_radius=0, anchor="center")
        self.path_label.grid(row=0, column=0, columnspan=6, padx=16, pady=10)

        self.path_show_button = ctk.CTkButton(
            self.path_frame,
            corner_radius=8,
            height=30,
            width=100,
            border_spacing=10,
            text="🔎Show",
            text_color=TEXT_COLOR,
            hover_color=HOVER_COLOR,
            anchor="center",
            command=self.show_path,
            fg_color=BUTTON_COLOR,
        )
        self.path_show_button.grid(row=1, column=0, sticky="nesw", padx=16, columnspan=3)
        self.path_show_button = ctk.CTkButton(
            self.path_frame,
            corner_radius=8,
            height=30,
            width=100,
            border_spacing=10,
            text="🗑️Clear",
            text_color=TEXT_COLOR,
            hover_color=HOVER_COLOR,
            anchor="center",
            command=self.draw_maze,
            fg_color=BUTTON_COLOR,
        )
        self.path_show_button.grid(row=1, column=3, sticky="nesw", padx=16, columnspan=3)

        # Start point
        self.path_start_label = ctk.CTkLabel(self.path_frame, text=f"Start: ", width=20, corner_radius=0, anchor="w")
        self.path_start_label.grid(row=2, column=0, padx=16, pady=10, sticky="w")
        self.path_start_x_label = ctk.CTkLabel(self.path_frame, text=f"(", width=5, corner_radius=0, anchor="w")
        self.path_start_x_label.grid(row=2, column=1, padx=2, pady=10, sticky="w")
        self.path_start_x_entry = ctk.CTkEntry(
            master=self.path_frame, placeholder_text=f"0", width=40, height=25, border_width=2, corner_radius=10
        )
        self.path_start_x_entry.grid(row=2, column=2, padx=2, pady=10, sticky="w")
        self.path_start_y_label = ctk.CTkLabel(self.path_frame, text=f";", width=5, corner_radius=0, anchor="w")
        self.path_start_y_label.grid(row=2, column=3, padx=2, pady=10, sticky="w")
        self.path_start_y_entry = ctk.CTkEntry(
            master=self.path_frame, placeholder_text=f"0", width=40, height=25, border_width=2, corner_radius=10
        )
        self.path_start_y_entry.grid(row=2, column=4, padx=2, pady=10, sticky="w")
        self.path_start_y_label = ctk.CTkLabel(self.path_frame, text=f")", width=5, corner_radius=0, anchor="w")
        self.path_start_y_label.grid(row=2, column=5, padx=2, pady=10, sticky="w")

        # End point
        self.path_end_label = ctk.CTkLabel(self.path_frame, text=f"End: ", width=20, corner_radius=0, anchor="w")
        self.path_end_label.grid(row=3, column=0, padx=16, pady=10, sticky="nsew")
        self.path_end_x_label = ctk.CTkLabel(self.path_frame, text=f"(", width=5, corner_radius=0, anchor="w")
        self.path_end_x_label.grid(row=3, column=1, padx=2, pady=10, sticky="w")
        self.path_end_x_entry = ctk.CTkEntry(
            master=self.path_frame, placeholder_text=f"0", width=40, height=25, border_width=2, corner_radius=10
        )
        self.path_end_x_entry.grid(row=3, column=2, padx=2, pady=10, sticky="w")
        self.path_end_y_label = ctk.CTkLabel(self.path_frame, text=f";", width=5, corner_radius=0, anchor="w")
        self.path_end_y_label.grid(row=3, column=3, padx=2, pady=10, sticky="w")
        self.path_end_y_entry = ctk.CTkEntry(
            master=self.path_frame, placeholder_text=f"0", width=40, height=25, border_width=2, corner_radius=10
        )
        self.path_end_y_entry.grid(row=3, column=4, padx=2, pady=10, sticky="w")
        self.path_end_y_label = ctk.CTkLabel(self.path_frame, text=f")", width=5, corner_radius=0, anchor="w")
        self.path_end_y_label.grid(row=3, column=5, padx=2, pady=10, sticky="w")

        # Import/Export File Frame
        self.file_frame = ctk.CTkFrame(
            self,
            corner_radius=10,
        )
        self.file_frame.grid(row=1, column=0, padx=16, pady=16, sticky="nwe")
        self.file_frame.grid_columnconfigure(0, weight=1)
        self.file_frame.grid_rowconfigure(3, weight=1)

        self.import_label = ctk.CTkLabel(self.file_frame, text=f"No imported maze", width=200, corner_radius=0, anchor="center")
        self.import_label.grid(row=0, column=0, padx=16, pady=10)

        self.import_button = ctk.CTkButton(
            self.file_frame,
            corner_radius=8,
            height=25,
            border_spacing=10,
            text="Import Maze",
            text_color=TEXT_COLOR,
            hover_color=HOVER_COLOR,
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
            height=25,
            border_spacing=10,
            text="Export Maze",
            text_color=TEXT_COLOR,
            hover_color=HOVER_COLOR,
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
        self.appearance_frame.grid(row=3, column=0, padx=16, pady=16, sticky="swe")
        self.appearance_frame.grid_columnconfigure(0, weight=1)
        self.appearance_frame.grid_rowconfigure(0, weight=1)
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(
            self.appearance_frame,
            values=["Light", "Dark"],
            command=self.change_appearance_mode_event,
            fg_color=BUTTON_COLOR,
            text_color=TEXT_COLOR,
            button_color=OPTION_COLOR,
            button_hover_color=OPTION_HOVER_COLOR,
        )
        self.appearance_mode_optionemenu.set("Dark")
        self.appearance_mode_optionemenu.grid(row=0, column=0, padx=16, pady=(10, 10))

        # Maze Frame
        self.maze_frame = ctk.CTkFrame(self, corner_radius=10)
        self.maze_frame.grid(row=0, column=1, rowspan=4, sticky="nsew", padx=16, pady=16)
        self.maze_frame.grid_rowconfigure(0, weight=1)
        self.maze_frame.grid_columnconfigure(0, weight=1)

        self.maze_label = ctk.CTkLabel(
            self.maze_frame, fg_color="transparent", text="", width=500, height=500, corner_radius=10, anchor="center"
        )
        self.maze_label.grid(row=0, column=0, padx=16, pady=20, sticky="nsew")

        self.generate_new_maze()

    def draw_maze(self):  # Put the self.maze on the tkinter window
        if self.width > self.height:
            size_x, size_y = 500, 500 // self.width * self.height
        else:
            size_x, size_y = 500 // self.height * self.width, 500
        self.maze_image = ctk.CTkImage(
            Image.fromarray(self.maze.draw_maze(self.appearance_mode_optionemenu.get())), size=(size_x, size_y)
        )
        self.maze_label.configure(image=self.maze_image, text="", corner_radius=10)

        self.path_start_x_entry.delete(0, "end")
        self.path_start_x_entry.insert(0, "0")
        self.path_start_y_entry.delete(0, "end")
        self.path_start_y_entry.insert(0, "0")
        self.path_end_x_entry.delete(0, "end")
        self.path_end_x_entry.insert(0, str(self.width - 1))
        self.path_end_y_entry.delete(0, "end")
        self.path_end_y_entry.insert(0, str(self.height - 1))
        self.path_label.configure(text="Maze Path")

    def draw_path(self):  # Put the maze with the path on the tkinter window
        if self.width > self.height:
            size_x, size_y = 500, 500 // self.width * self.height
        else:
            size_x, size_y = 500 // self.height * self.width, 500

        start = [0, 0]
        try:
            start[0] = int(self.path_start_x_entry.get())
        except:
            pass
        try:
            start[1] = int(self.path_start_y_entry.get())
        except:
            pass

        end = [self.width - 1, self.height - 1]
        try:
            end[0] = int(self.path_end_x_entry.get())
        except:
            pass
        try:
            end[1] = int(self.path_end_y_entry.get())
        except:
            pass

        path_img, path_len = self.maze.draw_path(tuple(start), tuple(end), self.appearance_mode_optionemenu.get())
        self.maze_image = ctk.CTkImage(Image.fromarray(path_img), size=(size_x, size_y))
        self.maze_label.configure(image=self.maze_image, text="", corner_radius=10)
        self.path_label.configure(text=f"Path length: {path_len}")

    def generate_new_maze(self):  # Generate a new maze with new seed
        try:
            if self.width_entry.get() != "":
                self.width = int(self.width_entry.get())
            if self.height_entry.get() != "":
                self.height = int(self.height_entry.get())
        except:
            tk.messagebox.showerror(title="Incorrect dimennsions", message="Width and height must be integers not more than 100")
            return
        if self.width > 100 or self.height > 100:
            tk.messagebox.showerror(title="Incorrect dimennsions", message="Width and height must be integers not more than 100")
            return

        self.import_label.configure(text="No imported maze")
        self.maze = Maze(self.width, self.height, algorithm=self.algorithm)
        self.draw_maze()

    def algorithm_selection_event(self, value):  # Change the generation algorithm
        self.algorithm = value
        self.generate_new_maze()

    def show_path(self):  # Show the path on the maze
        self.draw_path()

    def import_button_event(self):  # Import a maze from a file
        filename = filedialog.askopenfilename(
            initialdir=os.getcwd(), title="Select maze file", filetypes=(("Maze file", "*.maze"),)
        )
        if filename == "":
            return
        try:
            self.width, self.height, self.algorithm, self.seed = import_maze(filename)
        except:
            tk.messagebox.showerror(title="Import error", message="File unreadable")
            return
        self.import_label.configure(text=f"Imported maze: {filename.split('/')[-1]}")
        self.width_entry.delete(0, "end")
        self.width_entry.insert(0, str(self.width))
        self.height_entry.delete(0, "end")
        self.height_entry.insert(0, str(self.height))
        self.algorithm_options.set(self.algorithm)
        self.maze = Maze(self.width, self.height, algorithm=self.algorithm, seed=self.seed)
        self.draw_maze()

    def export_button_event(self):  # Export the maze to a .maze or .png file
        filetypes = (("Maze file", "*.maze"), ("Mage Picture", "*.png"))
        filename = filedialog.asksaveasfilename(
            initialdir=os.getcwd(), title="Select maze file", filetypes=filetypes, defaultextension=filetypes
        )
        if filename == "":
            return
        export_maze(self.maze, filename)

    def change_appearance_mode_event(self, new_appearance_mode: str):  # Change the appearance mode
        ctk.set_appearance_mode(new_appearance_mode)
        self.draw_maze()


if __name__ == "__main__":  # Run the app
    app = App()
    app.mainloop()
