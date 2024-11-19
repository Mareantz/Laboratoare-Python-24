# Create a Python script that calculates the total size of all files in a directory provided as a command line
# argument. The script should:
#
# Use the sys module to read the directory path from the command line. Utilize the os module to iterate through all
# the files in the given directory and its subdirectories. Sum up the sizes of all files and display the total size
# in bytes. Implement exception handling for cases like the directory not existing, permission errors, or other file
# access issues.


import os
import sys


def calculate_directory_size(directory):
    total_size = 0
    try:
        if not os.path.isdir(directory):
            raise FileNotFoundError(f"The directory '{directory}' does not exist.")

        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    total_size += os.path.getsize(file_path)
                except Exception as e:
                    print(f"Could not access file '{file_path}': {e}")

        return total_size
    except Exception as e:
        print(f"Error: {e}")
        return None


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python calculate_size.py <directory_path>")
    else:
        directory = sys.argv[1]
        size = calculate_directory_size(directory)
        if size is not None:
            print(f"Total size of files in '{directory}': {size} bytes")
