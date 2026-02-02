from PIL import ImageFont

font_path = "/System/Library/Fonts/Supplemental/Songti.ttc"
for i in range(10):
    try:
        font = ImageFont.truetype(font_path, 40, index=i)
        # Try to get font name - PIL doesn't make this super easy directly from the object usually,
        # but let's see if we can infer or just print that it worked.
        # Actually, getname() returns a tuple (name, style)
        name = font.getname()
        print(f"Index {i}: {name}")
    except Exception as e:
        print(f"Index {i}: Failed ({e})")
