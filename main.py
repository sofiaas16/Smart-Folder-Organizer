import sys
sys.dont_write_bytecode = True

import os
import shutil

from config import SOURCE_FOLDER, FOLDER_RULES, FOLDERS_CONTAINER, OTHERS_FOLDER
from analyzer import analyze
from cleaner import clean_inactive_files
from tidy import run as tidy_run



def get_existing_extensions():
    extensions = set()

    for item in os.listdir(SOURCE_FOLDER):
        path = os.path.join(SOURCE_FOLDER, item)

        if os.path.isfile(path) and not item.startswith("."):
            _, ext = os.path.splitext(item.lower())
            if ext:
                extensions.add(ext)

    return extensions


def create_needed_folders(existing_extensions):
    for folder, extensions in FOLDER_RULES.items():
        if any(ext in existing_extensions for ext in extensions):
            os.makedirs(os.path.join(SOURCE_FOLDER, folder), exist_ok=True)

    os.makedirs(os.path.join(SOURCE_FOLDER, OTHERS_FOLDER), exist_ok=True)


def move_existing_folders():
    container_path = os.path.join(SOURCE_FOLDER, FOLDERS_CONTAINER)
    os.makedirs(container_path, exist_ok=True)

    for item in os.listdir(SOURCE_FOLDER):
        path = os.path.join(SOURCE_FOLDER, item)

        if (
            os.path.isdir(path)
            and item not in FOLDER_RULES
            and item not in {FOLDERS_CONTAINER, OTHERS_FOLDER}
        ):
            try:
                shutil.move(path, os.path.join(container_path, item))
            except Exception:
                pass


def organize_files():
    for item in os.listdir(SOURCE_FOLDER):
        file_path = os.path.join(SOURCE_FOLDER, item)

        if not os.path.isfile(file_path):
            continue

        if item.startswith("."):
            continue

        _, ext = os.path.splitext(item.lower())
        moved = False

        for folder, extensions in FOLDER_RULES.items():
            if ext in extensions:
                try:
                    shutil.move(
                        file_path,
                        os.path.join(SOURCE_FOLDER, folder, item)
                    )
                    print(f"📁 {item} → {folder}")
                    moved = True
                except PermissionError:
                    print(f"⚠️ In use: {item}")
                break

        if not moved:
            try:
                shutil.move(
                    file_path,
                    os.path.join(SOURCE_FOLDER, OTHERS_FOLDER, item)
                )
                print(f"📁 {item} → {OTHERS_FOLDER}")
            except PermissionError:
                print(f"⚠️ In use: {item}")


def run_organizer():
    existing_extensions = get_existing_extensions()
    create_needed_folders(existing_extensions)
    move_existing_folders()
    organize_files()
    print("\n✅ Organization complete")




def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


def pause():
    input("\nPress ENTER to continue...")


def show_menu():
    print("""
🧠 SMART FOLDER ORGANIZER
────────────────────────
1️⃣  Organize files by type
2️⃣  Delete files inactive for +1 year
3️⃣  Tidy mode (light cleanup)
4️⃣  Exit
""")


def main():
    clear_terminal()

    print("🔍 PREVIEW MODE — No changes have been made\n")
    analyze(SOURCE_FOLDER)

    confirm = input("\nDo you want to continue? (y/n): ").strip().lower()
    if confirm != "y":
        print("\n❌ Operation cancelled")
        return

    while True:
        clear_terminal()
        show_menu()

        option = input("Choose an option (1-4): ").strip()

        if option == "1":
            run_organizer()
            pause()

        elif option == "2":
            clean_inactive_files(SOURCE_FOLDER)
            pause()

        elif option == "3":
            tidy_run(SOURCE_FOLDER)
            pause()

        elif option == "4":
            print("\n👋 Bye!")
            break

        else:
            print("\n⚠️  Invalid option")
            pause()


if __name__ == "__main__":
    main()
