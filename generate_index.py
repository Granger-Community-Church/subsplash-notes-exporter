#!/usr/bin/env python3
"""
Generate index.json for the notes viewer
"""

import json
import os
from pathlib import Path
import re


def parse_frontmatter(content):
    """Extract YAML frontmatter from markdown content"""
    if not content.startswith('---'):
        return {}, content

    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content

    frontmatter_text = parts[1].strip()
    body = parts[2].strip()

    # Parse YAML-like frontmatter
    metadata = {}
    for line in frontmatter_text.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            metadata[key.strip()] = value.strip()

    return metadata, body


def generate_index(notes_dir="subsplash_notes", output_file="viewer/notes_index.json"):
    """Generate JSON index of all notes"""

    notes_path = Path(notes_dir)
    if not notes_path.exists():
        print(f"Error: Directory '{notes_dir}' not found")
        return False

    collections = {}
    all_notes = []

    # Scan all markdown files
    for md_file in notes_path.rglob("*.md"):
        # Skip the main README
        if md_file.name == "README.md" and md_file.parent == notes_path:
            continue

        # Get collection name from parent directory
        collection_name = md_file.parent.name

        # Read the file
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {md_file}: {e}")
            continue

        # Parse frontmatter
        metadata, body = parse_frontmatter(content)

        # Build note info
        note_info = {
            "title": metadata.get("title", md_file.stem),
            "subtitle": metadata.get("subtitle", ""),
            "author": metadata.get("author", ""),
            "collection": collection_name,
            "date": metadata.get("date", ""),
            "created": metadata.get("created", ""),
            "updated": metadata.get("updated", ""),
            "file_path": str(md_file.relative_to(notes_path).as_posix()),
            "color": metadata.get("color", "#5B4336"),
            "preview": body[:200] + "..." if len(body) > 200 else body,
            "content": body  # Full markdown content for static deployment
        }

        all_notes.append(note_info)

        # Track collections
        if collection_name not in collections:
            collections[collection_name] = {
                "name": collection_name,
                "count": 0
            }
        collections[collection_name]["count"] += 1

    # Sort notes by date (most recent first)
    all_notes.sort(key=lambda x: x.get("date", ""), reverse=True)

    # Create index structure
    index = {
        "total_notes": len(all_notes),
        "total_collections": len(collections),
        "collections": list(collections.values()),
        "notes": all_notes
    }

    # Write to JSON
    output_path = Path(output_file)
    output_path.parent.mkdir(exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    print(f"Generated index with {len(all_notes)} notes from {len(collections)} collections")
    print(f"Saved to: {output_path}")

    return True


if __name__ == "__main__":
    generate_index()
