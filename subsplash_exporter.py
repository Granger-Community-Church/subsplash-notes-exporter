#!/usr/bin/env python3
"""
Subsplash Notes Exporter
Exports all your notes from notes.subsplash.com to markdown files
"""

import requests
import json
import os
from pathlib import Path
from datetime import datetime
import re


def sanitize_filename(filename):
    """Remove or replace characters that are invalid in filenames"""
    # Replace problematic characters with underscores
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')
    # Limit length to avoid filesystem issues
    if len(filename) > 200:
        filename = filename[:200]
    return filename


def export_notes(bearer_token, app_key=None, output_dir="subsplash_notes"):
    """
    Export all notes from Subsplash

    Args:
        bearer_token: Your JWT token from the Authorization header
        app_key: Your app key (visible in browser network requests to notes.subsplash.com)
        output_dir: Directory to save notes to
    """

    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # API endpoint
    url = f"https://notes.subsplash.com/fill-in/api/pages/list"
    params = {
        "appKey": app_key,
        "filter": json.dumps({
            "include": "collection",
            "order": "publish DESC"
        })
    }

    # Headers with authentication
    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Accept": "application/json"
    }

    print(f"Fetching notes from Subsplash...")

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()

        data = response.json()
        pages = data.get("pages", [])

        print(f"Found {len(pages)} notes to export\n")

        # Group notes by collection
        collections = {}
        for page in pages:
            collection_name = "Uncategorized"
            if page.get("collection"):
                collection_name = page["collection"].get("title", "Uncategorized")

            if collection_name not in collections:
                collections[collection_name] = []
            collections[collection_name].append(page)

        # Export each note
        exported_count = 0
        for collection_name, notes in collections.items():
            # Create collection folder
            collection_folder = output_path / sanitize_filename(collection_name)
            collection_folder.mkdir(exist_ok=True)

            print(f"Collection: {collection_name} ({len(notes)} notes)")

            for note in notes:
                # Create filename from title
                title = note.get("title", "Untitled")
                subtitle = note.get("subtitle", "")

                # Combine title and subtitle for filename
                if subtitle:
                    filename = f"{title} - {subtitle}.md"
                else:
                    filename = f"{title}.md"

                filename = sanitize_filename(filename)
                filepath = collection_folder / filename

                # Build markdown content with frontmatter
                content_parts = ["---"]
                content_parts.append(f"title: {title}")
                if subtitle:
                    content_parts.append(f"subtitle: {subtitle}")
                if note.get("author"):
                    content_parts.append(f"author: {note['author']}")
                if note.get("publish"):
                    publish_date = note["publish"]
                    content_parts.append(f"date: {publish_date}")
                if note.get("collection"):
                    content_parts.append(f"collection: {collection_name}")
                if note.get("color"):
                    content_parts.append(f"color: {note['color']}")

                content_parts.append(f"created: {note.get('created', '')}")
                content_parts.append(f"updated: {note.get('updated', '')}")
                content_parts.append(f"note_id: {note.get('id', '')}")
                content_parts.append(f"hid: {note.get('hid', '')}")
                content_parts.append("---")
                content_parts.append("")

                # Add the actual content
                note_content = note.get("content", "")
                content_parts.append(note_content)

                # Write to file
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(content_parts))

                print(f"  + {filename}")
                exported_count += 1

        # Create index file
        index_path = output_path / "README.md"
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(f"# Subsplash Notes Export\n\n")
            f.write(f"Exported on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total notes: {exported_count}\n\n")
            f.write(f"## Collections\n\n")
            for collection_name, notes in collections.items():
                f.write(f"### {collection_name} ({len(notes)} notes)\n\n")
                for note in notes:
                    title = note.get("title", "Untitled")
                    subtitle = note.get("subtitle", "")
                    if subtitle:
                        filename = f"{title} - {subtitle}.md"
                    else:
                        filename = f"{title}.md"
                    filename = sanitize_filename(filename)
                    f.write(f"- [{title}]({sanitize_filename(collection_name)}/{filename})\n")
                f.write("\n")

        print(f"\n[SUCCESS] Exported {exported_count} notes to '{output_dir}'")
        print(f"Notes are organized by collection in subfolders")
        print(f"See README.md for an index of all notes")

        return True

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Error fetching notes: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status: {e.response.status_code}")
            print(f"Response body: {e.response.text[:500]}")
        return False


def main():
    print("=" * 60)
    print("Subsplash Notes Exporter")
    print("=" * 60)
    print()

    print("To get your Bearer token and app key:")
    print("1. Open https://notes.subsplash.com in your browser (while logged in)")
    print("2. Open DevTools (F12)")
    print("3. Go to Network tab")
    print("4. Refresh the page")
    print("5. Find a request to 'pages/list'")
    print("6. Look in Request Headers for 'authorization: Bearer ...'")
    print("7. Copy everything AFTER 'Bearer ' (the long JWT token)")
    print("8. In the same request, look at Query String Parameters for 'appKey'")
    print()

    bearer_token = input("Paste your Bearer token here: ").strip()

    if not bearer_token:
        print("[ERROR] No token provided. Exiting.")
        return

    # Remove 'Bearer ' prefix if user included it
    if bearer_token.startswith('Bearer '):
        bearer_token = bearer_token[7:]

    print()
    app_key = input("Paste your app key here: ").strip()

    if not app_key:
        print("[ERROR] No app key provided. Exiting.")
        return

    print()
    output_dir = input("Output directory (default: subsplash_notes): ").strip()
    if not output_dir:
        output_dir = "subsplash_notes"

    print()
    export_notes(bearer_token, app_key=app_key, output_dir=output_dir)


if __name__ == "__main__":
    main()
