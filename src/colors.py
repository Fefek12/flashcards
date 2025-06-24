import json

class Colors():
    def __init__(self, file_path):
        self. file_path = file_path
    def load(self):
        content = {}
        if self.file_path:
            try:
                with open(self.file_path, "r") as file:
                    content = json.load(file)
            except Exception:
                return
        else:
            return

        return content
