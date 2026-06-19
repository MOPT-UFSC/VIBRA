import os
from pathlib import Path

import numpy as np
from PIL import Image

from vibra import DARK_ICON_COLOR, DARK_ICONS_DIR, LIGHT_ICON_COLOR, LIGHT_ICONS_DIR

DIR_EXCEPTIONS = ["cursors", "figures", "logos", "model_setup_items", "__pycache__", "warnings"]
ICONS_EXTENSIONS = [".png"]
ICONS_DIRS = [DARK_ICONS_DIR, LIGHT_ICONS_DIR]
COLORS = [DARK_ICON_COLOR, LIGHT_ICON_COLOR]


def get_icons_to_paint(dir: Path) -> list[Path]:
    icons_to_paint = list()

    for dir_path, _, files in os.walk(os.path.abspath(dir)):
        last_folder = Path(dir_path).name

        if last_folder in DIR_EXCEPTIONS:
            continue

        for file in files:
            icon_path = Path(os.path.join(dir_path, file))

            if icon_path.suffix.lower() not in ICONS_EXTENSIONS:
                continue

            icons_to_paint.append(icon_path)

    return icons_to_paint


def save_icon(icon_path: Path, icon_image: Image) -> None:
    icon_path.parent.mkdir(parents=True, exist_ok=True)
    icon_image.save(icon_path)


def paint_icons():
    for dir, color in zip(ICONS_DIRS, COLORS):
        icons_to_paint = get_icons_to_paint(dir)

        for icon in icons_to_paint:
            img = Image.open(icon).convert("RGBA")
            img_data = np.array(img)

            mask = img_data[:, :, 3] != 0
            img_data[mask] = color.to_rgba()

            painted_icon = Image.fromarray(img_data)
            save_icon(icon, painted_icon)


if __name__ == "__main__":
    paint_icons()
