#!/usr/bin/env python3
import os
import sys
import glob
import json
import re

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DRAFTS_DIR = os.path.join(BASE_DIR, "../../xhs_drafts")
IMAGES_DIR = os.path.join(DRAFTS_DIR, "image")

def get_latest_post():
    # Find all _summary.md files in xhs_drafts
    # We prioritize summary files because that's what we publish from
    files = glob.glob(os.path.join(DRAFTS_DIR, "*_summary.md"))
    if not files:
        return None
    # Sort by modification time, newest first
    files.sort(key=os.path.getmtime, reverse=True)
    return files[0]

def parse_post(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.strip().split('\n')
    title = "Untitled"
    
    if lines and lines[0].startswith("# "):
        title = lines[0].replace("# ", "").strip()
    
    # The whole content of the summary file is the caption (except maybe the title line)
    # But usually summary file includes title at top? 
    # Let's assume the user edits the summary file to be exactly what they want in the caption.
    # However, usually we want the title separate for the XHS title field.
    
    summary_content = content.strip()
    
    # If the first line is a header, treat it as title and the rest as description
    if lines and lines[0].startswith("# "):
        summary_content = "\n".join(lines[1:]).strip()
        
    return title, summary_content

def find_images(summary_basename):
    # Summary basename: {slug}_summary.md -> {slug}
    base_name = summary_basename.replace("_summary.md", "")

    # Pattern: {base_name}_*.png
    # But specifically looking for the sequence generated: _1.png, _2.png, etc.
    # Or just all starting with base_name

    pattern = os.path.join(IMAGES_DIR, f"{base_name}_*.png")
    images = glob.glob(pattern)

    # Sort carefully: _1.png < _2.png < _10.png
    # Extract number from filename
    def sort_key(filepath):
        filename = os.path.basename(filepath)
        # Try to find the number at the end
        match = re.search(r'_(\d+)\.png$', filename)
        if match:
            return int(match.group(1))
        return 0

    images.sort(key=sort_key)
    return images

def main():
    post_path = get_latest_post()
    if not post_path:
        print(json.dumps({"error": "No drafts found"}))
        sys.exit(1)

    post_filename = os.path.basename(post_path)
    title, body = parse_post(post_path)
    images = find_images(post_filename)

    result = {
        "title": title,
        "content": body,
        "images": images,
        "source_file": post_path
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
