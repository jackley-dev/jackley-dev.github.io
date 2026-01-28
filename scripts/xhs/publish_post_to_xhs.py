#!/usr/bin/env python3
import os
import sys
import glob
import re
from pathlib import Path

# Add the script directory to path to import text_card_generator
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

import text_card_generator

CONTENT_DIR = os.path.join(current_dir, "../../xhs_drafts")
# Output images to xhs_drafts/image folder
STATIC_IMG_DIR = os.path.join(CONTENT_DIR, "image")

def get_latest_post():
    # Find all .md files in xhs_drafts
    files = glob.glob(os.path.join(CONTENT_DIR, "*.md"))
    if not files:
        return None
    # Sort by modification time, newest first
    files.sort(key=os.path.getmtime, reverse=True)
    return files[0]

def parse_front_matter(content):
    # Since XHS drafts are simple markdown, we assume first line is title (# Title)
    lines = content.strip().split('\n')
    title = "Untitled"
    body_content = content

    if lines and lines[0].startswith("# "):
        title = lines[0].replace("# ", "").strip()
        body_content = "\n".join(lines[1:]).strip()
    
    return title, body_content

def clean_body(body):
    # Remove some common markdown artifacts if needed
    # For now, just return as is, the generator handles basic markdown
    return body

def main():
    # Ensure output directory exists
    if not os.path.exists(STATIC_IMG_DIR):
        os.makedirs(STATIC_IMG_DIR)

    post_path = get_latest_post()
    if not post_path:
        print("Error: No blog posts found.")
        sys.exit(1)

    print(f"Processing latest post: {post_path}")

    with open(post_path, 'r', encoding='utf-8') as f:
        content = f.read()

    title, body = parse_front_matter(content)
    cleaned_body = clean_body(body)

    # Generate filename based on post filename
    post_filename = os.path.basename(post_path)
    base_name = os.path.splitext(post_filename)[0]
    output_path = os.path.join(STATIC_IMG_DIR, f"{base_name}.png")

    print(f"Generating cards for: {title}")
    text_card_generator.generate_cards(title, cleaned_body, output_path)

if __name__ == "__main__":
    main()
