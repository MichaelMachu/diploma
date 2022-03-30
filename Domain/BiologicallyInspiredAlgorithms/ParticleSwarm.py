from types import MethodType
from typing import Tuple, List
from copy import deepcopy
from .Graph import Graph
from .Population import Population
from .Interval import Interval
from .Individual import Individual

class ParticleSwarm:

    def __init__(self, pop_size: int = 15, c_1: float = 2.0, c_2: float = 2.0, M_max: int = 50) -> None:
        self.population_history = []    # History of population
        self.gBest = None               # The best found individual
        self.pop_size = pop_size        # Size of population
        self.c_1 = c_1                  # Constant value for calculation of vector v
        self.c_2 = c_2                  # Constant value for calculation of vector v
        self.M_max = M_max              # Maximum number of generations

    def execute(self, dimension: int, interval: Interval, func: MethodType) -> Tuple[Individual, List[Individual]]:
        velocity = [-interval.step*2, interval.step*2] # Aktuálně možná rychlost

        # Vytvoření populace jedinců
        swarm = Population(interval, dimension)
        swarm.GenerateIndividuals(self.pop_size)
        # Vypočítaní hodnot na funkci pro všechny jedince
        swarm.CalculateIndividuals(func)
        # Nalezení nejlepšího jedince
        self.gBest = deepcopy(swarm.GetBestIndividual())
        # Pro každého jedince se vypočítá vektor v
        swarm.CalculateVectorOfIndividuals(self.c_1, self.c_2, self.gBest, velocity)
        m = 0

        # Pole historie populací pro vykreslení do animace
        self.population_history = []
        self.population_history.append(deepcopy(swarm))

        # Cyklus průchodu generací
        while m < self.M_max :
            # Cyklus průchodu jednotlivých jedinců
            for i, x in enumerate(swarm.individuals): 
                # Výpočet vektoru v na základě rychlost velocity
                swarm.CalculateVectorOfIndividual(x, self.c_1, self.c_2, self.gBest, velocity)
                # Výpočet nové pozice a přepsání staré
                swarm.CalculateNewPosition(x)
                swarm.CalculateIndividual(func, x)
                
                # Kontrola hodnot na funkcí, kde x.f je aktuální hodnota a x.pBestf aktuálně nejlepší nalezena pro konkrétního jedince
                if x.f < x.pBestf:
                    # Pokud je x.f menší, tak jsme našli lepší hodnotu (minimum) a dojde k přepsání aktuálně nejlepší hodnotě pro daného jedince                 
                    x.pBestf = x.f
                    for j in range(len(x.coordinates)):
                        x.pBest[j] = deepcopy(x.coordinates[j])
                    
                    # Pokud je nejlepší hodnota konkrétního jedince lepší, jak u globálně nejlepšího jedince, pak se globální nahradí za aktuálního
                    if x.pBestf < self.gBest.pBestf:
                        self.gBest = deepcopy(x)

                # Případné výstupy pro kontrolu hodnot
                #print(i, ". f: ", x.f, " x: ", x.coordinates[0], " y: ", x.coordinates[1])
                #print(i, ". pBestf: ", x.pBestf, " pBestX: ", x.pBest[0], " pBestY: ", x.pBest[1])
            m += 1
            # Přidání populace do historie pro vykreslení
            self.population_history.append(deepcopy(swarm))

        return self.gBest, self.population_history