import json

class Config():
    def __init__(self, flashcard, color, translation, keybinds):
        self.config = {
            "flashcard": flashcard,
            "color": color,
            "translation": translation,
            "keybinds": keybinds
        }
        self.config_file_name = "flashcards_config.json"
    def load(self):
        try:
            with open(self.config_file_name, "r", encoding="utf-8") as file:
                loaded = json.load(file)
        except Exception as e:
            print(e)
            return self.config

        return loaded
    def save(self):
        try:
            with open(self.config_file_name, "w", encoding="utf-8") as file:
                json.dump(self.config, file, indent=4)
        except Exception as e:
            print(e)
            return
