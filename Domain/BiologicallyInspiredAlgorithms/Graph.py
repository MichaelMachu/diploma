from types import MethodType
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np

from .Interval import Interval
from .Individual import Individual

class Graph:

    # Konstruktor třídy Graph nastavuje základní hodnoty proměnných pro konstrukci vizualizace grafu
    def __init__(self, figName: str = None, func: MethodType = None, interval: Interval = None) -> None:
        self.figName = figName
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.func = func
        self.interval = interval
        self.animation = None

    def __set_name(self) -> None:
        self.ax.set_title(self.figName)

    def refresh(self) -> None:
        self.animation = None
        self.ax.clear()
        self.__set_name()

    def close(self) -> None:
        plt.close()

    # Zobrazení grafu
    def Show(self, points: list = None, points_history: list = None, interval_anim: int = 1) -> None:
        # Sestavení bodů pro x a y skrze interval s následným vytvořením meshgridu
        x = y = np.arange(self.interval.lowerBound, self.interval.upperBound, self.interval.step)
        x, y = np.meshgrid(x, y)
        # Vytvoření křivky grafu dané funkce
        z = np.array([self.func([x, y]) for x, y in zip(np.ravel(x), np.ravel(y))])
        z = z.reshape(x.shape)

        # Sestavení grafu pomocí souřadnic
        self.ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap=plt.get_cmap('jet'), alpha=0.3)

        # Pojmenování grafu a jednotlivých os
        self.ax.set_title(self.figName)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')

        # Cesta bodů v animaci
        self.path = None
        # Body, které se budou animovat (historie průchodu)
        self.points_to_anim = points_history

        # Vykreslení animace
        # => vykreslená historie průchodu je zobrazena červeně
        if self.points_to_anim != None:
            self.animation = FuncAnimation(self.fig, self.anim, len(self.points_to_anim), interval=interval_anim, blit=False, repeat=False)

        # Vykreslení bodů získaných z vyhledávacího algoritmu
        # => výsledné body jsou vykresleny zeleně
        if points != None:
            for point in points:
                self.ax.scatter3D(point.x, point.y, point.z, c = '#00ff00')

        #plt.show()

    # Zobrazení grafu včetně vykreslení historie průchodu celé populace
    def ShowByPopulation(self, best_individual: Individual = None, population_history: list = None, interval_anim: int = 1) -> None:
        # Sestavení bodů pro x a y skrze interval s následným vytvořením meshgridu
        x = y = np.arange(self.interval.lowerBound, self.interval.upperBound, self.interval.step)
        x, y = np.meshgrid(x, y)
        # Vytvoření křivky grafu dané funkce
        z = np.array([self.func([x, y]) for x, y in zip(np.ravel(x), np.ravel(y))])
        z = z.reshape(x.shape)

        # Sestavení grafu pomocí souřadnic
        self.ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap=plt.get_cmap('jet'), alpha=0.3)

        # Pojmenování grafu a jednotlivých os
        self.ax.set_title(self.figName)
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')

        # Cesta bodů v animaci
        self.path = []
        # Populace, která se budou animovat (historie průchodu)
        self.population_to_anim = population_history

        # Vykreslení animace
        # => vykreslená historie průchodu je zobrazena červeně
        if self.population_to_anim != None:
            self.animation = FuncAnimation(self.fig, self.animByPopulation, len(self.population_to_anim), interval=interval_anim, blit=False, repeat=False)

        # Vykreslení nejlepšího jedince získaného z vyhledávacího algoritmu
        # => výsledný jedinec je vykresleny zeleně
        if best_individual != None:
            self.ax.scatter3D(best_individual.coordinates[0], best_individual.coordinates[1], best_individual.f, c = '#00ff00')

        #plt.show()

    # Vykreslení animace
    def anim(self, n: int) -> None:
        # Pokud je již vykreslený přechozí bod, tak ho odstraň
        if self.path != None:
            self.path.remove()

        # Pokud existuje bod pro vykreslení, tak ho vykresli
        if self.points_to_anim != None:
            self.path = self.ax.scatter3D(self.points_to_anim[n].x, self.points_to_anim[n].y, self.points_to_anim[n].z, c = '#ff0000')

    def animByPopulation(self, n: int) -> None:
        # Pokud jsou již vykreslený předchozí body, tak ho odstraň
        if self.path:
            for i in range(len(self.path)):
                if self.path[i]:
                    self.path[i].remove()
            self.path.clear()

        # Pokud existují body pro vykreslení, tak je vykresli
        if self.population_to_anim != None:
            for individual in self.population_to_anim[n].individuals:
                self.path.append(self.ax.scatter3D(individual.pBest[0], individual.pBest[1], individual.pBestf, c = '#ff0000'))
            
            # Slouží pouze pro vykreslení jen konkrétního jedince z populace
            #for i in range(len(self.population_to_anim[n].individuals)):
                #self.path.append(self.ax.scatter3D(self.population_to_anim[n].individuals[0].pBest[0], self.population_to_anim[n].individuals[0].pBest[1], self.population_to_anim[n].individuals[0].pBestf, c = '#ff0000'))
                #print(self.population_to_anim[n].individuals[0].pBestf)