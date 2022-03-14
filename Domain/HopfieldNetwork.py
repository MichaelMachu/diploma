from types import MethodType
import numpy as np
import copy

from .NeuronMatrix import NeuronMatrix

class HopfieldNetwork:

    def __init__(self) -> None:
        self.iter = 0

    # Sečtení všech matic
    def SumMatrices(self, matrices: NeuronMatrix, n: int, m: int) -> list:
        rows, cols = (n*m, n*m) 
        array = [[0 for _ in range(cols)] for _ in range(rows)]
        # Procházení všech matic
        for i in range(len(matrices)):
            # Procházení paternu konkrétní matice
            for j in range(len(matrices[i].fullPattern)):
                for k in range(len(matrices[i].fullPattern[j])):
                    array[j][k] = array[j][k] + matrices[i].fullPattern[j][k]

        return array

    # Hopfieldova sít synchroním způsobem
    def HopfieldNetworkSync(self, dimension: int, func: MethodType, inputVector: list, patterns: NeuronMatrix, n: int, m: int) -> list:
        # Sečtu všechny paterny aneb vytvořím celkovou váhu všech matic
        summedPatterns = self.SumMatrices(patterns, n, m)

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
            pom = func(pom)    # not sure
            result.append(pom)

        # Výslednému vektoru převedu mínus jedničky na nuly
        for i in range(len(result)):
            if result[i] == -1:
                result[i] = 0

        return result

    # Hopfieldova sít asynchroním způsobem
    def HopfieldNetworkAsync(self, dimension: int, func: MethodType, inputVector: list, patterns: NeuronMatrix, n: int, m: int) -> list:
        # Sečtu všechny paterny aneb vytvořím celkovou váhu všech matic
        summedPatterns = self.SumMatrices(patterns, n, m)

        # Vstupnímu vektoru převedu nuly na mínus jedničky
        for i in range(len(inputVector)):
            if inputVector[i] == 0:
                inputVector[i] = -1

        check = 0
        change = copy.deepcopy(inputVector)
        areSame = False
        print(inputVector)
        self.iter = 0
        size = m*n
        
        # Provádím cyklus tak dlouho, dokud se matice nemění 10x po sobě
        while check < 10:
            # Výpočet opravení chyb skrze váhovou matici a vstupní vektor
            for i in np.random.permutation(size): #np.random.permutation(size) #range(size):
                summary = 0
                for j in range(size): #np.random.permutation(m*n): #range(m*n):
                    summary += inputVector[j] * summedPatterns[i][j] #summedPatterns[i][j] #summedPatterns[j][i] => original a blbě
                summary = func(summary)
                inputVector[i] = summary

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
                change = copy.deepcopy(inputVector)

            self.iter += 1

        # Výslednému vektoru převedu mínus jedničky na nuly
        for i in range(len(inputVector)):
            if inputVector[i] == -1:
                inputVector[i] = 0

        return inputVector