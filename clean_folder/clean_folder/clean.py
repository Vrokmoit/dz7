import sys
from pathlib import Path
import os
import re
CATEGORIES = {
    "audio": [".mp3", ".ogg", ".wav", ".amr"],
    "documents": [".txt", ".docx", ".pdf", ".doc", ".xlsx", ".pptx"],
    "images": [".jpeg", ".png", ".jpg", ".svg"],
    "video": [".avi", "mp4", "mov", ".mkv"],
    "archives": [".zip", ".gz", ".tar"]
}
def normalize(filename):

    name, extension = os.path.splitext(filename)


    translit_map = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e',
        'є': 'ie', 'ж': 'zh', 'з': 'z', 'и': 'i', 'і': 'i', 'ї': 'yi',
        'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o',
        'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f',
        'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
        'ь': '', 'ю': 'yu', 'я': 'ya',
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E',
        'Є': 'IE', 'Ж': 'ZH', 'З': 'Z', 'И': 'I', 'І': 'I', 'Ї': 'YI',
        'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O',
        'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F',
        'Х': 'KH', 'Ц': 'TS', 'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SHCH',
        'Ь': '', 'Ю': 'YU', 'Я': 'YA'
    }


    transliterated_name = ''.join(translit_map.get(char, char) for char in name)


    normalized_name = re.sub(r'[\/:*?"<>|]', '_', transliterated_name)

    normalized_filename = normalized_name + extension

    return normalized_filename
def get_categories(file: Path) -> str:
    ext = file.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Other"
def move_file(file: Path, category: str, root_dir: Path) -> None:
    normalized_name = normalize(file.name) 
    target_dir = root_dir / category
    if not target_dir.exists():
        target_dir.mkdir(parents=True, exist_ok=True)
    file_copy = target_dir / normalized_name
    file_copy.write_bytes(file.read_bytes())
    file.unlink()


def sort_folder(path) -> dict:
    categories = {category: [] for category in CATEGORIES.keys()}
    unknown_extensions = set()
    for element in path.glob("**/*"):
        if element.is_file():
            category = get_categories(element)
            if category in categories:  # Проверяем, существует ли категория
                categories[category].append(element.name)
            else:
                unknown_extensions.add(element.suffix.lower())
            move_file(element, category, path)
    return categories, unknown_extensions



def remove_empty_folders_recursive(path):
    for folder in list(path.rglob('*'))[::-1]:
        if folder.is_dir():
            try:
                folder.rmdir()
            except OSError:
                pass

def remove_empty_folders(path):
    for folder in path.rglob('*'):
        if folder.is_dir():
            try:
                folder.rmdir()
            except OSError:
                pass
    remove_empty_folders_recursive(path)

def main():
    try:
        path = Path(sys.argv[1])
    except IndexError:
        print("No path to folder")
        return
    if not path.exists():
        print("Folder does not exist")
        return
    categories, unknown_extensions = sort_folder(path)
    
    print("Список файлів в кожній категорії:")
    for category, files in categories.items():
        print(f"{category}: {', '.join(files)}")

    print("\nПерелік усіх відомих скрипту розширень:")
    known_extensions = set(ext for exts in CATEGORIES.values() for ext in exts)
    print(", ".join(known_extensions))

    print("\nПерелік всіх розширень, які скрипту невідомі:")
    print(", ".join(unknown_extensions))

    remove_empty_folders(path)
    print("All ok")

if __name__ == '__main__':
    main()
