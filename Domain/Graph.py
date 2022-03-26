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

    # Draw bifurcation diagram
    def draw_bifurcation_diagram(self, data: List[dict], size: int = 1, colorDeterminism: str = "#00ff00", colorChaotic: str = "#ff0000") -> None:
        for item in data:
            #colors = [colorChaotic if k > 0.9 else colorDeterminism for k in item["kk"]]
            color = colorChaotic if item["k"] > 0.9 else colorDeterminism
            self.ax.scatter(item["xx"], item["yy"], s=size, c=color) # item["colors"]

    def draw(self, data, colors): # xx, yy, kk
        #self.ax.plot(xx, yy, c=kk)
        #i = 0
        #for item in data:
        #    self.ax.plot(xx, yy, c=kk)

        lineCollection = LineCollection(data, colors=colors) # colors=colors    cmap=plt.cm.gist_ncar
        self.ax.add_collection(lineCollection)
        self.ax.autoscale_view()

    def close(self) -> None:
        plt.close()