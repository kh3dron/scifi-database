# Utility to point me to files that should be added to

import os
import random

def get_file_size(file_path):
    return os.path.getsize(file_path)

# Function to list files in a directory recursively
def list_files_recursive(directory):
    file_list = []
    for root, _, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith(".md") and "People" not in root: # People pages are more for linking than content, ignoring here
                file_path = os.path.join(root, file_name)
                file_name = file_path.replace("../content/", "")[:-3]
                file_list.append((file_name, get_file_size(file_path)))
    return file_list

start_directory = '../content'
file_list = list_files_recursive(start_directory)

# sort by file size and then alphabetically
file_list.sort(key=lambda x: (x[1], x[0]))

with open("../analysis/smallest-files.md", "w") as file:
    file.write(f"# Files listed by size\n\n")

    for file_path, file_size in file_list:
        file.write(f"* {file_path} - {file_size} bytes\n")
