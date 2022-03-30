from types import MethodType
from copy import deepcopy
from .Interval import Interval

class Individual:

    def __init__(self, coordinates: list, f: float = None, generateBest: bool = False) -> None:
        self.coordinates = coordinates
        self.f = f
        self.v = [0] * len(coordinates)
        self.pBest = None
        self.pBestf = None

        if generateBest:
            self.GeneratepBest()

    # Provede výpočet na konkrétni funkci
    def CalculateF(self, func: MethodType) -> None:
        self.f = func(self.coordinates)

    # Výpočet vektoru "v" pro směr nového bodu, samotná funkce kontroluje rychlost na základě získaného rozsahu velocity
    def CalculateV(self, c_1: float, c_2: float, r_1: float, r_2: float, gBest: "Individual", velocity: list, interval: Interval) -> None:
        length = len(self.v)
        for i in range(length):
            self.v[i] = self.v[i] + r_1 * c_1 * (self.pBest[i] - self.coordinates[i]) + r_2 * c_2 * (gBest.pBest[i] - self.coordinates[i])
            if self.v[i] < velocity[0]:
                self.v[i] = velocity[0]
            elif self.v[i] > velocity[1]:
                self.v[i] = velocity[1]

    # Vygeneruje nejlepší nalezený bod
    def GeneratepBest(self) -> None:
        if self.pBest is None:
            self.pBest = deepcopy(self.coordinates)
            self.pBestf = self.f