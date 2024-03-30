import asyncio
from dataclasses import dataclass
from common import canvas, ctx, put_points
import numpy as np
import random

@dataclass
class ChaosConfig:
    vert_x: np.ndarray | list[float]
    vert_y: np.ndarray | list[float]
    w_pt: float = 1
    w_vert: float = 1
    side_centers: bool = False
    figure_center: bool = False
    
    def __post_init__(self):
        assert len(self.vert_x) == len(self.vert_y)
        orig_num_vertices = len(self.vert_x)
        if self.side_centers:
            for i in range(orig_num_vertices):
                j = (i + 1) % orig_num_vertices
                self.vert_x.append((self.vert_x[i] + self.vert_x[j]) / 2)
                self.vert_y.append((self.vert_y[i] + self.vert_y[j]) / 2)
        if self.figure_center:
            self.vert_x.append(sum(self.vert_x) / orig_num_vertices)
            self.vert_y.append(sum(self.vert_y) / orig_num_vertices)
        self.vert_x = np.array(self.vert_x) * canvas.width
        self.vert_y = np.array(self.vert_y) * canvas.height
        self.num_vertices = len(self.vert_x)
            

async def draw_sierpinsky(cfg: ChaosConfig, *, num_points=10000, num_iterations=100):
    image_data = ctx.createImageData(canvas.width, canvas.height)
    x, y = None, None
    for i in range(num_iterations):
        vert_idx = np.random.randint(0, cfg.num_vertices, num_points)
        attr_x, attr_y = cfg.vert_x[vert_idx], cfg.vert_y[vert_idx]
        if i == 0:
            x, y = attr_x, attr_y
        else: 
            w_denom = cfg.w_pt + cfg.w_vert
            x, y = (cfg.w_pt * x + cfg.w_vert * attr_x) / w_denom, (cfg.w_pt * y + cfg.w_vert * attr_y) / w_denom
        put_points(image_data, x, y)
        ctx.putImageData(image_data, 0, 0)
        await asyncio.sleep(0)

asyncio.ensure_future(draw_sierpinsky(random.choice([
    ChaosConfig([0, .5, 1],   [1,  0, 1]),  # Triangle
    ChaosConfig([0, 0, 1, 1], [0, 1, 1, 0], w_vert=2, side_centers=True),   # Carpet
    ChaosConfig([0, 0, 1, 1], [0, 1, 1, 0], w_vert=2, figure_center=True),  # Vicsek
    # TODO: Other restrictions re: vertex choice
    # TODO: Initialize vertices as a regular polygon
])))
