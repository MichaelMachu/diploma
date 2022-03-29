from Graph import Graph
from Population import Population
from copy import deepcopy

class ParticleSwarm:

    def __init__(self) -> None:
        self.pop_size = 15   # Velikost populace
        self.c_1 = 2.0       # Konstanta pro výpočet vektoru v
        self.c_2 = 2.0       # Konstanta pro výpočet vektoru v
        self.M_max = 50      # Počet generací

    # Algoritmus Particle Swarm sestavený podle kódu z prezentace
    def ParticleSwarm(self, dimension, interval, func, figName, interval_anim):
        velocity = [-interval.step*2, interval.step*2] # Aktuálně možná rychlost

        # Vytvoření populace jedinců
        swarm = Population(interval, dimension)
        swarm.GenerateIndividuals(self.pop_size)
        # Vypočítaní hodnot na funkci pro všechny jedince
        swarm.CalculateIndividuals(func)
        # Nalezení nejlepšího jedince
        gBest = deepcopy(swarm.GetBestIndividual())
        # Pro každého jedince se vypočítá vektor v
        swarm.CalculateVectorOfIndividuals(self.c_1, self.c_2, gBest, velocity)
        m = 0

        # Pole historie populací pro vykreslení do animace
        population_history = []
        population_history.append(deepcopy(swarm))

        # Cyklus průchodu generací
        while m < self.M_max :
            # Cyklus průchodu jednotlivých jedinců
            for i, x in enumerate(swarm.individuals): 
                # Výpočet vektoru v na základě rychlost velocity
                swarm.CalculateVectorOfIndividual(x, self.c_1, self.c_2, gBest, velocity)
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
                    if x.pBestf < gBest.pBestf:
                        gBest = deepcopy(x)

                # Případné výstupy pro kontrolu hodnot
                #print(i, ". f: ", x.f, " x: ", x.coordinates[0], " y: ", x.coordinates[1])
                #print(i, ". pBestf: ", x.pBestf, " pBestX: ", x.pBest[0], " pBestY: ", x.pBest[1])
            m += 1
            # Přidání populace do historie pro vykreslení
            population_history.append(deepcopy(swarm))

        # Sestavení grafu
        graph = Graph(func, interval)
        graph.ShowByPopulation(figName, gBest, population_history, interval_anim)
