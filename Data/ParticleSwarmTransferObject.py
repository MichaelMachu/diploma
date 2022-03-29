from Interfaces.TransferObjectInterface import TransferObjectInterface
from .DataProcess import DataProcess
from Domain.BiologicallyInspiredAlgorithms.ParticleSwarm import ParticleSwarm

class ParticleSwarmTransferObject(TransferObjectInterface):

    def __init__(self, particleSwarm: ParticleSwarm = None) -> None:
        if particleSwarm is None:
            return
        self.history = particleSwarm.population_hostory
        self.populationSize = particleSwarm.pop_size
        self.c1 = particleSwarm.c_1
        self.c2 = particleSwarm.c_2
        self.maxGeneration = particleSwarm.M_max

    # Class functions
    def set_by_dict(dictValue: dict) -> "ParticleSwarmTransferObject":
        result = ParticleSwarmTransferObject()
        result.history = dictValue["history"]
        result.populationSize = dictValue["populationSize"]
        result.c1 = dictValue["c1"]
        result.c2 = dictValue["c2"]
        result.maxGeneration = dictValue["maxGeneration"]
        return result

    # Object functions
    def get_as_dict(self) -> dict:
        return {
            "populationSize": self.populationSize,
            "c1": self.c1,
            "c2": self.c2,
            "maxGeneration": self.maxGeneration,
            "history": self.history,
        }