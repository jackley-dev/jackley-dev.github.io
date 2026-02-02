from fontTools.ttLib import TTCollection

font_path = "/System/Library/Fonts/Supplemental/Songti.ttc"
try:
    ttc = TTCollection(font_path)
    print(f"Number of fonts in TTC: {len(ttc)}")
    for i, font in enumerate(ttc):
        name_record = font['name'].getDebugName(4) # Full name
        print(f"Index {i}: {name_record}")
except Exception as e:
    print(f"Error: {e}")
