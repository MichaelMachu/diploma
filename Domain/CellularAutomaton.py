import numpy as np
from math import ceil
from random import seed, randint

class CellularAutomaton:

    def __init__(self, size: int or tuple, rule: int = None, K: int = 2, N: int = 3, λ: float = None, seedNumber: int = None) -> None:
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
        self.ruleNumber = rule          # Rule represented as number
        self.dimension = 1              # Dimension of the world
        if λ is None:
            # Set CA to 2D
            if type(size) is tuple and len(size) > 1:
                self.dimension = 2
                self.pattern2D = "moore"
                self.possibleStates = 18
                self.rule = self.__rule_calculation_binary(rule)
            # Set CA to 1D
            else:
                self.rule = self.__rule_calculation_binary(rule) if K == 2 else self.__rule_calculation(rule)
        else:
            self.ruleNumber = CellularAutomaton.get_quiescent_trainsitions(self.λ, self.K, self.N)
            self.possibleStates = N     # possible states for the neighborhood pattern -> is_rule_valid returns K^N
            self.seedNumber = seedNumber
            if seedNumber is None:
                #self.seedNumber = randint(-2147483648, 2147483647) # self.randomSeed
                self.seedNumber = randint(0, 2**32 - 1)
            seed(self.seedNumber)
            np.random.seed(self.seedNumber)
            print("seed: ", self.seedNumber)
            self.rule = [randint(1, self.K - 1) for _ in range(self.K**self.N)]
            #self.ruleUsed = [randint(0, 1) for _ in range(self.K**self.N)]
            self.isQuiscentState = [self.is_state_quiescent() for _ in range(self.K**self.N)]
        self.cellHistory = np.empty((0, self.size) if self.dimension == 1 else self.size, dtype=np.int8)
        self.currentState = np.zeros(self.size, dtype=np.int8)

    # Class functions
    def get_lambda(K: int, N: int, n: int) -> float:
        """
        Returns value of characterized paramater λ
        Params:
            - K: number of cell states
            - N: size of the neighborhood
            - n: value of a transition to special quiescent state
        """
        KN = K**N
        return (KN - n) / KN

    def get_quiescent_trainsitions(λ: float, K: int, N: int) -> int:
        """
        Returns value of a transition to special quiescent state
        Params:
            - λ: characterized paramater of subspace D(K/N)
            - K: number of cell states
            - N: size of the neighborhood
        """
        KN = K**N
        return -int((λ * KN) - KN)

    # Object functions
    def is_rule_valid(self) -> bool:
        return self.ruleNumber <= self.K**self.possibleStates

    def is_state_quiescent(self) -> bool:
        """Returns false for a random value or true for a quiescent state based on probability of λ"""
        if self.λ is None:
            raise ValueError("λ is not set")
        return bool(np.random.choice(a=[False, True], p=[self.λ, 1 - self.λ]))

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
        if self.dimension == 2:
            self.cellHistory = np.dstack((self.cellHistory, self.currentState))
            return
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

    def __calculate_next_step_2D(self) -> np.ndarray:
        stateSize = len(self.currentState)
        nextState = np.zeros(self.size, dtype=np.int8)

        if self.pattern2D == "neuman":
            for i in range(stateSize):
                # Previous states
                if i == 0:
                    previousStates = self.currentState[stateSize - 1]
                else:
                    previousStates = self.currentState[i - 1]

                # Next states
                if i == stateSize - 1:
                    nextStates = self.currentState[0]
                else:
                    nextStates = self.currentState[i + 1]

                #  Middle states
                middleStateRightShift = np.roll(self.currentState[i], 1)
                middleStateleftShift = np.roll(self.currentState[i], -1)

                stackOfNeighbors = np.vstack((previousStates, middleStateRightShift, self.currentState[i], middleStateleftShift, nextStates)).astype(np.int8)
                indexesOfNextStep = np.sum(stackOfNeighbors, axis=0).astype(np.int8)
            
                nextState[i,:] = self.rule[self.possibleStates - 1 - indexesOfNextStep]
            
            return nextState
        
        if self.pattern2D == "moore":
            for i in range(stateSize):
                index = i
                # Previous states
                if i == 0:
                    index = stateSize - 1
                else:
                    index = i - 1
                previousStates = self.currentState[index]
                previousStateRightShift = np.roll(self.currentState[index], 1)
                previousStateleftShift = np.roll(self.currentState[index], -1)

                # Next states
                if i == stateSize - 1:
                    index = 0
                else:
                    index = i + 1
                nextStates = self.currentState[index]
                nextStateRightShift = np.roll(self.currentState[index], 1)
                nextStateleftShift = np.roll(self.currentState[index], -1)

                #  Middle states
                middleStateRightShift = np.roll(self.currentState[i], 1)
                middleStateleftShift = np.roll(self.currentState[i], -1)

                stackOfNeighbors = np.vstack((previousStateRightShift, previousStates, previousStateleftShift, 
                                            middleStateRightShift, self.currentState[i], middleStateleftShift, 
                                            nextStateRightShift, nextStates, nextStateleftShift)).astype(np.int8)
                indexesOfNextStep = np.sum(stackOfNeighbors, axis=0).astype(np.int8)

                nextState[i,:] = self.rule[self.possibleStates - 1 - indexesOfNextStep]
            
            return nextState
        
        return None     # Pattern2D is not defined

    def generate_start(self, random: bool = True, selection: str = "center") -> None:
        """If random is set to False value, then it is needed to set also the type of selection, default value is center"""
        #self.quiescentState = np.random.randint(self.K)
        self.quiescentState = 0

        if self.dimension == 2:
            if random:
                #self.currentState[:] = np.array(np.random.rand(self.size) < 0.5, dtype=np.int8)
                self.currentState = np.random.randint(2, size=self.size)
                self.__insert_into_history()
                #print(self.currentState)
                return

            self.currentState[self.size[0] // 2:self.size[1] // 2] = 1
            return
        
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
        self.currentState = self.__calculate_next_step() if self.dimension == 1 else self.__calculate_next_step_2D()
        #print(self.currentState)
        #if self.λ is not None:
        #    self.__solver_random_table()
        self.__insert_into_history()
        #print(self.currentState)
        return self.currentState