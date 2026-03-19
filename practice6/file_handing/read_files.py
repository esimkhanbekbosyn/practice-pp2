from pathlib import Path

file_path = Path("sample.txt")

if file_path.exists():
    with open(file_path, "r", encoding="utf-8") as file:
        print("=== read() ===")
        print(file.read())

    with open(file_path, "r", encoding="utf-8") as file:
        print("=== readline() ===")
        print(file.readline().strip())
        print(file.readline().strip())

    with open(file_path, "r", encoding="utf-8") as file:
        print("=== readlines() ===")
        lines = file.readlines()
        for line in lines:
            print(line.strip())
else:
    print("File does not exist.")