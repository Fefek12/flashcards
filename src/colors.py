import json

def colors(file_path):
    if file_path:
        try:
            with open(file_path, "r") as file:
                content = json.load(file)
        except Exception:
            return

    return content