from Views import ApplicationView

from Domain.CellularAutomaton import CellularAutomaton
from Domain.TestCA import TestCA

if __name__ == "__main__":
    app = ApplicationView()

    """
    ca = CellularAutomaton(10, 5)
    ca.λ = 0.1
    for _ in range(20):
        print(ca.is_state_quiescent())
    """

    #testCa = TestCA(5, 4, 640, True, True, 123)
    #print(testCa.getWorld())
    #testCa.nextGeneration()
    #print(testCa.getWorld())
    #testCa.nextGeneration()
    #print(testCa.getWorld())