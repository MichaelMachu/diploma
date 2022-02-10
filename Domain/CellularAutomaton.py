import numpy as np
from math import ceil
from random import seed, randint

class CellularAutomaton:

    def __init__(self, size: int, rule: int, K: int = 2, N: int = 3, λ: float = None) -> None:
        """
        Cellular Automaton creates one step by method execute.
        Params:
            - size: is a size of space for cells
            - rule: it determines the rule for each step
        """
        self.size = size                # Size of dimension (number of neighbors)
        self.K = K                      # Number of states (colors)
        self.N = N                      # Neighborhood - number of neighbors
        self.λ = λ                      # Lambda
        self.quiescentState = None      # Arbitrary state
        self.possibleStates = 8 if K == 2 else 3 * K - 2    # 8 = 2^3
        #self.possibleStates = K**N
        self.ruleNumber = rule
        if λ is None:
            self.rule = self.__rule_calculation_binary(rule) if K == 2 else self.__rule_calculation(rule)
        else:
            seed(randint(-2147483648, 2147483647)) # self.randomSeed
            self.rule = [randint(0, self.K - 1) for _ in range(self.K**self.N)]
            #self.ruleUsed = [randint(0, 1) for _ in range(self.K**self.N)]
            self.isQuiscentState = [self.is_state_quiescent() for _ in range(self.K**self.N)]
        self.cellHistory = np.empty((0, self.size), dtype=np.int8)
        self.currentState = np.zeros(self.size, dtype=np.int8)

    # Class functions
    def get_lambda(K: int, N: int, n: int):
        """
        Returns value of characterized paramater λ
        Params:
            - K: number of cell states
            - N: size of the neighborhood
            - n: value of a transition to special quiescent state
        """
        KN = K**N
        return (KN - n) / KN

    def get_quiescent_trainsitions(λ: float, K: int, N: int):
        """
        Returns value of a transition to special quiescent state
        Params:
            - λ: characterized paramater of subspace D(K/N)
            - K: number of cell states
            - N: size of the neighborhood
        """
        KN = K**N
        return -((λ * KN) - KN)

    # Object functions
    def is_rule_valid(self) -> bool:
        return self.ruleNumber <= self.K**self.possibleStates

    def is_state_quiescent(self) -> bool:
        """Returns false for a random value or true for a quiescent state based on probability of λ"""
        if self.λ is None:
            raise ValueError("λ is not set")
        return np.random.choice(a=[False, True], p=[self.λ, 1 - self.λ])

    def __solver_random_table(self) -> None:
        """neighborhood = []
        center = ceil(self.N / 2)
        for i in reversed(range(1, self.N + 1)): # range(1, self.N)
            if i < center:
                neighborhood.append(np.roll(self.currentState, i - center))
            elif i > center:
                neighborhood.append(np.roll(self.currentState, i - center))
            else:
                neighborhood.append(self.currentState)

        for i in range(len(self.currentState)):
            if self.is_state_quiescent():
        """
        for i in range(len(self.currentState)):
            if self.is_state_quiescent():
                self.currentState[i] = self.quiescentState
            #else:
            #    self.currentState[i] = np.random.randint(self.K - 1) + 1


    def __solver_table_walk_through(self) -> None:
        pass

    def __insert_into_history(self) -> None:
        self.cellHistory = np.append(self.cellHistory, np.array([self.currentState]), axis=0) 

    def __rule_calculation_binary(self, number: int) -> np.ndarray:
        """Returns binary rule in numpy.ndarray based on the entry number."""
        binaryStr = np.binary_repr(number, width=self.possibleStates)
        binary = np.array([int(char) for char in binaryStr], dtype=np.int8)
        
        return binary

    def __rule_calculation(self, number: int) -> np.ndarray:
        result = [0 for _ in range(self.possibleStates)] # for k color => 3*k-2 => 3 * self.K - 2
        i = len(result) - 1
        #i = 0
        while (number != 0):
            result[i] = number % self.K
            number = int(number / self.K)
            i = i - 1
            #i = i + 1

        # Convert to ndarray
        result = np.array([val for val in result], dtype=np.int8)

        return result

    def __calculate_next_step(self) -> np.ndarray:
        #print(self.currentState)
        neighborhood = []
        center = ceil(self.N / 2)
        for i in reversed(range(1, self.N + 1)): # range(1, self.N)
            if i < center:
                neighborhood.append(np.roll(self.currentState, i - center))
                #print(i - center)
            elif i > center:
                neighborhood.append(np.roll(self.currentState, i - center))
                #print(i - center)
            else:
                neighborhood.append(self.currentState)
                #print(0)
                
        #x = np.vstack(neighborhood).astype(np.int8)
        #print(x)

        if self.λ is not None:
            result = []
            i, j, c = 0, 0, 0
            while j < self.size:
                c = c * self.K + neighborhood[i][j]

                i += 1

                if i >= self.N:
                    if not self.isQuiscentState[c]:
                        result.append(self.rule[c])
                    else:
                        result.append(self.quiescentState)
                    j += 1
                    i = 0
                    c = 0
                
            return result

        #print(neighborhood)
        #rightShift = np.roll(self.currentState, 1)
        #leftShift = np.roll(self.currentState, -1)
        #stackOfNeighbors = np.vstack((rightShift, self.currentState, leftShift)).astype(np.int8)

        #print(stackOfNeighbors)
        stackOfNeighbors = np.vstack(neighborhood).astype(np.int8)

        # Indexes for the next step are calculated by two ways:
        # - if state of cells is binary, then the stack of all neighbors is multiplied by power of two
        # - if state of cells is ternary or bigger then it is used summary of neighbors, 
        #   because the rule is made differently (converted to specific system)
        indexesOfNextStep = np.sum([[4],[2],[1]] * stackOfNeighbors, axis=0).astype(np.int8) if self.K == 2 else np.sum(stackOfNeighbors, axis=0).astype(np.int8)

        return self.rule[self.possibleStates - 1 - indexesOfNextStep]

    def generate_start(self, random: bool = True, selection: str = "center") -> None:
        """If random is set to False value, then it is needed to set also the type of selection, default value is center"""
        #self.quiescentState = np.random.randint(self.K)
        self.quiescentState = 0
        
        if random:
            self.currentState[:] = np.array(np.random.rand(self.size) < 0.5, dtype=np.int8)
            self.__insert_into_history()
            return

        if selection == "left":
            self.currentState[0] = 1
        elif selection == "right":
            self.currentState[self.size - 1] = 1
        else:
            self.currentState[self.size // 2] = 1

        self.__insert_into_history()

    def execute(self) -> np.ndarray:
        self.currentState = self.__calculate_next_step()
        print(self.currentState)
        #if self.λ is not None:
        #    self.__solver_random_table()
        self.__insert_into_history()
        return self.currentState