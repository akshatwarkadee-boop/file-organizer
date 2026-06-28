# ============================================================
#  File Organizer Script — Pure Python, Standard Library Only
#  Author  : Akshat
#  Modules : os, pathlib, shutil, hashlib, datetime
# ============================================================

import os
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
from collections import defaultdict


# ──────────────────────────────────────────
#  EXTENSION → CATEGORY MAP
#  Add more extensions here anytime
# ──────────────────────────────────────────

EXTENSION_MAP = {
    # Images
    "Images":     [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg",
                   ".webp", ".ico", ".tiff", ".heic", ".raw"],
    # Videos
    "Videos":     [".mp4", ".mkv", ".mov", ".avi", ".wmv",
                   ".flv", ".webm", ".m4v", ".3gp"],
    # Audio
    "Audio":      [".mp3", ".wav", ".flac", ".aac", ".ogg",
                   ".wma", ".m4a", ".opus"],
    # Documents
    "Documents":  [".pdf", ".doc", ".docx", ".txt", ".rtf",
                   ".odt", ".pages", ".tex", ".md"],
    # Spreadsheets
    "Spreadsheets": [".xls", ".xlsx", ".csv", ".ods", ".numbers"],
    # Presentations
    "Presentations": [".ppt", ".pptx", ".odp", ".key"],
    # Code
    "Code":       [".py", ".js", ".ts", ".html", ".css", ".java",
                   ".c", ".cpp", ".h", ".cs", ".go", ".rs",
                   ".php", ".rb", ".sh", ".json", ".xml", ".yaml",
                   ".yml", ".toml", ".sql", ".r", ".swift"],
    # Archives
    "Archives":   [".zip", ".tar", ".gz", ".rar", ".7z",
                   ".bz2", ".xz", ".iso"],
    # Executables & Installers
    "Installers": [".exe", ".msi", ".dmg", ".pkg", ".deb", ".rpm", ".apk"],
    # Fonts
    "Fonts":      [".ttf", ".otf", ".woff", ".woff2"],
    # Data
    "Data":       [".db", ".sqlite", ".sql", ".parquet", ".feather"],
}


# ──────────────────────────────────────────
#  HELPERS — Display
# ──────────────────────────────────────────

def divider(char="─", width=58):
    print(char * width)

def header(title):
    print("\n" + "═" * 58)
    print(f"  {title}")
    print("═" * 58)

def format_size(num_bytes):
    """Turn raw bytes into human-readable size string."""
    for unit in ["B", "KB", "MB", "GB"]:
        if num_bytes < 1024:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.1f} TB"


# ──────────────────────────────────────────
#  HELPERS — File System
# ──────────────────────────────────────────

def resolve_folder(path_str):
    """
    Take whatever the user typed and return an absolute Path.
    Supports: ~/Downloads, relative paths, absolute paths.
    """
    return Path(path_str).expanduser().resolve()


def get_category(extension):
    """Return the category folder name for a given extension."""
    ext = extension.lower()
    for category, ext_list in EXTENSION_MAP.items():
        if ext in ext_list:
            return category
    return "Others"


def safe_move(src, dest_dir):
    """
    Move src file into dest_dir.
    If a file with the same name already exists there,
    append _2, _3, etc. instead of overwriting.
    Returns the final destination path.
    """
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.name

    if dest.exists() and dest != src:
        stem      = src.stem
        suffix    = src.suffix
        counter   = 2
        while dest.exists():
            dest = dest_dir / f"{stem}_{counter}{suffix}"
            counter += 1

    shutil.move(str(src), str(dest))
    return dest


def get_file_hash(filepath, chunk_size=65536):
    """
    Compute MD5 hash of a file in chunks (safe for large files).
    Two identical files → identical hash.
    """
    hasher = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)
        return hasher.hexdigest()
    except (PermissionError, OSError):
        return None


def scan_files(folder, recursive=False):
    """
    Return a list of Path objects for every file in the folder.
    If recursive=True, also scans sub-folders.
    Hidden files (starting with .) are skipped.
    """
    folder = Path(folder)
    pattern = "**/*" if recursive else "*"
    return [
        f for f in folder.glob(pattern)
        if f.is_file() and not f.name.startswith(".")
    ]


# ──────────────────────────────────────────
#  FEATURE 1 — Sort by Extension (Category)
# ──────────────────────────────────────────

def sort_by_extension(folder):
    """
    Move every file in folder into a sub-folder named after its category.
    e.g.  Downloads/photo.jpg  →  Downloads/Images/photo.jpg
    """
    header("📂  SORT FILES BY TYPE")

    folder = resolve_folder(folder)
    if not folder.exists():
        print(f"\n  ✗  Folder not found: {folder}\n")
        return

    files = scan_files(folder)
    if not files:
        print(f"\n  No files found in {folder}\n")
        return

    # Preview first
    print(f"\n  Folder : {folder}")
    print(f"  Files  : {len(files)} found\n")

    # Count what will go where
    preview = defaultdict(list)
    for f in files:
        cat = get_category(f.suffix)
        preview[cat].append(f)

    divider()
    print(f"  {'CATEGORY':<20} {'FILES':>6}   EXAMPLES")
    divider()
    for cat in sorted(preview.keys()):
        file_list = preview[cat]
        examples  = ", ".join(f.name for f in file_list[:2])
        more      = f"  +{len(file_list)-2} more" if len(file_list) > 2 else ""
        print(f"  {cat:<20} {len(file_list):>5}   {examples}{more}")
    divider()

    confirm = input("\n  Proceed with sorting? (y/n): ").strip().lower()
    if confirm not in ("y", "yes"):
        print("  Cancelled.\n")
        return

    # Move files
    moved   = 0
    skipped = 0
    log     = []

    print()
    for f in files:
        cat      = get_category(f.suffix)
        dest_dir = folder / cat

        # Don't move files that are already inside a category subfolder
        if f.parent == folder:
            dest = safe_move(f, dest_dir)
            log.append(f"  MOVED  {f.name:<40} → {cat}/")
            moved += 1
        else:
            skipped += 1

    # Print log
    for line in log:
        print(line)

    print()
    divider()
    print(f"  ✓  Done!  {moved} file(s) moved,  {skipped} skipped.")
    divider()

    # Save log file
    log_path = folder / "organizer_log.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a", encoding="utf-8") as lf:
        lf.write(f"\n[{timestamp}] — Sort by Extension\n")
        lf.write("\n".join(log) + "\n")
    print(f"  Log saved → {log_path.name}\n")


# ──────────────────────────────────────────
#  FEATURE 2 — Sort by Date
# ──────────────────────────────────────────

def sort_by_date(folder):
    """
    Move every file into a YYYY/YYYY-MM sub-folder based on
    the file's last-modified date.
    e.g.  Downloads/photo.jpg  →  Downloads/2024/2024-06/photo.jpg
    """
    header("📅  SORT FILES BY DATE")

    folder = resolve_folder(folder)
    if not folder.exists():
        print(f"\n  ✗  Folder not found: {folder}\n")
        return

    files = scan_files(folder)
    if not files:
        print(f"\n  No files found in {folder}\n")
        return

    print(f"\n  Folder : {folder}")
    print(f"  Files  : {len(files)} found\n")

    # Group by YYYY-MM for preview
    date_groups = defaultdict(list)
    for f in files:
        mtime     = os.path.getmtime(f)
        dt        = datetime.fromtimestamp(mtime)
        month_key = dt.strftime("%Y-%m")
        date_groups[month_key].append(f)

    divider()
    print(f"  {'MONTH':<12} {'FILES':>6}   SIZE")
    divider()
    for month in sorted(date_groups.keys()):
        file_list  = date_groups[month]
        total_size = sum(f.stat().st_size for f in file_list)
        print(f"  {month:<12} {len(file_list):>5}   {format_size(total_size)}")
    divider()

    confirm = input("\n  Proceed with date-based sorting? (y/n): ").strip().lower()
    if confirm not in ("y", "yes"):
        print("  Cancelled.\n")
        return

    moved = 0
    log   = []
    print()

    for f in files:
        if f.parent != folder:
            continue                   # Already in a sub-folder

        mtime    = os.path.getmtime(f)
        dt       = datetime.fromtimestamp(mtime)
        year     = dt.strftime("%Y")
        month    = dt.strftime("%Y-%m")
        dest_dir = folder / year / month

        dest = safe_move(f, dest_dir)
        log.append(f"  MOVED  {f.name:<40} → {year}/{month}/")
        print(log[-1])
        moved += 1

    print()
    divider()
    print(f"  ✓  Done!  {moved} file(s) organised by date.")
    divider()

    log_path  = folder / "organizer_log.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a", encoding="utf-8") as lf:
        lf.write(f"\n[{timestamp}] — Sort by Date\n")
        lf.write("\n".join(log) + "\n")
    print(f"  Log saved → {log_path.name}\n")


# ──────────────────────────────────────────
#  FEATURE 3 — Duplicate Finder
# ──────────────────────────────────────────

def find_duplicates(folder):
    """
    Hash every file in folder (and sub-folders).
    Group files with identical hashes — those are exact duplicates.
    Show them grouped so the user can decide what to delete.
    """
    header("🔍  DUPLICATE FILE FINDER")

    folder = resolve_folder(folder)
    if not folder.exists():
        print(f"\n  ✗  Folder not found: {folder}\n")
        return

    print(f"\n  Scanning (including sub-folders): {folder}")
    print("  Hashing files... this may take a moment for large folders.\n")

    files = scan_files(folder, recursive=True)
    if not files:
        print("  No files found.\n")
        return

    # Build hash → [list of files] map
    hash_map = defaultdict(list)
    for i, f in enumerate(files, 1):
        print(f"  [{i:>4}/{len(files)}]  {f.name[:50]:<50}", end="\r")
        file_hash = get_file_hash(f)
        if file_hash:
            hash_map[file_hash].append(f)

    print(" " * 60, end="\r")   # Clear the progress line

    # Keep only hashes that have more than 1 file
    duplicates = {h: paths for h, paths in hash_map.items() if len(paths) > 1}

    if not duplicates:
        print("  ✓  No duplicate files found!\n")
        return

    # Count wasted space
    wasted_bytes = 0
    for paths in duplicates.values():
        size         = paths[0].stat().st_size
        wasted_bytes += size * (len(paths) - 1)

    print(f"  Found {len(duplicates)} duplicate group(s).")
    print(f"  Wasted space: {format_size(wasted_bytes)}\n")
    divider()

    for group_num, (file_hash, paths) in enumerate(duplicates.items(), 1):
        size = paths[0].stat().st_size
        print(f"\n  GROUP {group_num}  │  {len(paths)} copies  │  {format_size(size)} each")
        divider("·", 58)
        for idx, p in enumerate(paths):
            mtime = datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d")
            # Show path relative to folder for readability
            try:
                rel = p.relative_to(folder)
            except ValueError:
                rel = p
            marker = "  [KEEP?]" if idx == 0 else "  [DUPE] "
            print(f"{marker}  {str(rel):<48}  {mtime}")
    divider()

    print(f"\n  Wasted space total: {format_size(wasted_bytes)}")
    print("  Review the list above and manually delete the [DUPE] files.")
    print("  Tip: Keep the copy in the most organised location.\n")

    # Save report
    report_path = folder / "duplicates_report.txt"
    with open(report_path, "w", encoding="utf-8") as rf:
        rf.write(f"Duplicate Report — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        rf.write(f"Folder: {folder}\n\n")
        for group_num, (file_hash, paths) in enumerate(duplicates.items(), 1):
            size = paths[0].stat().st_size
            rf.write(f"GROUP {group_num}  |  {len(paths)} copies  |  {format_size(size)} each\n")
            for p in paths:
                rf.write(f"  {p}\n")
            rf.write("\n")
        rf.write(f"Total wasted space: {format_size(wasted_bytes)}\n")
    print(f"  Report saved → {report_path.name}\n")


# ──────────────────────────────────────────
#  FEATURE 4 — Folder Stats (bonus)
# ──────────────────────────────────────────

def folder_stats(folder):
    """Quick breakdown of what's in the folder by type and size."""
    header("📊  FOLDER STATISTICS")

    folder = resolve_folder(folder)
    if not folder.exists():
        print(f"\n  ✗  Folder not found: {folder}\n")
        return

    files = scan_files(folder, recursive=True)
    if not files:
        print("  Folder is empty.\n")
        return

    # Group by category
    cat_data = defaultdict(lambda: {"count": 0, "size": 0})
    for f in files:
        cat = get_category(f.suffix)
        cat_data[cat]["count"] += 1
        cat_data[cat]["size"]  += f.stat().st_size

    total_files = len(files)
    total_size  = sum(f.stat().st_size for f in files)

    print(f"\n  Location  : {folder}")
    print(f"  Total files: {total_files}")
    print(f"  Total size : {format_size(total_size)}\n")

    divider()
    print(f"  {'CATEGORY':<20} {'FILES':>6}   {'SIZE':>10}   BAR")
    divider()

    for cat in sorted(cat_data.keys(), key=lambda c: cat_data[c]["size"], reverse=True):
        info     = cat_data[cat]
        pct      = info["size"] / total_size if total_size > 0 else 0
        bar_len  = int(pct * 20)
        bar      = "▓" * bar_len + "░" * (20 - bar_len)
        print(
            f"  {cat:<20} {info['count']:>5}   "
            f"{format_size(info['size']):>10}   [{bar}]"
        )

    divider()
    print(f"  {'TOTAL':<20} {total_files:>5}   {format_size(total_size):>10}")
    divider()
    print()


# ──────────────────────────────────────────
#  INPUT HELPERS
# ──────────────────────────────────────────

def get_target_folder():
    """Ask for a folder path and validate it exists."""
    print()
    print("  Common paths:")
    print("  ~/Downloads    ~/Desktop    ~/Documents")
    print()
    while True:
        raw = input("  Enter folder path: ").strip()
        if not raw:
            print("  ✗  Please enter a path.")
            continue
        path = resolve_folder(raw)
        if path.is_dir():
            return str(path)
        print(f"  ✗  '{path}' is not a valid folder. Try again.")


# ──────────────────────────────────────────
#  MAIN MENU
# ──────────────────────────────────────────

def show_menu():
    print("\n" + "═" * 58)
    print("  🗂️   FILE ORGANIZER SCRIPT")
    print("═" * 58)
    print("  1.  📂  Sort files by Type  (Images, Videos, Docs…)")
    print("  2.  📅  Sort files by Date  (2024/2024-06/file)")
    print("  3.  🔍  Find Duplicate files")
    print("  4.  📊  Folder Statistics")
    print("─" * 58)
    print("  Q.  Quit")
    print("─" * 58)


def main():
    print("\n  Welcome to File Organizer!")
    print("  Point it at any folder — Downloads, Desktop, anywhere.")
    print("  All moves are logged. Nothing is permanently deleted.\n")

    actions = {
        "1": sort_by_extension,
        "2": sort_by_date,
        "3": find_duplicates,
        "4": folder_stats,
    }

    while True:
        show_menu()
        choice = input("  Your choice: ").strip().upper()

        if choice == "Q":
            print("\n  Goodbye! Stay organised. 📁\n")
            break
        elif choice in actions:
            folder = get_target_folder()
            actions[choice](folder)
        else:
            print(f"\n  ✗  '{choice}' is not valid. Pick 1–4 or Q.\n")


# ──────────────────────────────────────────
#  ENTRY POINT
# ──────────────────────────────────────────

if __name__ == "__main__":
    main()