#!/usr/bin/env python3
"""
Build static site for Vercel deployment
"""

import argparse
import shutil
import sys
from pathlib import Path
from generate_index import generate_index


def build_deployment(target_dir=None):
    """Build deployment files with embedded content

    Args:
        target_dir: Optional path to deployment repository to copy files to
    """

    # Generate index with full content
    print("Generating notes index with full content...")
    success = generate_index(
        notes_dir="subsplash_notes",
        output_file="dist/notes_index.json"
    )

    if not success:
        print("Failed to generate index. Make sure notes have been exported first.")
        return False

    # Create dist directory
    dist_path = Path("dist")
    dist_path.mkdir(exist_ok=True)

    # Copy viewer HTML (rename to index.html)
    print("Copying viewer files...")
    shutil.copy("viewer/index.html", "dist/index.html")

    print("\n✓ Build complete! Files ready in dist/")

    # Copy to deployment repository if target specified
    if target_dir:
        target_path = Path(target_dir)

        if not target_path.exists():
            print(f"\n❌ Error: Target directory does not exist: {target_dir}")
            print("Create the deployment repository first, then run this command again.")
            return False

        print(f"\nCopying files to deployment repository: {target_path}")

        # Copy built files
        print("  → Copying index.html...")
        shutil.copy("dist/index.html", target_path / "index.html")

        print("  → Copying notes_index.json...")
        shutil.copy("dist/notes_index.json", target_path / "notes_index.json")

        # Copy template files if they don't exist
        template_path = Path("deployment-repo-template")
        template_files = [
            "middleware.js",
            "package.json",
            "vercel.json",
            ".gitignore",
            "README.md"
        ]

        for filename in template_files:
            target_file = target_path / filename
            if not target_file.exists():
                source_file = template_path / filename
                if source_file.exists():
                    print(f"  → Copying {filename} (first time setup)...")
                    shutil.copy(source_file, target_file)

        print("\n✓ Files copied to deployment repository!")
        print("\nNext steps:")
        print(f"  cd {target_dir}")
        print("  git add .")
        print("  git commit -m 'Update notes - $(date +%Y-%m-%d)'")
        print("  git push")
    else:
        print("\nNext steps:")
        print("1. Copy dist/ contents to your deployment repository")
        print("2. Add middleware.ts, package.json, vercel.json (see deployment-repo-template/)")
        print("3. Commit and push to deploy on Vercel")
        print("\nTip: Run with --target-dir to automate copying:")
        print("  python3 build_for_deployment.py --target-dir ../subsplash-notes-viewer-deploy")

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Build static site for Vercel deployment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Build only (files in dist/)
  python3 build_for_deployment.py

  # Build and copy to deployment repo
  python3 build_for_deployment.py --target-dir ../subsplash-notes-viewer-deploy
  python3 build_for_deployment.py -t ~/repos/notes-deploy
"""
    )

    parser.add_argument(
        '--target-dir', '-t',
        help='Path to deployment repository (will copy files there)',
        type=str,
        default=None
    )

    args = parser.parse_args()

    success = build_deployment(target_dir=args.target_dir)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
