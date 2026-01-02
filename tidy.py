import os


def _normalize_filename(filename):
    name, ext = os.path.splitext(filename)
    name = name.strip().lower().replace(" ", "_")
    ext = ext.lower()
    return name + ext


def _remove_empty_folders(folder_path):
    removed = False

    for root, dirs, _ in os.walk(folder_path, topdown=False):
        for d in dirs:
            path = os.path.join(root, d)

            try:
                if not os.listdir(path):
                    os.rmdir(path)
                    print(f"🧹 Removed empty folder: {path}")
                    removed = True
            except Exception:
                pass

    if not removed:
        print("🧼 No empty folders found.")


def _normalize_filenames(folder_path):
    for item in os.listdir(folder_path):
        path = os.path.join(folder_path, item)

        if not os.path.isfile(path) or item.startswith("."):
            continue

        new_name = _normalize_filename(item)
        new_path = os.path.join(folder_path, new_name)

        if new_name != item and not os.path.exists(new_path):
            try:
                os.rename(path, new_path)
                print(f"✏️ {item} → {new_name}")
            except Exception:
                pass


def run(folder_path):
    print("\n🧹 Running tidy mode...\n")
    _normalize_filenames(folder_path)
    _remove_empty_folders(folder_path)
    print("\n✨ Tidy mode completed.\n")
