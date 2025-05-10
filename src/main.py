import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

from flashcards import flashcards
from colors import colors

class Main():
    def __init__(self):
        self.rezolution = "500x300"
        self.title = "Flashcards by Fefek"

        self.flipped = False

        self.front_color = "yellow"
        self.back_color = "lightblue"
        self.front_font_color = "black"
        self.back_font_color = "black"
    def layout(self):
        self.flashcard_frame = tk.Frame(self.root, width=300, height=200, bg=self.front_color, borderwidth=1, relief="solid")
        self.flashcard_frame.pack(pady=10)
        self.flashcard_frame.pack_propagate(False)

        self.front_label = tk.Label(self.flashcard_frame, textvariable=self.current_front, fg=self.front_font_color, justify="center", bg=self.front_color)
        self.front_label.pack(pady=75)

        self.back_label = tk.Label(self.flashcard_frame, textvariable=self.current_back, fg=self.back_font_color, justify="center", bg=self.back_color)

        options_frame = tk.Frame(self.root)
        options_frame.pack(pady=10)

        tk.Button(options_frame, text="Flip", command=self.flip_logic).grid(row=0, column=0)
        tk.Button(options_frame, text="Next", command=self.next_logic).grid(row=0, column=1, padx=5)

        menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Load", command=self.load_flashcards)

        program_menu = tk.Menu(menu_bar, tearoff=0)
        program_menu.add_command(label="Colors", command=self.change_colors)

        menu_bar.add_cascade(label="File", menu=file_menu)
        menu_bar.add_cascade(label="Program", menu=program_menu)
        self.root.config(menu=menu_bar)
    def start(self):
        self.root = tk.Tk()
        self.root.title(self.title)
        self.root.geometry(self.rezolution)
        self.root.resizable(0, 0)

        self.current_front = tk.StringVar()
        self.current_back = tk.StringVar()
        self.current_index = 0
        self.content = {}

        self.current_front.set("Load a file first")
        self.current_back.set("Load a file first")

        self.layout()
        self.root.mainloop()
    def load_flashcards(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not file_path:
             return

        self.content = flashcards(file_path)
        self.current_index = 0
        self.current_front.set(self.content["0"]["front"])
        self.current_back.set(self.content["0"]["back"])
    def flip_logic(self):
        if self.flipped:
            self.flashcard_frame.config(bg=self.front_color)
            self.back_label.pack_forget()
            self.front_label.pack(pady=75)
        else:
            self.flashcard_frame.config(bg=self.back_color)
            self.front_label.pack_forget()
            self.back_label.pack(pady=75)
        self.flipped = not self.flipped
    def next_logic(self):
        keys = list(self.content.keys())

        if self.current_index + 1 < len(keys):
            self.current_index += 1
        else:
            self.current_index = 0

        card = self.content[str(self.current_index)]
        self.current_back.set(card["back"])
        self.front_label.pack(pady=75)
        self.current_front.set(card["front"])
        self.back_label.pack_forget()
        self.flashcard_frame.config(bg=self.front_color)
        self.flipped = False
    def change_colors(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])

        loaded_colors = colors(file_path)

        self.front_color = loaded_colors["front"]
        self.back_color = loaded_colors["back"]
        self.front_font_color = loaded_colors["font-front"]
        self.back_font_color = loaded_colors["font-back"]

        if self.flipped:
            self.flashcard_frame.config(bg=self.back_color)
        else:
            self.flashcard_frame.config(bg=self.front_color)
        
        self.front_label.config(bg=self.front_color, fg=self.front_font_color)
        self.back_label.config(bg=self.back_color, fg=self.back_font_color)

if __name__ == "__main__":
    app = Main()
    app.start()