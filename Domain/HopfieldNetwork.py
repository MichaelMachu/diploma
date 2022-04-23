from types import MethodType
from typing import Tuple
import numpy as np
from copy import deepcopy
from math import sqrt

from .NeuronMatrix import NeuronMatrix

class HopfieldNetwork:

    def __init__(self, size: Tuple[int, int] = (10, 10)) -> None:
        self.iter = 0
        self.size = size
        self.sizeFull = size[0] * size[1]
        self.bias = 1e-10   # 1e-5 1e-1
        self.history = []

    def get_max_patterns(self) -> int:
        return int(self.sizeFull / (2 * sqrt(self.sizeFull)))

    # Sečtení všech matic
    def SumMatrices(self, matrices: NeuronMatrix) -> list:  # n: int, m: int
        rows, cols = (self.sizeFull, self.sizeFull) # (n*m, n*m)
        array = [[0 for _ in range(cols)] for _ in range(rows)]
        # Procházení všech matic
        for i in range(len(matrices)):
            # Procházení paternu konkrétní matice
            for j in range(len(matrices[i].fullPattern)):
                for k in range(len(matrices[i].fullPattern[j])):
                    array[j][k] = array[j][k] + matrices[i].fullPattern[j][k]

        return array

    def energy(self, activatedInputVector: list) -> float:
        summaryWeight = 0
        summaryBias = 0
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                summaryWeight += self.summedPatterns[i][j] * activatedInputVector[i] * activatedInputVector[j]
            
        for value in activatedInputVector:
            summaryBias += value * self.bias

        return -0.5 * summaryWeight + summaryBias

    # Hopfieldova sít synchroním způsobem
    def HopfieldNetworkSync(self, dimension: int, func: MethodType, inputVector: list, patterns: NeuronMatrix) -> list: # n: int, m: int
        # Sečtu všechny paterny aneb vytvořím celkovou váhu všech matic
        summedPatterns = self.SumMatrices(patterns)

        # Vstupnímu vektoru převedu nuly na mínus jedničky
        for i in range(len(inputVector)):
            if inputVector[i] == 0:
                inputVector[i] = -1

        result = []
        # Násobící fáze
        for i in range(len(summedPatterns)):
            pom = 0
            for j in range(len(summedPatterns[i])):
                pom = summedPatterns[i][j] * inputVector[j]
            pom = func(pom)
            result.append(pom)

        # Výslednému vektoru převedu mínus jedničky na nuly
        for i in range(len(result)):
            if result[i] == -1:
                result[i] = 0

        return result

    # Hopfieldova sít asynchroním způsobem
    def HopfieldNetworkAsync(self, dimension: int, func: MethodType, inputVector: list, patterns: NeuronMatrix, checkMax: int = 3, useCheck: bool = False) -> list: # useEnergy: bool = True
        # Sečtu všechny paterny aneb vytvořím celkovou váhu všech matic
        summedPatterns = self.SumMatrices(patterns)
        self.summedPatterns = summedPatterns

        # Vstupnímu vektoru převedu nuly na mínus jedničky
        for i in range(len(inputVector)):
            if inputVector[i] == 0:
                inputVector[i] = -1

        check = 0
        change = deepcopy(inputVector)
        self.history = [deepcopy(inputVector)]
        areSame = False
        self.iter = 0

        energy = self.energy(change)
        
        # Provádím cyklus tak dlouho, dokud se matice nemění 10x po sobě
        while check < checkMax:
            # Výpočet opravení chyb skrze váhovou matici a vstupní vektor
            for i in range(self.sizeFull): #np.random.permutation(size) #range(size):
                idx = np.random.randint(0, self.sizeFull)

                summary = 0
                for j in range(self.sizeFull): #np.random.permutation(m*n): #range(m*n):
                    summary += inputVector[j] * summedPatterns[idx][j] #summedPatterns[i][j] #summedPatterns[j][i] => original a blbě
                summary = func(summary)
                inputVector[idx] = summary

            self.history.append(deepcopy(inputVector))
            energyNew = self.energy(inputVector)

            print(energy, energyNew)

            #if useEnergy:
            if energy == energyNew:
                if useCheck:
                    # Kontrola, jestli se výsledek nezměnil
                    for i in range(len(change)):
                        if change[i] != inputVector[i]:
                            areSame = False
                            break
                        else:
                            areSame = True

                    if areSame:
                        check += 1
                    else:
                        check = 0
                        change = deepcopy(inputVector)
                else:
                    break

            energy = energyNew

            self.iter += 1

        # Výslednému vektoru převedu mínus jedničky na nuly
        for i in range(len(inputVector)):
            if inputVector[i] == -1:
                inputVector[i] = 0

        return inputVector