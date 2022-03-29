import random
from Individual import Individual
from operator import attrgetter

class Population:

    # Privátní promměná, která nabývá hodnoty true, pokud již jedinci byli ohodnoceni (kvůli výběru nejlepšího jedince)
    __individualsWereCalculated = False

    def __init__(self, interval, dimension):
        self.interval = interval
        self.dimension = dimension
        self.individuals = []

    # Generuje náhodné hodnoty pro vyhledávání skrze hodnoty z intervalu a dimenze
    def GenerateIndividual(self):
        array = []

        for _ in range(self.dimension):  
            array.append(random.uniform(self.interval.lowerBound, self.interval.upperBound))
            
        individual = Individual(array)
        
        return individual

    # Vytvoření populace jedinců
    def GenerateIndividuals(self, number):
        if self.individuals:
            return

        for _ in range(number):
            self.individuals.append(self.GenerateIndividual())

    # Výpočet hodnot na funkci pro všechny jedince
    def CalculateIndividuals(self, func):
        self.__individualsWereCalculated = True

        for individual in self.individuals:
            individual.CalculateF(func)
            individual.GeneratepBest()

    # Výpočet hodnotu funkce na konkrétním jedinci
    def CalculateIndividual(self, func, individual):
        individual.CalculateF(func)

    # Výpočet nového vektoru na všech jedinců
    def CalculateVectorOfIndividuals(self, c_1, c_2, gBest, velocity):
        for individual in self.individuals:
            self.CalculateVectorOfIndividual(individual, c_1, c_2, gBest, velocity)

    # Výpočet nového vektoru na konkrétním jedinci
    def CalculateVectorOfIndividual(self, individual, c_1, c_2, gBest, velocity):
        r_1 = random.uniform(0, 1)
        r_2 = random.uniform(0, 1)
        individual.CalculateV(c_1, c_2, r_1, r_2, gBest, velocity, self.interval)

    # Výpočet nové pozice pro daného jedince, je zde obsažena i kontrola hranice intervalu funkce
    def CalculateNewPosition(self, individual):
        length = len(individual.coordinates)

        for i in range(length):
            individual.coordinates[i] = individual.coordinates[i] + individual.v[i]
            if individual.coordinates[i] <= self.interval.lowerBound:
                individual.coordinates[i] = self.interval.lowerBound
            elif individual.coordinates[i] >= self.interval.upperBound:
                individual.coordinates[i] = self.interval.upperBound

    # Funkce vrací nejlepšího jedince, pokud nebyli ještě jedinci ohodnoce, vrátí se hodnota None
    def GetBestIndividual(self):
        if not self.__individualsWereCalculated:
            return None
        return min(self.individuals, key = attrgetter("f"))