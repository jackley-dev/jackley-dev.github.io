#!/usr/bin/env python3
import os
import sys
import argparse
import re
import glob
from pathlib import Path

# Setup paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
POSTS_DIR = os.path.join(PROJECT_ROOT, "content/posts")
XHS_DIR = os.path.join(PROJECT_ROOT, "xhs_drafts")

def get_latest_post():
    files = glob.glob(os.path.join(POSTS_DIR, "**/*.md"), recursive=True)
    if not files:
        return None
    files.sort(key=os.path.getmtime, reverse=True)
    return files[0]

def clean_content(content):
    # 1. Remove TOML Front Matter (+++ ... +++)
    content = re.sub(r'^\+\+\+.*?\+\+\+', '', content, flags=re.DOTALL)

    # 2. Remove YAML Front Matter (--- ... ---)
    content = re.sub(r'^---.*?---', '', content, flags=re.DOTALL)

    # 3. Remove Hugo Shortcodes (e.g. {{< ... >}})
    content = re.sub(r'\{\{<.*?>\}\}', '', content)

    # 4. Remove Links but keep text [text](url) -> text
    content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)

    # 5. Trim whitespace
    return content.strip()

def main():
    parser = argparse.ArgumentParser(description="Convert a blog post to XHS draft.")
    parser.add_argument("file", nargs="?", help="Path to the blog post file (optional, defaults to latest)")
    args = parser.parse_args()

    source_path = args.file
    if not source_path:
        print("Finding latest post...")
        source_path = get_latest_post()

    if not source_path or not os.path.exists(source_path):
        print(f"Error: Post not found: {source_path}")
        sys.exit(1)

    print(f"Reading: {source_path}")

    with open(source_path, 'r', encoding='utf-8') as f:
        original_content = f.read()

    # Extract Title (Try to find title in front matter first)
    title = "Untitled"
    title_match = re.search(r'title\s*=\s*"(.*?)"', original_content)
    if not title_match:
         title_match = re.search(r'title:\s*"?([^"\n]+)"?', original_content)

    if title_match:
        title = title_match.group(1)

    # Clean Body
    body = clean_content(original_content)

    # Prepare Raw Content (Cleaned but not structured)
    raw_content = f"# {title}\n\n{body}"

    # Output Filename: {filename}.md
    filename = os.path.basename(source_path)
    output_filename = filename # Keep original filename
    output_path = os.path.join(XHS_DIR, output_filename)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(raw_content)

    print(f"✅ Cleaned content saved to: {output_path}")
    print(f"👉 Next Step: Generate summary and save to {os.path.splitext(output_filename)[0]}_summary.md")

if __name__ == "__main__":
    main()
