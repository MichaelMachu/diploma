import numpy as np
from types import MethodType
from typing import Tuple
from .Interval import Interval

# Funkce jsou sestavené podle pseudokódů a matematických funkcí ze stránky https://www.sfu.ca/~ssurjano/optimization.html
class TestFunctions:

    def GetByName(name: str) -> Tuple[MethodType, Interval]:
        """It returns test function with default interval.

        Option names are:
            - sphere
            - schwefel
            - rosenbrock
            - rastrigin
            - griewank
            - levy
            - michalewicz
            - zakharov
            - ackley
        """

        switcher = {
            "sphere": (TestFunctions.Sphere, Interval(-5.12,  5.12, 0.5)),
            "schwefel": (TestFunctions.Schwefel, Interval(-500, 500, 30)),
            "rosenbrock": (TestFunctions.Rosenbrock, Interval(-2.048,  2.048, 0.15)),
            "rastrigin": (TestFunctions.Rastrigin, Interval(-5.12, 5.12, 0.3)),
            "griewank": (TestFunctions.Griewank, Interval(-5, 5, 0.5)),
            "levy": (TestFunctions.Levy, Interval(-10, 10, 1)),
            "michalewicz": (TestFunctions.Michalewicz, Interval(0, np.pi, 0.1)),
            "zakharov": (TestFunctions.Zakharov, Interval(-10, 10, 1)),
            "ackley": (TestFunctions.Ackley, Interval(-32.768, 32.768, 3))
        }
        # Get the function from switcher dictionary
        func = switcher.get(name.lower(), lambda: "Invalid name of the test function")
        
        return func

    def Sphere(xx: list) -> float:
        summary = 0
        for x in xx:
            summary += x**2
        return summary

    def Schwefel(xx: list) -> float:
        d = len(xx)
        summary = 0
        for x in xx:
            summary += x * np.sin(np.sqrt(np.abs(x)))
        summary = 418.9829 * d - summary
        return summary

    def Rosenbrock(xx: list) -> float:
        index = 1
        summary = 0
        for x in xx[:-1]:
            summary += 100 * ((xx[index] - x**2)**2) + (x - 1)**2 
            index += 1
        return summary

    def Rastrigin(xx: list) -> float:
        d = len(xx)
        summary = 0
        for x in xx:
            summary += x**2 - 10 * np.cos(2 * np.pi * x)
        summary = d * 200 + summary
        return summary

    def Griewank(xx: list) -> float:
        summary = 0
        prod = 1
        i = 1
        for x in xx:
            summary += x**2 / 4000
            prod *= np.cos(x / np.sqrt(i))
            i += 1
        summary = summary - prod + 1
        return summary

    def Levy(xx: list) -> float:
        d = len(xx)
        summary = 0
        w = []
        for i in range(len(xx)):
            w.append(1 + (xx[i] - 1) / 4)

        term1 = (np.sin(np.pi * w[1]))**2
        term3 = (w[d-1] - 1)**2 * (1 + (np.sin(2 * np.pi * w[d-1]))**2)

        for wi in w[:-1]:
            summary += (wi - 1)**2 * (1 + 10 * (np.sin(np.pi * wi + 1))**2)
        summary = term1 + summary + term3
        return summary

    def Michalewicz(xx: list) -> float:
        summary = 0
        m = 10
        i = 1
        for x in xx:
            summary += np.sin(x) * (np.sin(i * x**2 / np.pi))**(2 * m)
            i += 1
        return -summary

    def Zakharov(xx: list) -> float:
        summary1 = 0
        summary2 = 0
        i = 1
        for x in xx:
            summary1 += x**2
            summary2 += 0.5 * i * x
            i += 1
        summary = summary1 + summary2**2 + summary2**4
        return summary

    def Ackley(xx: list) -> float:
        d = len(xx)
        summary1 = 0
        summary2 = 0
        a = 20
        b = 0.2
        c = 2 * np.pi
        for x in xx:
            summary1 += x**2
            summary2 += np.cos(c * x)
        summary = (-a * np.exp(-b * np.sqrt(summary1 / d))) + (-np.exp(summary2 / d)) + a + np.exp(1)
        return summary