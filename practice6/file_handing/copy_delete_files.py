from pathlib import Path
import shutil

source = Path("sample.txt")
backup_dir = Path("backup")
backup_dir.mkdir(exist_ok=True)

backup_file = backup_dir / "sample_backup.txt"

# Copy file
if source.exists():
    shutil.copy(source, backup_file)
    print("File copied to backup folder.")
else:
    print("Source file does not exist.")

# Verify backup content
if backup_file.exists():
    with open(backup_file, "r", encoding="utf-8") as file:
        print("=== Backup file content ===")
        print(file.read())

# Safe delete example
temp_file = Path("temp_to_delete.txt")
with open(temp_file, "w", encoding="utf-8") as file:
    file.write("This file will be deleted.")

if temp_file.exists():
    temp_file.unlink()
    print("Temporary file deleted safely.")
else:
    print("Temporary file not found.")