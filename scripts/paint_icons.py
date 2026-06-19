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

def save_icon(icon_path: Path, icon_image: Image, theme: str) -> None:
    parts = icon_path.parts
    index = parts.index("icons") + 1
    new_path = Path(*parts[:index], theme, *parts[index:])

    new_path.parent.mkdir(parents=True, exist_ok=True)
    icon_image.save(new_path)

def paint_icons():
    icons_to_paint = get_icons_to_paint()
    colors_map = {
        "dark": DARK_ICON_COLOR,
        "light": LIGHT_ICON_COLOR
    }

    for icon in icons_to_paint:
        img = Image.open(icon).convert("RGBA")
        img_data = np.array(img)

        mask = img_data[:,:, 3] != 0

        for theme, color in colors_map.items():
            img_data[mask] = color.to_rgba()

            painted_icon = Image.fromarray(img_data)
            save_icon(icon, painted_icon, theme)


if __name__ == "__main__":
    paint_icons()