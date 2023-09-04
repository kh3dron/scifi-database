import os
import re
import shutil
from collections import Counter
import markdown2

directory = '../content'

# Count pages in each category

def count_pages_in_directory(directory):
    md_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                md_files.append(os.path.join(root, file))
    return len(md_files)

tv = count_pages_in_directory(directory + "/TV")
comics = count_pages_in_directory(directory + "/Comics")
movies = count_pages_in_directory(directory + "/Movies")
novels = count_pages_in_directory(directory + "/Novels")
stories = count_pages_in_directory(directory + "/Stories")
people = count_pages_in_directory(directory + "/People")
total = tv + comics + movies + novels + stories + people


# Count tags
# TODO: recursive tags

tag_counts = {}
tag_pattern = r'#\w+(?:-\w+)*'

def extract_tags_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        tags = re.findall(tag_pattern, content)
        for tag in tags:
            tag = tag.lower()
            if tag in tag_counts:
                tag_counts[tag] += 1
            else:
                tag_counts[tag] = 1

for root, dirs, files in os.walk(directory):
    for filename in files:
        if filename.endswith('.md'):
            file_path = os.path.join(root, filename)
            extract_tags_from_file(file_path)

# Generate README.md

with open("../README.md", "w") as file:
    file.write(f"# Total Entries: {total}\n")
    file.write(f"Entries by Category:\n\n")
    file.write(f"* Short Stories: {stories}\n")
    file.write(f"* TV Episodes: {tv}\n")
    file.write(f"* Novels: {novels}\n")
    file.write(f"* Comics: {comics}\n")
    file.write(f"* Movies: {movies}\n")
    file.write(f"* People: {people}\n\n")

    file.write(f"# Unique tags: {len(tag_counts)}\n")
    file.write(f"Occurrences of Tags:\n\n")
    for tag, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True):
        file.write(f'* {tag}: {count}' + "\n")
