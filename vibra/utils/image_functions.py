from PIL import Image
import numpy as np


def removes_image_background(image: Image):
    image = image.convert("RGBA")
    data_rgba = image.getdata()
    new_data = []
    transparent = (255, 255, 255, 0)
    pink = np.array([247, 0, 255])

    for pixel in data_rgba:
        dist_color = np.linalg.norm(pink - pixel[:3])
        if dist_color < 190:
            new_data.append(transparent)
        else:
            new_data.append(pixel)

    image.putdata(new_data)
    return image
