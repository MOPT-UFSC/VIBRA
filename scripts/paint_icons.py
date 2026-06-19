import os
import numpy as np

from pathlib import Path
from PIL import Image
from vibra import DARK_ICON_COLOR, ICON_DIR, LIGHT_ICON_COLOR


DIR_EXCEPTIONS = ["cursors", "figures", "logos", "model_setup_items", "__pycache__", "warnings"]
ICONS_EXTENSIONS = [".png"]


def get_icons_to_paint() -> list[Path]:
    icons_to_paint = list()

    for dir_path, _, files in os.walk(os.path.abspath(ICON_DIR)):
        last_folder = Path(dir_path).name
    
        if last_folder in DIR_EXCEPTIONS:
            continue

        for file in files:
            icon_path = Path(os.path.join(dir_path, file))

            if icon_path.suffix.lower() not in ICONS_EXTENSIONS:
                continue
            
            icons_to_paint.append(icon_path)
    
    return icons_to_paint

def paint_icons():
    icons_to_paint = get_icons_to_paint()

    for icon in icons_to_paint:

        img = Image.open(icon).convert("RGBA")
        img_data = np.array(img)
        
        for i in range(len(img_data)):
            for j in range(len(img_data[i])):
                rgba_color = img_data[i][j]

                if rgba_color[-1] == 0:
                    continue

                img_data[i][j] = DARK_ICON_COLOR.to_rgba()

        new_img = Image.fromarray(img_data)

if __name__ == "__main__":
    paint_icons()