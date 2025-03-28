from PIL import Image
import numpy as np

image = Image.open("C:/Users/vinir/Pictures/Screenshots/Captura de tela 2025-03-28 152527.png")

# image.show()
image.thumbnail((512, 512))
data_rgba = image.getdata().convert("RGBA") # talvez precise converter para rgba com o convert
new_data = []
transparent = (0, 0, 0, 0)
pink = np.array([247, 0, 255]) # rosa choque
for pixel in data_rgba:
    # rgb(129, 28, 132)
    dist_color = np.linalg.norm(pink - pixel[:3])
    # print(dist_color)
    if dist_color < 190:
        new_data.append(transparent)
    else:
        new_data.append(pixel)

image.putdata(new_data)
image.show()

