import os
import shutil
from pathlib import Path
from datetime import datetime


# Folders to organize 
FOLDERS_TO_ORGANIZE = [
    str(Path.home() / "Desktop"),
    str(Path.home() / "Downloads"),
]

# File categories
FILE_CATEGORIES = {
    "PDFs": [".pdf"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".ico"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov", ".wmv"],
    "Audio": [".mp3", ".wav", ".flac", ".aac"],
    "Documents": [".doc", ".docx", ".txt", ".pptx", ".xlsx", ".csv"],
    "Code": [".py", ".js", ".html", ".css", ".json", ".xml", ".ipynb"],
    "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Executables": [".exe", ".msi", ".bat"],
}

def get_category(file_ext):
    for category, extensions in FILE_CATEGORIES.items():
        if file_ext.lower() in extensions:
            return category
    return "Others"

def organize_folder(folder_path):
    folder = Path(folder_path)
    
    if not folder.exists():
        print(f" Folder not found: {folder_path}")
        return
    
    print(f"\n Organizing: {folder_path}")
    print("=" * 50)
    
    moved = 0
    skipped = 0
    
    for file in folder.iterdir():
        # Skip folders and hidden files
        if file.is_dir() or file.name.startswith('.') or file.suffix == '.lnk':
            skipped += 1
            continue
            
        # Get category
        category = get_category(file.suffix)
        
        # Create category folder
        category_folder = folder / category
        category_folder.mkdir(exist_ok=True)
        
        # Move file
        destination = category_folder / file.name
        
        # If file already exists, add timestamp
        if destination.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_name = f"{file.stem}_{timestamp}{file.suffix}"
            destination = category_folder / new_name
        
        shutil.move(str(file), str(destination))
        print(f"{file.name} → {category}/")
        moved += 1
    
    print("=" * 50)
    print(f"Moved: {moved} files")
    print(f"Skipped: {skipped} items")
    return moved

def main():
    print("SHAHID'S FILE ORGANIZER AGENT")
    print("=" * 50)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    total_moved = 0
    
    for folder in FOLDERS_TO_ORGANIZE:
        moved = organize_folder(folder)
        if moved:
            total_moved += moved
    
    print(f"\n DONE! Total files organized: {total_moved}")
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()