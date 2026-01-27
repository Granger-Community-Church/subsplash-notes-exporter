# Subsplash Notes Exporter

A Python tool to export all your notes from [notes.subsplash.com](https://notes.subsplash.com) to local markdown files.

## Features

- ✅ Exports all notes with a single command
- ✅ Organizes notes by collection into folders
- ✅ Preserves all metadata (title, author, dates, etc.)
- ✅ Saves as markdown files with YAML frontmatter
- ✅ Creates an index with links to all notes
- ✅ No data loss - complete backup of your notes

## Quick Start

### 1. Set Up Virtual Environment (Recommended)

Create an isolated Python environment:

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Note:** You'll need to activate the venv each time you use the script. When activated, your terminal prompt will show `(venv)` at the beginning.

### 2. Get Your Bearer Token

Your Bearer token authenticates you with Subsplash. It's temporary and expires after ~10 minutes.

**Steps:**

1. Open [https://notes.subsplash.com](https://notes.subsplash.com) in your browser (while logged in)
2. Press `F12` to open DevTools
3. Go to the **Network** tab
4. Click the **Fetch/XHR** filter button
5. Refresh the page (`F5`)
6. Click on a request named `list` (URL contains `/pages/list`)
7. In the **Headers** section, find **Request Headers**
8. Copy the token from `authorization: Bearer ...` (everything **after** "Bearer ")

The token should start with `eyJ` and be several hundred characters long.

### 3. Run the Exporter

```bash
python subsplash_exporter.py
```

Follow the prompts to:
- Paste your Bearer token
- Choose output directory (default: `subsplash_notes`)

### 4. Browse Your Notes (Web Viewer)

After exporting, you can use the included web viewer to browse your notes:

```bash
# Generate the index for the viewer
python generate_index.py

# Start the web viewer
python start_viewer.py
```

The viewer will:
- Open automatically in your browser at `http://localhost:8000/viewer/`
- Display all notes in a table similar to Subsplash
- Provide search and filter functionality
- Allow you to view individual notes with rendered markdown
- Work completely offline

**Note:** The viewer requires running a local web server due to browser security restrictions when loading local files.

## Output Structure

```
subsplash_notes/
├── README.md                                  # Index of all notes
├── Stuck/                                     # Collection folder
│   ├── Discussion Questions - Week 4.md
│   ├── Unstuck and on Mission - October 25_26, 2025.md
│   └── ...
├── Another Collection/
│   ├── Note 1.md
│   └── Note 2.md
└── Uncategorized/
    └── ...
```

## Note Format

Each note is saved as a markdown file with YAML frontmatter:

```markdown
---
title: Unstuck and on Mission
subtitle: October 25/26, 2025
author: John Keim
date: 2025-10-22T19:15:00.000Z
collection: Stuck
color: #5B4336
created: 2025-10-22T19:14:09.000Z
updated: 2025-11-03T16:18:27.638Z
note_id: 68f92d0136414809d17da11b
hid: SyF-TiURll
---

[Your full note content in markdown format...]
```

## Troubleshooting

### "401 Unauthorized" or "Token expired"
- Your token expires after ~10 minutes of inactivity
- Get a fresh token using the steps above

### "Module 'requests' not found"
- Make sure your virtual environment is activated (look for `(venv)` in your prompt)
- If not using venv: `pip install requests`
- If using venv: Activate it first, then the module should be available

### No notes exported
- Verify you copied the **entire** token (it's very long)
- Make sure you're copying from the `authorization` header, not cookies
- Confirm you're logged into Subsplash in the browser

### Viewer not loading
- Make sure you ran `python generate_index.py` after exporting notes
- Ensure the local server is running (`python start_viewer.py`)
- Try accessing `http://localhost:8000/viewer/` directly in your browser
- Check that the `viewer/notes_index.json` file exists

## Web Viewer

The included web viewer provides a Subsplash-like interface to browse your exported notes locally.

### Features

- **Search** - Find notes by title, subtitle, author, or collection
- **Filter by Collection** - Show notes from specific collections only
- **Responsive Design** - Works on desktop and mobile browsers
- **Markdown Rendering** - View notes with proper formatting
- **Offline** - Works completely offline once loaded
- **Fast** - All notes indexed for instant searching

### How It Works

1. `generate_index.py` scans your exported notes and creates a JSON index
2. `start_viewer.py` starts a local web server on port 8000
3. Your browser loads the viewer at `http://localhost:8000/viewer/`
4. The viewer fetches the index and displays your notes
5. Click any note to view its full content with rendered markdown

### Using a Different Port

If port 8000 is already in use, you can edit `start_viewer.py` and change:

```python
PORT = 8000  # Change to any available port
```

## Use Cases

After exporting, you can:
- **Backup** - Keep a local copy of your notes
- **Search** - Use file system search across all notes
- **Import** - Move notes to other apps (Obsidian, Notion, etc.)
- **Version Control** - Track changes with Git
- **Cloud Storage** - Sync to Dropbox, Google Drive, etc.

## Technical Details

- **Language**: Python 3.7+
- **Dependencies**: `requests` library only
- **Authentication**: JWT Bearer token from browser session
- **API**: Uses the same endpoints as the Subsplash web app
- **Read-only**: Does not modify or delete anything on Subsplash

## Security Notes

- Your Bearer token is like a temporary password - don't share it
- Tokens expire automatically after ~10 minutes
- The script doesn't store your token anywhere
- You're accessing your own paid data

## Publishing to GitHub

If you fork or publish this project, ensure you don't commit your personal data:

**Protected by `.gitignore`:**
- `subsplash_notes/` - Your exported notes
- `viewer/notes_index.json` - Index containing note metadata and previews
- `venv/` - Python virtual environment

**Never commit:**
- Bearer tokens (these expire after ~10 minutes anyway)
- Any personal notes or content

The app key is visible in browser network requests to notes.subsplash.com when you're logged in. It's specific to your organization's Subsplash account.

## License

This is a personal backup tool for accessing your own data. Use responsibly.
