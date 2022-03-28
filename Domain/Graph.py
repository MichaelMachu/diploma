import matplotlib as matplb
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.collections import LineCollection
import numpy as np
from typing import List

class Graph:

    def __init__(self, figName: str = None):
        self.figName = figName
        #self.fig = plt.figure(figName)
        self.fig, self.ax = plt.subplots()
        self.fig.suptitle(figName)
        #self.ax = self.fig.add_subplot()

    def __set_name(self):
        self.ax.set_title(self.figName)

    def refresh(self):
        self.ax.clear()
        self.__set_name()

    # Draw bifurcation diagram
    def draw_bifurcation_diagram(self, data: List[dict], size: int = 1, colorDeterminism: str = "#00ff00", colorChaotic: str = "#ff0000") -> None:
        for item in data:
            #colors = [colorChaotic if k > 0.9 else colorDeterminism for k in item["kk"]]
            color = colorChaotic if item["k"] > 0.9 else colorDeterminism
            self.ax.scatter(item["xx"], item["yy"], s=size, c=color) # item["colors"]

    def draw_iteration(self, data, colorDeterminism: str = "#00ff00", colorChaotic: str = "#ff0000"): # xx, yy, kk
        colors = []
        segments = []
        for item in data:
            color = colorChaotic if item["k"] > 0.5 else colorDeterminism
            colors.append(color)
            segments.append(item["segment"])

        lineCollection = LineCollection(segments, colors=colors)
        self.ax.add_collection(lineCollection)
        self.ax.autoscale_view()

    def close(self) -> None:
        plt.close()