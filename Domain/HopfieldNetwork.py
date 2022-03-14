import random
import numpy as np
import copy

class HopfieldNetwork:

    def __init__(self):
        self.iter = 0

    # Sečtení všech matic
    def SumMatrices(self, matrices, n, m):
        rows, cols = (n*m, n*m) 
        array = [[0 for i in range(cols)] for j in range(rows)]
        # Procházení všech matic
        for i in range(len(matrices)):
            # Procházení paternu konkrétní matice
            for j in range(len(matrices[i].fullPattern)):
                for k in range(len(matrices[i].fullPattern[j])):
                    array[j][k] = array[j][k] + matrices[i].fullPattern[j][k]

        return array

    # Hopfieldova sít synchroním způsobem
    def HopfieldNetworkSync(self, dimension, func, input_vector, patterns, n, m):
        # Sečtu všechny paterny aneb vytvořím celkovou váhu všech matic
        summedPatterns = self.SumMatrices(patterns, n, m)

        # Vstupnímu vektoru převedu nuly na mínus jedničky
        for i in range(len(input_vector)):
            if input_vector[i] == 0:
                input_vector[i] = -1

        result = []
        # Násobící fáze
        for i in range(len(summedPatterns)):
            pom = 0
            for j in range(len(summedPatterns[i])):
                pom = summedPatterns[i][j] * input_vector[j]
            pom = func(pom)    # not sure
            result.append(pom)

        # Výslednému vektoru převedu mínus jedničky na nuly
        for i in range(len(result)):
            if result[i] == -1:
                result[i] = 0

        return result

    # Hopfieldova sít asynchroním způsobem
    def HopfieldNetworkAsync(self, dimension, func, input_vector, patterns, n, m):
        # Sečtu všechny paterny aneb vytvořím celkovou váhu všech matic
        summedPatterns = self.SumMatrices(patterns, n, m)

        # Vstupnímu vektoru převedu nuly na mínus jedničky
        for i in range(len(input_vector)):
            if input_vector[i] == 0:
                input_vector[i] = -1

        check = 0
        change = copy.deepcopy(input_vector)
        are_same = False
        print(input_vector)
        self.iter = 0
        size = m*n
        
        # Provádím cyklus tak dlouho, dokud se matice nemění 10x po sobě
        while check < 10:
            # Výpočet opravení chyb skrze váhovou matici a vstupní vektor
            for i in np.random.permutation(size): #np.random.permutation(size) #range(size):
                summary = 0
                for j in range(size): #np.random.permutation(m*n): #range(m*n):
                    summary += input_vector[j] * summedPatterns[i][j] #summedPatterns[i][j] #summedPatterns[j][i] => original a blbě
                summary = func(summary)
                input_vector[i] = summary

            # Kontrola, jestli se výsledek nezměnil
            for i in range(len(change)):
                if change[i] != input_vector[i]:
                    are_same = False
                    break
                else:
                    are_same = True

            if are_same:
                check += 1
            else:
                check = 0
                change = copy.deepcopy(input_vector)

            self.iter += 1

        # Výslednému vektoru převedu mínus jedničky na nuly
        for i in range(len(input_vector)):
            if input_vector[i] == -1:
                input_vector[i] = 0

        return input_vector