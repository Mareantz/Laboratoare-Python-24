# Write a script using the os module that renames all files in a specified directory to have a sequential number
# prefix. For example, file1.txt, file2.txt, etc. Include error handling for cases like the directory not existing or
# files that can't be renamed.

import os
import sys


def rename_files_with_prefix(directory):
    try:
        if not os.path.isdir(directory):
            raise FileNotFoundError(f"The directory '{directory}' does not exist.")

        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

        if not files:
            print(f"No files found in the directory '{directory}'.")
            return

        files.sort()

        for i, file_name in enumerate(files, start=1):
            old_path = os.path.join(directory, file_name)
            new_name = f"{i:03d}_{file_name}"
            new_path = os.path.join(directory, new_name)

            try:
                os.rename(old_path, new_path)
                print(f"Renamed: '{file_name}' -> '{new_name}'")
            except Exception as e:
                print(f"Could not rename file '{file_name}': {e}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python rename_files.py <directory_path>")
    else:
        directory = sys.argv[1]
        rename_files_with_prefix(directory)
