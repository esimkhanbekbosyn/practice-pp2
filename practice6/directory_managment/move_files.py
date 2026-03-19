from pathlib import Path
import shutil

source_dir = Path("source_files")
target_dir = Path("target_files")

source_dir.mkdir(exist_ok=True)
target_dir.mkdir(exist_ok=True)

# Create sample files
file1 = source_dir / "notes.txt"
file2 = source_dir / "data.csv"
file3 = source_dir / "report.txt"

with open(file1, "w", encoding="utf-8") as f:
    f.write("Text file 1")

with open(file2, "w", encoding="utf-8") as f:
    f.write("id,name\n1,Ali")

with open(file3, "w", encoding="utf-8") as f:
    f.write("Text file 2")

print("Sample files created.")

# Find files by extension
print("\nTXT files in source_files:")
for file in source_dir.iterdir():
    if file.suffix == ".txt":
        print(file.name)

# Copy txt files to target directory
for file in source_dir.iterdir():
    if file.suffix == ".txt":
        shutil.copy(file, target_dir / file.name)

print("\nTXT files copied to target_files.")

# Move csv file
csv_file = source_dir / "data.csv"
if csv_file.exists():
    shutil.move(str(csv_file), str(target_dir / csv_file.name))
    print("CSV file moved to target_files.")