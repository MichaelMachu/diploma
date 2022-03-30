import random
from types import MethodType
from operator import attrgetter
from .Individual import Individual
from .Interval import Interval

class Population:

    # Privátní promměná, která nabývá hodnoty true, pokud již jedinci byli ohodnoceni (kvůli výběru nejlepšího jedince)
    __individualsWereCalculated = False

    def __init__(self, interval: Interval = None, dimension: int = 0, individuals: list = []) -> None:
        self.interval = interval
        self.dimension = dimension
        self.individuals = individuals

    # Generuje náhodné hodnoty pro vyhledávání skrze hodnoty z intervalu a dimenze
    def GenerateIndividual(self) -> Individual:
        array = []

        for _ in range(self.dimension):  
            array.append(random.uniform(self.interval.lowerBound, self.interval.upperBound))
            
        individual = Individual(array)
        
        return individual

    # Vytvoření populace jedinců
    def GenerateIndividuals(self, number: int) -> None:
        if self.individuals:
            return

        for _ in range(number):
            self.individuals.append(self.GenerateIndividual())

    # Výpočet hodnot na funkci pro všechny jedince
    def CalculateIndividuals(self, func: MethodType) -> None:
        self.__individualsWereCalculated = True

        for individual in self.individuals:
            individual.CalculateF(func)
            individual.GeneratepBest()

    # Výpočet hodnotu funkce na konkrétním jedinci
    def CalculateIndividual(self, func: MethodType, individual: Individual) -> None:
        individual.CalculateF(func)

    # Výpočet nového vektoru na všech jedinců
    def CalculateVectorOfIndividuals(self, c_1: float, c_2: float, gBest: Individual, velocity: list) -> None:
        for individual in self.individuals:
            self.CalculateVectorOfIndividual(individual, c_1, c_2, gBest, velocity)

    # Výpočet nového vektoru na konkrétním jedinci
    def CalculateVectorOfIndividual(self, individual: Individual, c_1: float, c_2: float, gBest: Individual, velocity: list) -> None:
        r_1 = random.uniform(0, 1)
        r_2 = random.uniform(0, 1)
        individual.CalculateV(c_1, c_2, r_1, r_2, gBest, velocity, self.interval)

    # Výpočet nové pozice pro daného jedince, je zde obsažena i kontrola hranice intervalu funkce
    def CalculateNewPosition(self, individual: Individual) -> None:
        length = len(individual.coordinates)

        for i in range(length):
            individual.coordinates[i] = individual.coordinates[i] + individual.v[i]
            if individual.coordinates[i] <= self.interval.lowerBound:
                individual.coordinates[i] = self.interval.lowerBound
            elif individual.coordinates[i] >= self.interval.upperBound:
                individual.coordinates[i] = self.interval.upperBound

    # Funkce vrací nejlepšího jedince, pokud nebyli ještě jedinci ohodnoce, vrátí se hodnota None
    def GetBestIndividual(self) -> float or None:
        if not self.__individualsWereCalculated:
            return None
        return min(self.individuals, key = attrgetter("f"))