import numpy as np
from numpy.lib.function_base import select

class CellularAutomaton:

    def __init__(self, size: int, rule: int) -> None:
        """
        Cellular Automaton creates one step by method execute.
        Params:
            size: is a size of space for cells
            rule: it determines the rule for each step
        """
        self.size = size
        self.rule = self.__rule_calculation(rule)
        self.cellHistory = np.empty((0, self.size), dtype=np.int8)
        self.currentState = np.zeros(self.size, dtype=np.int8)
        #print(self.cellHistory)

    def __insert_into_history(self) -> None:
        self.cellHistory = np.append(self.cellHistory, np.array([self.currentState]), axis=0) 

    def __rule_calculation(self, number: int) -> np.ndarray:
        """
        Returns rule in numpy.ndarray based on the entry number.
        """
        binary_str = np.binary_repr(number, width=8)
        binary = np.array([int(char) for char in binary_str], dtype=np.int8)
        
        return binary

    def __calculate_next_step(self) -> np.ndarray:
        rightShift = np.roll(self.currentState, 1)
        leftShift = np.roll(self.currentState, -1)
        y = np.vstack((rightShift, self.currentState, leftShift)).astype(np.int8)
        #y2 = np.vstack((sr, self.currentState, sl))
        z = np.sum([[4],[2],[1]] * y, axis=0).astype(np.int8)

        #print(sr, sl, y, y2, z, self.rule[7 - z], self.rule)
        
        return self.rule[7 - z] # return converted result to binary

    def generate_start(self, random: bool = True, selection: str = "center") -> None:
        """
        If random is set to False value, then it is needed to set also the type of selection, default value is center
        """
        if random:
            self.currentState[:] = np.array(np.random.rand(self.size) < 0.5, dtype=np.int8)
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
        self.__insert_into_history()
        return self.currentState

"""
ca = CellularAutomaton(10, 90)
ca.generate_start(False)
ca.execute()
print(ca.cellHistory)

for i in range(1000):
    ca.execute()
    
print(ca.cellHistory)
"""
#print(ca.__rule_calculation(90))
#ca.generate_start(False, "right")
#print(ca.cellHistory)

#for i in ca.rule_calculation(90):  works
#    print(i)

"""
t = np.empty((0,3))
print(t)

a = np.array([1,2,3])
t = np.append(t, np.array([a]), axis=0)
b = np.array([4,5,6])
t = np.append(t, np.array([b]), axis=0)
print(t)
"""