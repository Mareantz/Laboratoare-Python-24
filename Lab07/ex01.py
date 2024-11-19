# Create a Python script that does the following:
# Takes a directory path and a file extension as command line arguments (use sys.argv).
# Searches for all files with the given extension in the specified directory (use os module).
# For each file found, read its contents and print them.
# Implement exception handling for invalid directory paths, incorrect file extensions, and file access errors.


import os
import sys


def search_and_print_files(directory, extension):
    try:
        if not os.path.isdir(directory):
            raise FileNotFoundError(f"The directory '{directory}' does not exist.")

        if not extension.startswith("."):
            raise ValueError("Invalid file extension. It should start with a '.' (e.g., '.txt').")

        found_files = [file for file in os.listdir(directory) if file.endswith(extension)]

        if not found_files:
            print(f"No files with the extension '{extension}' found in '{directory}'.")
            return

        for file in found_files:
            file_path = os.path.join(directory, file)
            try:
                with open(file_path, 'r') as f:
                    print(f"--- Contents of {file} ---")
                    print(f.read())
                    print("-" * 30)
            except Exception as e:
                print(f"Could not read file '{file}': {e}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <directory_path> <file_extension>")
    else:
        directory = sys.argv[1]
        extension = sys.argv[2]
        search_and_print_files(directory, extension)
