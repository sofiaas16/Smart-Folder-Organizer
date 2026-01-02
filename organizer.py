import os
import shutil
from config import FOLDER_RULES, FOLDERS_CONTAINER, OTHERS_FOLDER


def organize(folder_path):
    print("\n📦 Organizing files...\n")

    used_folders = set()
    used_others = False
    moved_folders = False
    
    # Move existing folders
    for item in os.listdir(folder_path):
        path = os.path.join(folder_path, item)

        if (
            os.path.isdir(path)
            and item not in FOLDER_RULES
            and item not in {FOLDERS_CONTAINER, OTHERS_FOLDER}
        ):
            container_path = os.path.join(folder_path, FOLDERS_CONTAINER)
            os.makedirs(container_path, exist_ok=True)

            try:
                shutil.move(path, os.path.join(container_path, item))
                moved_folders = True
            except Exception:
                pass

    #  Organize files

    for item in os.listdir(folder_path):
        file_path = os.path.join(folder_path, item)

        if not os.path.isfile(file_path) or item.startswith("."):
            continue

        _, ext = os.path.splitext(item.lower())
        moved = False

        for folder, extensions in FOLDER_RULES.items():
            if ext in extensions:
                target_dir = os.path.join(folder_path, folder)
                os.makedirs(target_dir, exist_ok=True)

                try:
                    shutil.move(file_path, os.path.join(target_dir, item))
                    print(f"📄 {item} → {folder}")
                    used_folders.add(folder)
                    moved = True
                except PermissionError:
                    print(f"⚠️ In use: {item}")
                break

        if not moved:
            others_path = os.path.join(folder_path, OTHERS_FOLDER)
            os.makedirs(others_path, exist_ok=True)

            try:
                shutil.move(file_path, os.path.join(others_path, item))
                print(f"❓ {item} → {OTHERS_FOLDER}")
                used_others = True
            except PermissionError:
                print(f"⚠️ In use: {item}")


    # Cleanup empty folders
    if not used_others:
        others_path = os.path.join(folder_path, OTHERS_FOLDER)
        if os.path.exists(others_path) and not os.listdir(others_path):
            os.rmdir(others_path)

    if not moved_folders:
        folders_path = os.path.join(folder_path, FOLDERS_CONTAINER)
        if os.path.exists(folders_path) and not os.listdir(folders_path):
            os.rmdir(folders_path)

    print("\n✅ Organization completed.\n")
