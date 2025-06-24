import tkinter as tk
from tkinter import filedialog
import webbrowser

from flashcards import flashcards, swap
from colors import colors

class Main():
    def __init__(self):
        version = "1.2.0"

        self.rezolution = "500x300"
        self.title = "flashcards " + version

        self.flipped = False

        self.front_color = "yellow"
        self.back_color = "lightblue"
        self.front_font_color = "black"
        self.back_font_color = "black"

        self.github_url = "https://github.com/Fefek12/flashcards"
        self.releases_url = "https://github.com/Fefek12/flashcards/releases"
        self.issues_url = "https://github.com/Fefek12/flashcards/issues"
    def layout(self):
        def next():
            self.move_logic("next")
        def previous():
            self.move_logic("previous")
        def invert():
            swap(self.file_path)

        def github():
            self.help(self.github_url)
        def release_notes():
            self.help(self.releases_url)
        def issues():
            self.help(self.issues_url)

        self.flashcard_frame = tk.Frame(self.root, width=300, height=200, bg=self.front_color, borderwidth=1, relief="solid")
        self.flashcard_frame.pack(pady=10)
        self.flashcard_frame.pack_propagate(False)

        self.front_label = tk.Label(self.flashcard_frame, textvariable=self.current_front, fg=self.front_font_color, justify="center", bg=self.front_color)
        self.front_label.pack(pady=75)

        self.back_label = tk.Label(self.flashcard_frame, textvariable=self.current_back, fg=self.back_font_color, justify="center", bg=self.back_color)

        options_frame = tk.Frame(self.root)
        options_frame.pack(pady=10)

        tk.Button(options_frame, text="flip", command=self.flip_logic).grid(row=0, column=0)
        tk.Button(options_frame, text="next", command=next).grid(row=0, column=1, padx=5)
        tk.Button(options_frame, text="previous", command=previous).grid(row=0, column=2)

        menu_bar = tk.Menu(self.root)
        flashcard_menu = tk.Menu(menu_bar, tearoff=0)
        flashcard_menu.add_command(label="load", command=self.load_flashcards)
        flashcard_menu.add_command(label="invert", command=invert)

        program_menu = tk.Menu(menu_bar, tearoff=0)
        program_menu.add_command(label="colors", command=self.change_colors)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="github", command=github)
        help_menu.add_command(label="view releases", command=release_notes)
        help_menu.add_command(label="issues", command=issues)

        menu_bar.add_cascade(label="flashcard", menu=flashcard_menu)
        menu_bar.add_cascade(label="program", menu=program_menu)
        menu_bar.add_cascade(label="help", menu=help_menu)
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

        self.current_front.set("load a file first")
        self.current_back.set("load a file first")

        self.layout()
        self.root.mainloop()
    def load_flashcards(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if not self.file_path:
            return

        self.content = flashcards(self.file_path)
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
    def move_logic(self, direction):
        keys = list(self.content.keys())

        if self.current_index + 1 < len(keys) and direction == "next":
            self.current_index += 1
        elif self.current_index - 1 >= 0 and direction == "previous":
            self.current_index -= 1
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
    def help(self, url):
        webbrowser.open_new(url)

if __name__ == "__main__":
    app = Main()
    app.start()
