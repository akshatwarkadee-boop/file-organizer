# File Organizer Script 🗂️

> A real-world automation script that organises any folder on your computer.  
> Powered by Python's `os`, `pathlib`, `shutil`, and `hashlib` — zero pip installs.  

---

## What It Does

| Feature | What happens |
|---|---|
| **Sort by Type** | Moves files into `Images/`, `Videos/`, `Documents/`, `Code/` etc. |
| **Sort by Date** | Moves files into `2024/2024-06/` folder structure |
| **Duplicate Finder** | Hashes every file, groups exact copies, shows wasted space |
| **Folder Stats** | Visual breakdown of file types and sizes with % bars |

All moves are logged to `organizer_log.txt`. Nothing is deleted.

---

## How to Run

```bash
python organizer.py
```

No `pip install` needed. Works on macOS, Windows, and Linux.

---

## Demo

```
══════════════════════════════════════════════════════════
  🗂️  FILE ORGANIZER SCRIPT
══════════════════════════════════════════════════════════
  1.  📂  Sort files by Type
  2.  📅  Sort files by Date
  3.  🔍  Find Duplicate files
  4.  📊  Folder Statistics
  Q.  Quit

  Enter folder path: ~/Downloads

  CATEGORY             FILES   EXAMPLES
  ─────────────────────────────────────────────
  Documents                3   resume.pdf, notes.txt
  Images                   8   photo.jpg, screenshot.png  +6 more
  Installers               2   setup.exe, app.dmg
  Videos                   1   demo.mp4
  ─────────────────────────────────────────────

  Proceed with sorting? (y/n): y

  MOVED  photo.jpg      → Images/
  MOVED  resume.pdf     → Documents/
  MOVED  demo.mp4       → Videos/
  ...
  ✓  Done!  14 file(s) moved, 0 skipped.
  Log saved → organizer_log.txt
```

---

## Extension Categories

| Folder | Extensions |
|---|---|
| Images | .jpg .jpeg .png .gif .bmp .svg .webp .heic |
| Videos | .mp4 .mkv .mov .avi .wmv .flv .webm |
| Audio | .mp3 .wav .flac .aac .ogg .m4a |
| Documents | .pdf .doc .docx .txt .md .rtf .odt |
| Spreadsheets | .xls .xlsx .csv .numbers |
| Code | .py .js .html .css .java .c .cpp .go .rs |
| Archives | .zip .tar .gz .rar .7z |
| Installers | .exe .dmg .pkg .deb .apk |
| Others | Anything not in the list above |

---

## Safety Features

- **Preview before moving** — shows exactly what will be moved and where
- **Confirmation prompt** — always asks before touching files
- **No overwrites** — if a file with same name exists, appends `_2`, `_3`, etc.
- **Move log** — every action written to `organizer_log.txt`
- **Duplicate report** — saved to `duplicates_report.txt`, nothing auto-deleted
- **Skips hidden files** — files starting with `.` are never touched

---

## What I Learned

- `pathlib.Path` — modern, cross-platform file path handling
- `Path.expanduser()` — handles `~/Downloads` on any OS
- `shutil.move()` — moves files safely across directories
- `hashlib.md5()` — hashing file contents to detect duplicates
- `os.path.getmtime()` — reading file modification timestamps
- `defaultdict(list)` — grouping data without key-existence checks
- Reading files in binary chunks for memory safety with large files

---

## Project Structure

```
file-organizer/
├── organizer.py          ← All logic (single file)
├── README.md
├── GITHUB_SETUP.md
└── .gitignore
```

Files created at runtime (not pushed to GitHub):
```
your-folder/
├── organizer_log.txt     ← created after sorting
└── duplicates_report.txt ← created after duplicate scan
```

---

## Author

**Akshat** — B.E. Civil Engineering @ UIT Barkatullah University  
Building an AI Engineering career, one project at a time.