import json

def flashcards(file_path):
    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = json.load(file)
        except Exception:
            return
        
    return content