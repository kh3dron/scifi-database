#!/usr/bin/env bash

# add_fields.sh - Add standardized front-matter fields to all markdown files in the scifi-database
# This script will add title, author, rating, read, and tags to each .md file.
# It works recursively through the content/ directory.

set -euo pipefail

# Configuration
CONTENT_DIR="/home/tristan/Documents/Github/scifi-database/content"
BACKUP_DIR="${CONTENT_DIR}/_backup"  # Optional backup location
TMPDIR="/tmp/add_fields_$(date +%s)"

# Ensure backup directory exists
mkdir -p "${BACKUP_DIR}"

# Function to extract metadata from a file
# Returns a JSON object like: { "title":"...", "author":"...", "rating":"...", "read":"...", "tags":["..."...]}
get_metadata() {
    local file="$1"
    # Extract title from filename (strip .md)
    local title=$(basename "${file}" .md)
    # If title is empty, fallback to full path
    if [[ -z "${title}" ]]; then title="${file##*/}"; fi

    # Try to read existing metadata from front‑matter
    local meta="$(awk -F': ' '/^\s*[tT]itle:/{print "title:"$2; exit}' "${file}" 2>/dev/null || echo "title:${title}")"
    meta="$(awk -F': ' '/^\s*[aA]uthor:/{print $0; exit}' "${file}" 2>/dev/null || echo "author:${title}")"
    meta="$(awk -F': ' '/^\s*[rR]ating:/{print "rating:"$2; exit}' "${file}" 2>/dev/null || echo "rating:0")"
    meta="$(awk -F': ' '/^\s*[rR]ead:/{print "read:"$2; exit}' "${file}" 2>/dev/null || echo "read:$(date +%F)")"
    local tags=$(awk '/^\s*#/{print $0}' "${file}" | tr '\n' ' ' | sed 's/^[^#]*//;s/\s*$//')
    meta="$(echo "${meta}" | sed "s/tags:${tags// /\"}/")"

    # Store as JSON for easy parsing later (we'll just echo it)
    echo "${meta// /\"}"
}

# Main loop over all markdown files
for file in "${CONTENT_DIR}"/**/*.md; do
    if [[ ! -e "${file}" ]]; then continue; fi

    echo "Processing ${file}"

    # Create a temporary working copy
    tmpfile="${TMPDIR}/${file##*/}.tmp"
    cp "${file}" "${tmpfile}"

    # Get metadata; if file lacks front‑matter, we'll inject it
    meta=$(get_metadata "${file}")
    title=$(echo "${meta}" | awk -F'"title:"' '{print $2}' | cut -d'"' -f2)
    author=$(echo "${meta}" | awk -F'"author:"' '{print $2}' | cut -d'"' -f2)
    rating=$(echo "${meta}" | awk -F'"rating:"' '{print $2}' | cut -d'"' -f2)
    read_date=$(echo "${meta}" | awk -F'"read:"' '{print $2}' | cut -d'"' -f2)
    tags=$(echo "${meta}" | awk -F'"tags:"' '{print $2}' | cut -d'"' -f2 | sed 's/\"//g' | sed 's/\/\s*/"/"')

    # Build the YAML front‑matter
    yaml="---\n"
    yaml+="title: ${title}\n"
    yaml+="author: ${author}\n"
    yaml+="rating: ${rating}\n"
    yaml+="read: ${read_date}\n"
    yaml+="tags: ${tags}\n"
    yaml+="---
"

    # Preserve any existing front‑matter
    if grep -q '^---' "${file}"; then
        # Insert new front‑matter after the first existing block
        sed -i "1,/^---/{/^---/{a${yaml}}" "${tmpfile}"\n    else
        # Prepend the new front‑matter
        printf "%s\n%s\n" "${yaml}" "$(cat "${tmpfile}")" > "${tmpfile}"\n    fi

    # Replace original file with updated version
    mv "${tmpfile}" "${file}"
    echo "Updated ${file}"

    # (Optional) create a backup copy
    cp "${file}" "${BACKUP_DIR}/${file##*/}.bak"
    echo "Backup saved to ${BACKUP_DIR}/${file##*/}.bak"
done

echo "All markdown files processed."
