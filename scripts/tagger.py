import os
import re
import shutil
from collections import Counter
import markdown2


def find_md_files(directory):
    md_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                md_files.append(os.path.join(root, file))
    return md_files

def extract_tags(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        tags = re.findall(r'#([\w-]+)', content)
        return tags

def count_tags(directory):
    md_files = find_md_files(directory)
    all_tags = []
    file_tags_map = {}
    for file_path in md_files:
        tags = extract_tags(file_path)
        all_tags.extend(tags)
        for tag in tags:
            if tag not in file_tags_map:
                file_tags_map[tag] = []
            file_tags_map[tag].append(file_path)
    tag_count = Counter(all_tags)
    return tag_count, file_tags_map

def generate_tag_pages(directory, tag_counts, file_tags_map):
    if os.path.exists(directory):
        shutil.rmtree(directory)  # Delete the tags directory if it already exists
    os.makedirs(directory)  # Create the tags directory

    tag_template = """---
layout: default
title: {tag}
---
# {tag}

Occurrences: {count}

**Files:**

{file_list}
"""
    for tag, count in tag_counts.items():
        file_list = "\n".join(["- [{}]({})".format(os.path.basename(file_path), file_path) for file_path in file_tags_map[tag]])
        tag_page_content = tag_template.format(tag=tag, count=count, file_list=file_list)
        tag_file_path = os.path.join(directory, f"{tag}.md")
        with open(tag_file_path, 'w') as tag_file:
            tag_file.write(tag_page_content)

def generate_tags_page(directory, tag_counts):
    tags_page_template = """Tags

<table>
  <tr>
    <th>Tag</th>
    <th>Frequency</th>
  </tr>
{tag_table}
</table>
"""
    sorted_counts = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
    tag_table_rows = ""
    for tag, count in sorted_counts:
        tag_table_rows += f"  <tr>\n    <td><a href='/tags/{tag}.html'>{tag}</a></td>\n    <td>{count}</td>\n  </tr>\n"
    tags_page_content = tags_page_template.format(tag_table=tag_table_rows)
    tags_page_path = os.path.join(directory, "..", "tags.html")
    with open(tags_page_path, 'w') as tags_page_file:
        tags_page_file.write(tags_page_content)


def print_tag_counts(tag_counts):
    sorted_counts = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)
    for tag, count in sorted_counts:
        print(f"{tag}: {count}")

# Replace 'directory_path' with the path to the directory you want to search
directory_path = 'content'
tags_directory = 'content/tags'
tag_counts, file_tags_map = count_tags(directory_path)
print_tag_counts(tag_counts)
generate_tag_pages(tags_directory, tag_counts, file_tags_map)
generate_tags_page(tags_directory, tag_counts)
