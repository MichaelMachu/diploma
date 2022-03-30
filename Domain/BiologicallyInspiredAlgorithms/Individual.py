from copy import deepcopy

class Individual:

    def __init__(self, coordinates) -> None:
        self.coordinates = coordinates
        self.f = None
        self.v = [0] * len(coordinates)
        self.pBest = None
        self.pBestf = None

    # Provede výpočet na konkrétni funkci
    def CalculateF(self, func):
        self.f = func(self.coordinates)

    # Výpočet vektoru "v" pro směr nového bodu, samotná funkce kontroluje rychlost na základě získaného rozsahu velocity
    def CalculateV(self, c_1, c_2, r_1, r_2, gBest, velocity, interval):
        length = len(self.v)
        for i in range(length):
            self.v[i] = self.v[i] + r_1 * c_1 * (self.pBest[i] - self.coordinates[i]) + r_2 * c_2 * (gBest.pBest[i] - self.coordinates[i])
            if self.v[i] < velocity[0]:
                self.v[i] = velocity[0]
            elif self.v[i] > velocity[1]:
                self.v[i] = velocity[1]

    # Vygeneruje nejlepší nalezený bod
    def GeneratepBest(self):
        if self.pBest is None:
            self.pBest = deepcopy(self.coordinates)
            self.pBestf = self.f