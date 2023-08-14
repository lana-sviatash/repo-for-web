import shutil
from pathlib import Path
from normalize import normalize

CATEGORIES = {"Audio": [".mp3", ".aiff", ".wav", ".ogg"],
              "Video": [".mkv", ".mov", ".mp4", ".avi"],
              "Document": [".docx", ".pptx", ".doc", ".txt", ".pdf", ".xlsx", ".pptx", ".rtf", ".xls", ".pub"],
              "Image": [".jpeg", ".png", ".svg", ".jpg", ".bmp", ".gif"],
              "Archive": [".zip", ".tar", ".7z", ".gz", ".rar"],
              "Python": [".py", ".json", ".pyc"],
              "Other": []}
dictionary_of_files = {}
dictionary_global = {}
dictionary_of_ext = {}
dictionary_ext = {}


def move_file(path: Path, root_dir: Path, categories: str):
    target_dir = root_dir.joinpath(categories)
    if not target_dir.exists():
        target_dir.mkdir()

    path.replace(target_dir.joinpath(f"{normalize(path.stem)}{path.suffix}"))


def unpack_archive(path: Path):
    archive_folder = "Archive"
    ext = [".zip", ".tar", ".7z", ".gz", ".rar"]

    for el in path.glob(f"**/*"):
        if not el.name.startswith('.'):
            if el.suffix in ext:
                filename = el.stem
                arch_dir = path.joinpath(path / archive_folder / filename)
                arch_dir.mkdir()
                try:
                    shutil.unpack_archive(el, arch_dir)
                except shutil.ReadError:
                    continue
            else:
                continue


def delete_empty_folder(path: Path):
    folders_to_delete = [f for f in path.glob("**")]
    for folder in folders_to_delete[::-1]:
        if not folder.name.startswith('.'):
            try:
                folder.rmdir()
            except OSError:
                continue


def get_categories(path: Path) -> str:
    ext = path.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Other"


def sort_folder(path: Path):
    for item in path.glob("**/*"):
        if not item.name.startswith('.'):
            if item.is_file():
                cat = get_categories(item)
                move_file(item, path, cat)


def files_sorter(path: Path):
    for item in path.glob("**/*"):
        if not item.name.startswith('.'):
            if item.is_file():
                # print(item)
                cat = get_categories(item)
                if dictionary_of_files.get(cat):
                    if item.name not in dictionary_of_files[cat]:
                        dictionary_of_files[cat].append(item.name)
                else:
                    dictionary_of_files[cat] = [item.name]
    dictionary_global.update(dictionary_of_files)
    print(' ________________________________________________________')
    print("| {:^54} |".format("▣ Files found in folders: ▣"))
    print('|________________________________________________________|')
    for el, values in dictionary_global.items():
        print('|________________________________________________________|')
        print("|▶ {:<30} | {:>20} |".format(el, len(values)))
        print('|________________________________________________________|')
    return dictionary_global == {}


def sorter_starter():
    print("|{:^32}|".format("▣ For exit type 'exit' or '0' ▣"))
    print("|" + "_" * 32 + "|")
    print("|{:^32}|".format("Input path to folder:"))
    print("|" + "_" * 32 + "|")

    while True:

        try:

            path = Path(input("|>>> "))
            if path.name.lower() in ("close", "exit", "good bye", "0"):
                return "\nGood bye!"
            elif path.exists():
                print("|" + "_" * 32 + "|" + "\n")
                print("_" * 58)
                print("|{:^50}|".format("✨✨✨ Sorting completed! ✨✨✨"))
                print("|" + "_" * 56 + "|")
            else:
                print("_" * 34)
                print("|{:<32}|".format("Folder with this path not exist"))
                print("|{:<32}|".format("Try again..."))
                print("|" + "_" * 32 + "|" + "\n")
                continue

        except IndexError:
            return "\n"

        sort_folder(path)
        delete_empty_folder(path)
        unpack_archive(path)
        delete_empty_folder(path)
        files_sorter(path)
        # files_ext(path)

        print("\n If you like to continue type 'resume' or type 'exit' to exit\n")
        user_answer = input("|>>> ")
        if user_answer.lower() in ("close", "exit", "goodbye", "0"):
            return '\nGood bye!'
        else:
            print("_" * 34)
            print("| Input path to folder:")
            continue


if __name__ == "__main__":
    sorter_starter()
