import json

class Translations():
    def __init__(self, file_path):
        self.file_path = file_path
        self.english = {
            "disclaimer": "load file first",
            "flashcards": ["flashcards", "load", "invert"],
            "program": ["program", "colors", "translations"],
            "help": ["help", "github", "new releases", "issues"],
            "options": ["flip", "next", "previous"]
        }
    def load(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                translations = json.load(file)
        except Exception:
            return self.english

        return translations
