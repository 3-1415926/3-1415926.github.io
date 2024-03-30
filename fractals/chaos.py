import asyncio
from common import canvas, ctx, put_points
import numpy as np

async def draw_sierpinsky(vert_x: list[float], vert_y: list[float], *, num_points=10000, num_iterations=100, w1=1, w2=1):
    vert_x, vert_y = np.array(vert_x) * canvas.width, np.array(vert_y) * canvas.height
    assert len(vert_x) == len(vert_y)
    image_data = ctx.createImageData(canvas.width, canvas.height)
    x, y = None, None
    for i in range(num_iterations):
        vert_idx = np.random.randint(0, len(vert_x), num_points)
        attr_x, attr_y = vert_x[vert_idx], vert_y[vert_idx]
        if i > 0:
            x, y = (w1 * x + w2 * attr_x) / (w1 + w2), (w1 * y + w2 * attr_y) / (w1 + w2)
        else:
            x, y = attr_x, attr_y
        put_points(image_data, x, y)
        ctx.putImageData(image_data, 0, 0)
        await asyncio.sleep(0)

asyncio.ensure_future(draw_sierpinsky(
    # [0, .5, 1], [1,  0, 1]  # Triangle
    [0, 0, 1, 1, .5,  1, .5, 0], [0, 1, 1, 0,  0, .5, 1, .5], w2=2  # Square
))
