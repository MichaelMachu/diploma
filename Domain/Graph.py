import matplotlib as matplb
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from typing import List

class Graph:

    def __init__(self, figName: str = None):
        self.fig = plt.figure(figName)
        self.fig.suptitle(figName)
        self.ax = self.fig.add_subplot()

    # Draw bifurcation diagram
    def draw_bifurcation_diagram(self, data: List[dict], size: int = 1, colorDeterminism: str = "#00ff00", colorChaotic: str = "#ff0000") -> None:
        for item in data:
            #colors = [colorChaotic if k > 0.9 else colorDeterminism for k in item["kk"]]
            color = colorChaotic if item["k"] > 0.9 else colorDeterminism
            self.ax.scatter(item["xx"], item["yy"], s=size, c=color) # item["colors"]

    def close(self) -> None:
        plt.close()