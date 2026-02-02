from PIL import ImageFont

FONT_PATH = "/System/Library/Fonts/Supplemental/Songti.ttc"
SIZE = 40

def check_metrics(index, name):
    try:
        font = ImageFont.truetype(FONT_PATH, SIZE, index=index)
        ascent, descent = font.getmetrics()
        print(f"{name} (Index {index}): Ascent={ascent}, Descent={descent}, Total={ascent+descent}")
        bbox = font.getbbox("Hg")
        print(f"  bbox 'Hg': {bbox}")
    except Exception as e:
        print(f"Error loading index {index}: {e}")

check_metrics(4, "STSong Regular")
check_metrics(1, "Songti SC Bold")
