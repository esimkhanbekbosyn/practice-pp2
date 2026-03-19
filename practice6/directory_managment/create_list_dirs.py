from pathlib import Path
import os

base_dir = Path("workspace")
nested_dir = base_dir / "projects" / "python" / "practice6"

# Create nested directories
nested_dir.mkdir(parents=True, exist_ok=True)
print("Nested directories created.")

# Current working directory
print("Current working directory:")
print(os.getcwd())

# List files and folders in current directory
print("\nItems in current directory:")
for item in os.listdir():
    print(item)

# List files and folders in workspace
print("\nItems in workspace:")
for item in os.listdir(base_dir):
    print(item)