from pathlib import Path

# Create file path
file_path = Path("sample.txt")

# Write sample data
with open(file_path, "w", encoding="utf-8") as file:
    file.write("Python File Handling Practice\n")
    file.write("Line 1: Hello\n")
    file.write("Line 2: This is a sample file\n")
    file.write("Line 3: Practice 6\n")

print("File created and written successfully.")

# Append new lines
with open(file_path, "a", encoding="utf-8") as file:
    file.write("Line 4: Appended line\n")
    file.write("Line 5: Another appended line\n")

print("New lines appended successfully.")