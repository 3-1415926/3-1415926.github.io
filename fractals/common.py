import numpy as np
from pyscript import document

canvas = document.getElementById("canvas")
ctx = canvas.getContext("2d")

def put_points(image_data, xs: np.ndarray, ys: np.ndarray):
    BYTES_PER_PIXEL = 4
    for x, y in zip(xs, ys):
        image_data.data[int(y) * image_data.width * BYTES_PER_PIXEL + int(x) * BYTES_PER_PIXEL + BYTES_PER_PIXEL - 1] = 255
