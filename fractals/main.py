import asyncio
import numpy as np
from pyodide.ffi import create_proxy
from pyscript import document, window

BYTES_PER_PIXEL = 4

canvas = document.getElementById("canvas")
ctx = canvas.getContext("2d")

def put_points(image_data, xs: np.ndarray, ys: np.ndarray):
    for x, y in zip(xs, ys):
        image_data.data[int(y) * image_data.width * BYTES_PER_PIXEL + int(x) * BYTES_PER_PIXEL + BYTES_PER_PIXEL - 1] = 255

async def draw_sierpinsky(vert_x: list[float], vert_y: list[float], *, num_points=10000, num_iterations=100):
    vert_x, vert_y = np.array(vert_x), np.array(vert_y)
    assert len(vert_x) == len(vert_y)
    image_data = ctx.createImageData(canvas.width, canvas.height)
    x, y = None, None
    for i in range(num_iterations):
        vert_idx = np.random.randint(0, len(vert_x), num_points)
        attr_x, attr_y = vert_x[vert_idx], vert_y[vert_idx]
        x, y = ((x + attr_x) / 2, (y + attr_y) / 2) if x is not None else (attr_x, attr_y)
        put_points(image_data, x, y)
        ctx.putImageData(image_data, 0, 0)
        await asyncio.sleep(0)

async def draw(*args):
    await draw_sierpinsky(
        [canvas.width      / 5, canvas.width  / 2, canvas.width  * 4 / 5],
        [canvas.height * 4 / 5, canvas.height / 5, canvas.height * 4 / 5])
    
asyncio.ensure_future(draw())    
