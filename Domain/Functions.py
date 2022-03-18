from types import MethodType
import numpy as np

class Functions:

    def GetByName(name: str) -> MethodType:
        """
        Option names are:
            - logistic map
            - sin
            - scaled normal
            - scaled uniform
        """

        switcher = {
            "logistic map": Functions.logistic_map,
            "sin": Functions.sin,
            "scaled normal": Functions.scaled_normal_with_random_selection,
            "scaled uniform": Functions.scaled_random_uniform,
        }
        # Get the function from switcher dictionary
        func = switcher.get(name.lower(), lambda: "Invalid name of the function")
        
        return func

    def logistic_map(r: float, x: float) -> float:
        return r * x * (1 - x)

    def sin(r: float) -> float:
        return np.sin(r)

    def scaled_normal_with_random_selection(r: float, a: float = 4, scale: float = 0.1) -> float:
        return a * np.random.normal(scale=scale) * (1 - r)

    def scaled_random_uniform(r: float, a: float = 4) -> float:
        return a * np.random.uniform(0, 1) * (1 - r)