from types import MethodType
import numpy as np

from Bases.FunctionBase import FunctionBase

from Domain.Functions.LogisticMap import LogisticMap
from Domain.Functions.Sinus import Sinus
from Domain.Functions.ScaledRandomNormal import ScaledRandomNormal
from Domain.Functions.ScaledRandomUniform import ScaledRandomUniform

class FunctionSelection:

    def GetByName(name: str) -> FunctionBase:
        """
        Option names are:
            - logistic map
            - sinus
            - scaled normal
            - scaled uniform
        """

        switcher = {
            "logistic map": LogisticMap(),
            "sinus": Sinus(),
            "scaled normal": ScaledRandomNormal(),
            "scaled uniform": ScaledRandomUniform(),
        }
        # Get the function from switcher dictionary
        func = switcher.get(name.lower(), lambda: "Invalid name of the function")
        
        return func