import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import webbrowser

from flashcards import Flashcard
from colors import Colors
from translations import Translations
from config import Config

class Main():
    def __init__(self):
        version = "1.3.0"

        self.rezolution = "500x300"
        self.title = "flashcards " + version

        self.flipped = False
        self.current_index = 0
        self.content = {}
        self.loaded_translation = {}
        self.config = None

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
            if self.config["flashcard"]:
                flashcard = Flashcard(self.config["flashcard"])
                flashcard.swap()

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

        tk.Button(options_frame, text=self.loaded_translation["options"][0], command=self.flip_logic).grid(row=0, column=0)
        tk.Button(options_frame, text=self.loaded_translation["options"][1], command=next).grid(row=0, column=1, padx=5)
        tk.Button(options_frame, text=self.loaded_translation["options"][2], command=previous).grid(row=0, column=2)

        menu_bar = tk.Menu(self.root)
        flashcard_menu = tk.Menu(menu_bar, tearoff=0)
        flashcard_menu.add_command(label=self.loaded_translation["flashcards"][1], command=self.load_flashcards)
        flashcard_menu.add_command(label=self.loaded_translation["flashcards"][2], command=invert)

        program_menu = tk.Menu(menu_bar, tearoff=0)
        program_menu.add_command(label=self.loaded_translation["program"][1], command=self.change_colors)
        program_menu.add_command(label=self.loaded_translation["program"][2], command=self.translate)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label=self.loaded_translation["help"][1], command=github)
        help_menu.add_command(label=self.loaded_translation["help"][2], command=release_notes)
        help_menu.add_command(label=self.loaded_translation["help"][3], command=issues)

        menu_bar.add_cascade(label=self.loaded_translation["flashcards"][0], menu=flashcard_menu)
        menu_bar.add_cascade(label=self.loaded_translation["program"][0], menu=program_menu)
        menu_bar.add_cascade(label=self.loaded_translation["help"][0], menu=help_menu)
        self.root.config(menu=menu_bar)
    def start(self):
        self.root = tk.Tk()
        self.root.title(self.title)
        self.root.geometry(self.rezolution)
        self.root.resizable(0, 0)

        self.current_front = tk.StringVar()
        self.current_back = tk.StringVar()

        config = Config(None, None, None, ["<Right>", "<Left>", "<Up>"])
        self.config = config.load()
        translations = Translations(self.config["translation"])
        self.loaded_translation = translations.load()

        self.current_front.set(self.loaded_translation["disclaimer"])
        self.current_back.set(self.loaded_translation["disclaimer"])

        self.layout()
        self.change_colors(True)
        self.load_flashcards(True)

        self.root.bind(self.config["keybinds"][0], lambda event: self.move_logic("next"))
        self.root.bind(self.config["keybinds"][1], lambda event: self.move_logic("previous"))
        self.root.bind(self.config["keybinds"][2], lambda event: self.flip_logic())

        self.root.protocol("WM_DELETE_WINDOW", self.closing)
        self.root.mainloop()
    def load_flashcards(self, initial=False):
        if not initial:
            try:
                self.config["flashcard"] = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
            except Exception:
                return
        else:
            if not self.config or not self.config["flashcard"]:
                return

        flashcard = Flashcard(self.config["flashcard"])

        self.content = flashcard.load()
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
    def change_colors(self, initial=False):
        if not initial:
            try:
                self.config["color"] = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
            except Exception:
                return
        else:
            if not self.config or not self.config["color"]:
                return

        colors = Colors(self.config["color"])

        loaded_colors = colors.load()

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
    def translate(self, initial=False):
        if not initial:
            try:
                self.config["translation"] = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
            except Exception:
                return

        translations = Translations(self.config["translation"])
        self.loaded_translation = translations.load()

        if not initial:
            messagebox.showinfo("translations", "restart app to see changes")
    def closing(self):
        config = Config(self.config["flashcard"], self.config["color"], self.config["translation"], self.config["keybinds"])
        config.save()
        self.root.destroy()

if __name__ == "__main__":
    app = Main()
    app.start()
