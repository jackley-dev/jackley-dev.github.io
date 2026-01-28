import os
import argparse
from PIL import Image, ImageDraw, ImageFont

# --- Configuration ---
WIDTH = 1080
MAX_HEIGHT = 1440 # 3:4 aspect ratio
PADDING = 90
BG_COLOR = "#FDFDFD"  # Off-white paper look
TEXT_COLOR = "#1F1F1F" # Soft Black
TITLE_COLOR = "#000000"
H2_COLOR = "#000000"
FOOTER_COLOR = "#888888"
FONT_PATH = "/System/Library/Fonts/Supplemental/Songti.ttc"

# Optimized for 1080px width (Approx. 20 chars per line for body)
TITLE_FONT_SIZE = 120
H2_FONT_SIZE = 70
H3_FONT_SIZE = 40
BODY_FONT_SIZE = 40
FOOTER_FONT_SIZE = 30

LINE_SPACING_RATIO = 1.6 # Tighter line spacing like the screenshot
PARAGRAPH_SPACING_RATIO = 0.6 # Spacing between paragraphs
H2_SPACING_RATIO = 1.4 # Spacing before H2
H3_SPACING_RATIO = 1.2 # Spacing before H3

# Font Indices based on check_font.py
# Index 0: ('Songti SC', 'Black')
# Index 1: ('Songti SC', 'Bold')
# Index 4: ('STSong', 'Regular')
TITLE_FONT_INDEX = 1
H2_FONT_INDEX = 1 # Bold for H2
H3_FONT_INDEX = 1 # Bold for H3
BODY_FONT_INDEX = 4

def get_font(size, index):
    try:
        return ImageFont.truetype(FONT_PATH, size, index=index)
    except Exception as e:
        print(f"Warning: Could not load font at index {index}. Using default. Error: {e}")
        return ImageFont.load_default()

def wrap_text(text, font, max_width):
    """
    Wraps text character by character to fit max_width.
    Handles Chinese characters correctly by checking pixel width.
    """
    lines = []
    current_line = ""

    for char in text:
        # Check width of current line + char
        test_line = current_line + char
        bbox = font.getbbox(test_line)
        w = bbox[2] - bbox[0]

        if w <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = char

    if current_line:
        lines.append(current_line)

    return lines

def generate_cards(title, body, output_prefix="output"):
    # 1. Setup Fonts
    title_font = get_font(TITLE_FONT_SIZE, TITLE_FONT_INDEX)
    h2_font = get_font(H2_FONT_SIZE, H2_FONT_INDEX)
    h3_font = get_font(H3_FONT_SIZE, H3_FONT_INDEX)
    body_font = get_font(BODY_FONT_SIZE, BODY_FONT_INDEX)
    footer_font = get_font(FOOTER_FONT_SIZE, BODY_FONT_INDEX)

    content_width = WIDTH - (PADDING * 2)

    # 2. Process Title
    title_raw_lines = title.split('\\n')
    if len(title_raw_lines) == 1:
        title_raw_lines = title.split('\n')

    title_lines = []
    for raw_line in title_raw_lines:
        title_lines.extend(wrap_text(raw_line, title_font, content_width))

    # 3. Process Body
    body_paragraphs = body.split('\\n') if '\\n' in body else body.split('\n')

    # List of (text, type) where type is 'body', 'h2', 'break'
    final_body_lines = []

    for para in body_paragraphs:
        stripped = para.strip()
        if stripped == "":
            continue

        if stripped.startswith("###"):
            # It's a header 3
            text = stripped.lstrip("#").strip()
            lines = wrap_text(text, h3_font, content_width)
            for line in lines:
                final_body_lines.append((line, 'h3'))
        elif stripped.startswith("##"):
            # It's a header 2
            text = stripped.lstrip("#").strip()
            lines = wrap_text(text, h2_font, content_width)
            for line in lines:
                final_body_lines.append((line, 'h2'))
        else:
            # Body text
            # Remove bold markers **
            text = para.replace("**", "")
            lines = wrap_text(text, body_font, content_width)
            for line in lines:
                final_body_lines.append((line, 'body'))

        final_body_lines.append(("", 'break')) # Paragraph break

    if final_body_lines and final_body_lines[-1][1] == 'break':
        final_body_lines.pop()

    # 4. Calculate Dimensions & Layout Pages

    # Metrics
    def get_line_height(font, ratio=1.0):
        bbox = font.getbbox("Hg")
        base_h = bbox[3] - bbox[1]
        return base_h * ratio

    title_line_height = get_line_height(title_font, 1.3)
    h2_line_height = get_line_height(h2_font, 1.4)
    h3_line_height = get_line_height(h3_font, 1.4)
    body_line_height = get_line_height(body_font, LINE_SPACING_RATIO)
    body_base_height = get_line_height(body_font, 1.0) # For breaks

    title_body_gap = 120

    # Pagination Loop
    pages = [] # List of list of elements: {'text', 'font', 'x', 'y', 'color'}
    current_page = []
    current_y = PADDING

    # -- Title (Always on Page 1) --
    for line in title_lines:
        current_page.append({
            'text': line,
            'font': title_font,
            'x': PADDING,
            'y': current_y,
            'color': TITLE_COLOR
        })
        current_y += title_line_height

    current_y += title_body_gap

    # -- Body --
    for i, (text, type) in enumerate(final_body_lines):
        line_h = 0
        font = None
        color = TEXT_COLOR

        if type == 'break':
            # Check next item type
            next_type = final_body_lines[i+1][1] if i + 1 < len(final_body_lines) else 'body'
            if next_type == 'h2':
                # More space before H2
                line_h = body_base_height * H2_SPACING_RATIO
            elif next_type == 'h3':
                # More space before H3
                line_h = body_base_height * H3_SPACING_RATIO
            else:
                line_h = body_base_height * PARAGRAPH_SPACING_RATIO
        elif type == 'h2':
            line_h = h2_line_height
            font = h2_font
            color = H2_COLOR
        elif type == 'h3':
            line_h = h3_line_height
            font = h3_font
            color = H2_COLOR # Use same color as H2 for now
        else: # body
            line_h = body_line_height
            font = body_font
            color = TEXT_COLOR

        # Check bounds
        # Reserve space for footer if we might need pagination (approx 60px)
        if current_y + line_h + PADDING + 60 > MAX_HEIGHT:
            # Push current page
            pages.append(current_page)
            current_page = []
            current_y = PADDING # Reset to top

            # If the first thing on a new page is a paragraph break, skip it
            if type == 'break':
                continue

        if type != 'break':
            current_page.append({
                'text': text,
                'font': font,
                'x': PADDING,
                'y': current_y,
                'color': color
            })

        current_y += line_h

    # Push last page
    if current_page:
        pages.append(current_page)

    # 5. Render
    # If only 1 page, use actual height (adaptive)
    # If > 1 page, use fixed MAX_HEIGHT for uniformity

    is_multipage = len(pages) > 1

    output_base, output_ext = os.path.splitext(output_prefix)

    for i, elements in enumerate(pages):
        page_num = i + 1

        if is_multipage:
            img_height = MAX_HEIGHT
        else:
            # Calculate actual used height
            # Last element y + line_height + PADDING
            if elements:
                last_el = elements[-1]
                # Re-calculate height of last element roughly
                h = body_line_height if last_el['font'] == body_font else title_line_height
                img_height = int(last_el['y'] + h + PADDING)
            else:
                img_height = MAX_HEIGHT

        img = Image.new('RGB', (WIDTH, img_height), color=BG_COLOR)
        draw = ImageDraw.Draw(img)

        # Draw Elements
        for el in elements:
            draw.text((el['x'], el['y']), el['text'], font=el['font'], fill=el['color'])

        # Draw Footer (Page Number) if multipage
        # if is_multipage:
        #     footer_text = f"{page_num} / {len(pages)}"
        #     # Center footer
        #     f_bbox = footer_font.getbbox(footer_text)
        #     f_width = f_bbox[2] - f_bbox[0]
        #     f_x = (WIDTH - f_width) / 2
        #     f_y = img_height - PADDING + 10 # Slightly below content area, inside padding?
        #     # Actually PADDING is usually margin. Let's put it at bottom margin area.
        #     f_y = img_height - (PADDING / 1.5)
        #
        #     draw.text((f_x, f_y), footer_text, font=footer_font, fill=FOOTER_COLOR)

        # Save
        if is_multipage:
            filename = f"{output_base}_{page_num}{output_ext}"
        else:
            filename = f"{output_base}{output_ext}"

        img.save(filename)
        print(f"✅ Generated card: {filename} ({WIDTH}x{img_height})")

def main():
    parser = argparse.ArgumentParser(description="Generate Xiaohongshu style text card.")
    parser.add_argument("--title", "-t", required=True, help="Title text")
    parser.add_argument("--body", "-b", required=False, help="Body text (or use --file)")
    parser.add_argument("--file", "-f", help="Read body from text file")
    parser.add_argument("--output", "-o", default="xhs_card.png", help="Output filename")

    args = parser.parse_args()

    body_text = args.body
    if args.file:
        if os.path.exists(args.file):
            with open(args.file, 'r', encoding='utf-8') as f:
                body_text = f.read()
        else:
            print(f"Error: File {args.file} not found.")
            return

    if not body_text:
        print("Error: Must provide body text via --body or --file")
        return

    generate_cards(args.title, body_text, args.output)

if __name__ == "__main__":
    main()
