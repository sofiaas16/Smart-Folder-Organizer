import os
import time
from config import FOLDER_RULES, OTHERS_FOLDER

ONE_YEAR_SECONDS = 60 * 60 * 24 * 365


def analyze_folder(folder_path):
    report = {
        "by_type": {},
        "folders_count": 0,
        "unknown_files": [],
        "inactive_files": [],
        "oldest_file": None,
    }

    now = time.time()
    oldest_time = now

    for item in os.listdir(folder_path):
        path = os.path.join(folder_path, item)

        # Count folders
        if os.path.isdir(path):
            report["folders_count"] += 1
            continue

        if not os.path.isfile(path) or item.startswith("."):
            continue

        _, ext = os.path.splitext(item.lower())
        matched = False

        # Detect file type
        for folder, extensions in FOLDER_RULES.items():
            if ext in extensions:
                report["by_type"][folder] = report["by_type"].get(folder, 0) + 1
                matched = True
                break

        if not matched:
            report["unknown_files"].append(item)

        # Inactivity check
        last_modified = os.path.getmtime(path)
        inactivity_time = now - last_modified

        if inactivity_time > ONE_YEAR_SECONDS:
            report["inactive_files"].append((item, inactivity_time))

        # Oldest file
        if last_modified < oldest_time:
            oldest_time = last_modified
            report["oldest_file"] = (item, inactivity_time)

    return report


def print_report(report):
    print("\n📊 Folder Analysis Preview\n")

    for file_type, count in report["by_type"].items():
        print(f"📄 {file_type}: {count}")

    print(f"\n📁 Folders found: {report['folders_count']}")
    print(f"❓ Unknown files: {len(report['unknown_files'])}")
    print(f"🕰 Files inactive +1 year: {len(report['inactive_files'])}")

    if report["oldest_file"]:
        name, seconds = report["oldest_file"]
        years = seconds // ONE_YEAR_SECONDS
        print(f"📜 Oldest file: {name} ({int(years)} years ago)")

    print("\n⚠️ No changes have been made yet.\n")


def analyze(folder_path):
    report = analyze_folder(folder_path)
    print_report(report)
