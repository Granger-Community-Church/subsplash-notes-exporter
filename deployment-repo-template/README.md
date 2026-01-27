# Subsplash Notes Viewer - Deployment

Static deployment of Subsplash notes with basic authentication for team access.

## Deployment

Deployed on Vercel with native Edge Middleware for basic authentication (no framework dependencies).

### Environment Variables

Set these in Vercel project settings (Settings → Environment Variables):

- `AUTH_USERNAME` - Username for basic auth
- `AUTH_PASSWORD` - Password for basic auth (use a strong password, 16+ characters)

### Initial Setup

1. Create this repository as **private** on GitHub
2. Copy files from the tooling repo:
   - `dist/index.html` → `index.html`
   - `dist/notes_index.json` → `notes_index.json`
   - All files from `deployment-repo-template/` to root
3. Commit and push to GitHub
4. Import project to Vercel
5. Set Framework Preset: "Other"
6. Configure environment variables (AUTH_USERNAME and AUTH_PASSWORD)
7. Deploy

### Local Development

```bash
vercel env pull .env.local  # Pull environment variables (optional)
python -m http.server 8000   # Simple local server at http://localhost:8000
# Note: Local testing won't have authentication (middleware runs only on Vercel)
```

### Updating Content

When notes are updated in the main tooling repository:

1. In the tooling repo, run:
   ```bash
   python subsplash_exporter.py        # Export new notes
   python build_for_deployment.py      # Build static files
   ```

2. Copy the built files to this repo:
   ```bash
   cp ../subsplash-notes-exporter/dist/index.html .
   cp ../subsplash-notes-exporter/dist/notes_index.json .
   ```

3. Commit and push (Vercel will auto-deploy):
   ```bash
   git add index.html notes_index.json
   git commit -m "Update notes content - $(date +%Y-%m-%d)"
   git push
   ```

Vercel will automatically deploy the changes in ~30 seconds.

## Security

- This repo contains exported notes content (committed to git)
- **Keep this repository private** - it contains all your notes
- Basic auth credentials are stored only in Vercel environment variables
- Edge middleware runs on every request for authentication
- All traffic is encrypted via HTTPS (Vercel provides free SSL)

## Files

- `index.html` - Main viewer application
- `notes_index.json` - All notes with embedded markdown content (~2-5MB)
- `middleware.js` - Native Edge Middleware for basic authentication (no dependencies)
- `package.json` - Minimal package config for ES modules
- `vercel.json` - Vercel configuration

## Troubleshooting

**Auth not working:**
- Verify AUTH_USERNAME and AUTH_PASSWORD are set in Vercel environment variables
- Check that variables are applied to Production environment
- Redeploy after changing environment variables

**Notes not loading:**
- Verify notes_index.json is present and contains the "content" field
- Check browser console for errors
- Verify the file was generated with the updated generate_index.py

**Build fails:**
- Verify package.json is present
- Check that Next.js dependency is specified
- Review Vercel build logs for specific errors
