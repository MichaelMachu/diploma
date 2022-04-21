from Interfaces.TransferObjectInterface import TransferObjectInterface
from .DataProcess import DataProcess
from Domain.BiologicallyInspiredAlgorithms.ParticleSwarm import ParticleSwarm
from Domain.BiologicallyInspiredAlgorithms.Individual import Individual
from Domain.BiologicallyInspiredAlgorithms.Population import Population

class ParticleSwarmTransferObject(TransferObjectInterface):

    def __init__(self, particleSwarm: ParticleSwarm = None, functionName: str = None) -> None:
        if particleSwarm is None or functionName is None:
            return
        self.populations = particleSwarm.population_history
        self.bestFound = particleSwarm.gBest
        self.populationSize = particleSwarm.pop_size
        self.c1 = particleSwarm.c_1
        self.c2 = particleSwarm.c_2
        self.maxGeneration = particleSwarm.M_max
        self.functionName = functionName

    # Class functions
    def set_by_dict(dictValue: dict) -> "ParticleSwarmTransferObject":
        result = ParticleSwarmTransferObject()
        result.populations = [Population(individuals=[Individual(individualData[0], individualData[1], True) for individualData in populationData]) for populationData in dictValue["populations"]]
        result.bestFound = Individual(dictValue["bestFound"][0], dictValue["bestFound"][1], True)
        result.populationSize = dictValue["populationSize"]
        result.c1 = dictValue["c1"]
        result.c2 = dictValue["c2"]
        result.maxGeneration = dictValue["maxGeneration"]
        result.functionName = dictValue["functionName"]
        return result

    # Object functions
    def get_as_dict(self) -> dict:
        return {
            "populationSize": self.populationSize,
            "c1": self.c1,
            "c2": self.c2,
            "maxGeneration": self.maxGeneration,
            "functionName": self.functionName,
            "bestFound": [self.bestFound.pBest, self.bestFound.f],
            "populations": [[[individual.pBest, individual.f] for individual in population.individuals] for population in self.populations],
            "historyF": [[individual.f for individual in population.individuals] for population in self.populations],
            "historypBestF": [[individual.pBestf for individual in population.individuals] for population in self.populations],
        }