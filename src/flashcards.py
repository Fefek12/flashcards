import json

input_file = None

def swap(input_filename):
    with open(input_filename, 'r', encoding='utf-8') as f:
        content = f.read().strip()
        if not content.startswith('{'):
            content = '{' + content
        if not content.endswith('}'):
            content = content.rstrip(',\n') + '}'
        data = json.loads(content)

    for key, value in data.items():
        value['front'], value['back'] = value['back'], value['front']

    with open(input_filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def flashcards(file_path):
    global input_file
    input_file = file_path
    if file_path:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = json.load(file)
        except Exception:
            return
        
    return content