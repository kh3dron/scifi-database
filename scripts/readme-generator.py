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
link_counts = {}

tag_pattern = r'#\w+(?:-\w+)*(?:/\w+(?:-\w+)*)*'
link_pattern = r'\[\[([^\]]+)\]\]'

def pattern_parse(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        tag_count = 0
        link_count = 0
        content = file.read()
        
        tags = re.findall(tag_pattern, content)
        for tag in tags:
            tag_parts = tag.split('/')
            for i in range(1, len(tag_parts) + 1):
                sub_tag = '/'.join(tag_parts[:i])
                if sub_tag in tag_counts:
                    tag_counts[sub_tag] += 1
                else:
                    tag_counts[sub_tag] = 1
        
        
        links = re.findall(link_pattern, content)
        for link in links:
            link_count += 1
            if link in link_counts:
                link_counts[link] += 1
            else:
                link_counts[link] = 1
            
    return tag_count, link_count

total_tag_count = 0
total_link_count = 0

for root, dirs, files in os.walk(directory):
    for filename in files:
        if filename.endswith('.md'):
            file_path = os.path.join(root, filename)
            tag_count, link_count = pattern_parse(file_path)
            total_tag_count += tag_count
            total_link_count += link_count

sorted_tag_counts = sorted(tag_counts.items(), key=lambda x: (-x[1], x[0]))
sorted_link_counts = sorted(link_counts.items(), key=lambda x: (-x[1], x[0]))

# Generate README.md

with open("../README.md", "w") as file:
    
    file.write(f"### Global Statistics\n\n")
    
    file.write(f"* Total Pages: {total}\n")
    file.write(f"* Total Tag occurrences: {total_tag_count}\n")
    file.write(f"* Total Link occurrences: {total_link_count}\n\n")
    
    file.write(f"Pages by Category:\n")
    file.write(f"  * Short Stories: {stories}\n")
    file.write(f"  * TV Episodes: {tv}\n")
    file.write(f"  * Novels: {novels}\n")
    file.write(f"  * Comics: {comics}\n")
    file.write(f"  * Movies: {movies}\n")
    file.write(f"  * People: {people}\n")
    
    
    file.write(f"\nUnique tags: {len(tag_counts)}\n")
    file.write(f"Tags by usage:\n\n")
    for tag, count in sorted_tag_counts:
        file.write(f'* {tag}: {count}\n')

    file.write(f"\nUnique links: {len(link_counts)}\n")
    file.write(f"Links by usage:\n\n")
    for link, count in sorted_link_counts:
        file.write(f'* {link}: {count}\n')
    