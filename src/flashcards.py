import json

class Flashcard():
    def __init__(self, file_path):
        self.file_path = file_path
    def swap(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                content = file.read().strip()
                if not content.startswith('{'):
                    content = '{' + content
                if not content.endswith('}'):
                    content = content.rstrip(',\n') + '}'
                data = json.loads(content)
        except Exception:
            return

        for key, value in data.items():
            value['front'], value['back'] = value['back'], value['front']

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    def load(self):
        content = {}
        if self.file_path:
            try:
                with open(self.file_path, "r", encoding="utf-8") as file:
                    content = json.load(file)
            except Exception:
                return
        else:
            return

        return content
