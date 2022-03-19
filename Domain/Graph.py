import matplotlib as matplb
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

class Graph:

    def __init__(self, figName: str = None):
        self.fig = plt.figure(figName)
        self.fig.suptitle(figName)
        self.ax = self.fig.add_subplot()

    # Draw bifurcation diagram
    def draw_bifurcation_diagram(self, data: list[dict], size: int = 1) -> None:
        for item in data:
            self.ax.scatter(item["xx"], item["yy"], s=size, c=item["colors"])

        plt.show()