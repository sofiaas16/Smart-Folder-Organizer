import os
import time

ONE_YEAR_SECONDS = 60 * 60 * 24 * 365


def clean_inactive_files(folder_path):
    now = time.time()
    inactive_files = []

    for item in os.listdir(folder_path):
        path = os.path.join(folder_path, item)

        if not os.path.isfile(path) or item.startswith("."):
            continue

        last_modified = os.path.getmtime(path)
        inactivity_time = now - last_modified

        if inactivity_time > ONE_YEAR_SECONDS:
            inactive_files.append((item, path, inactivity_time))

    if not inactive_files:
        print("✅ No inactive files found.")
        return

    print("\n🕰 Files inactive for more than 1 year:\n")

    for item, _, seconds in inactive_files:
        years = seconds // ONE_YEAR_SECONDS
        print(f"- {item} ({int(years)} years inactive)")

    print("\n⚠️ This action is PERMANENT.")
    confirm = input("Type DELETE to confirm: ")

    if confirm != "DELETE":
        print("❌ Operation cancelled.")
        return

    for _, path, _ in inactive_files:
        try:
            os.remove(path)
        except Exception:
            print(f"⚠️ Could not delete: {path}")

    print("🗑 Inactive files deleted successfully.")
