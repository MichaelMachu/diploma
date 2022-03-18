from Views import ApplicationView

from Domain.Chaos01 import Chaos01
#import Domain.Functions.Sinus as func
from Domain.Functions.LogisticMap import LogisticMap
from Domain.Functions.Sinus import Sinus
from Domain.Functions.ScaledRandomNormal import ScaledRandomNormal
from Domain.Functions.ScaledRandomUniform import ScaledRandomUniform

if __name__ == "__main__":
#    app = ApplicationView()
    function = LogisticMap()
    Chaos01.bifurcation_diagram(function, 0, 10, 1000)