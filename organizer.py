import os
import shutil

# Downloads folder ka rasta
downloads = os.path.join(os.path.expanduser("~"), "Downloads")

# Kaunsi file kis folder me jayegi
folders = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
    "Videos": [".mp4", ".mkv", ".avi"],
    "Music": [".mp3", ".wav"],
    "Programs": [".exe", ".msi", ".zip"],
}

count = 0
for file in os.listdir(downloads):
    path = os.path.join(downloads, file)
    if os.path.isfile(path):
        ext = os.path.splitext(file)[1].lower()
        for folder, extensions in folders.items():
            if ext in extensions:
                dest = os.path.join(downloads, folder)
                os.makedirs(dest, exist_ok=True)
                shutil.move(path, os.path.join(dest, file))
                print(f"{file} -> {folder}")
                count += 1
                break

print(f"\nDone! {count} files organized.")
