# Write a Python script that counts the number of files with each extension in a given directory. The script should:
# Accept a directory path as a command line argument (using sys.argv). Use the os module to list all files in the
# directory. Count the number of files for each extension (e.g., .txt, .py, .jpg) and print out the counts. Include
# error handling for scenarios such as the directory not being found, no read permissions, or the directory being empty.


import os
import sys
from collections import Counter


def count_file_extensions(directory):
    try:
        if not os.path.isdir(directory):
            raise FileNotFoundError(f"The directory '{directory}' does not exist.")

        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

        if not files:
            print(f"The directory '{directory}' is empty.")
            return

        extension_counts = Counter(os.path.splitext(file)[1] for file in files)

        print(f"File extension counts in '{directory}':")
        for ext, count in extension_counts.items():
            ext_display = ext if ext else "(no extension)"
            print(f"  {ext_display}: {count}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python count_extensions.py <directory_path>")
    else:
        directory = sys.argv[1]
        count_file_extensions(directory)
