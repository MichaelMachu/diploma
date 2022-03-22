from types import MethodType
import numpy as np

class ActivationFunctions:

    def GetByName(name: str) -> MethodType:
        """
        Option names are:
            - signum
            - relu
            - sigmoid

        If you want a derivative of a specific method then use name:    
            - signum derivative
            - relu derivative
            - sigmoid derivative
        """

        switcher = {
            "signum": ActivationFunctions.Signum,
            "signum derivative": ActivationFunctions.SignumDerivative,
            "relu": ActivationFunctions.ReLU,
            "relu derivative": ActivationFunctions.ReLUDerivative,
            "sigmoid": ActivationFunctions.Sigmoid,
            "sigmoid derivative": ActivationFunctions.SigmoidDerivative
        }
        # Get the function from switcher dictionary
        func = switcher.get(name.lower(), lambda: "Invalid name of the activation function")
        
        return func

    def Signum(x: float) -> float:
        return np.sign(x)

    # 2*delta(x)
    def SignumDerivative(x: float) -> float:
        return 0 if x != 0 else 2
    
    def ReLU(x: float) -> float:
        return np.max(0, x)

    def Tanh(x: float) -> float:
        return np.tanh(x)

    def ReLUDerivative(x: float) -> float:
        return 0 if x < 0 else 1

    def Sigmoid(x: float) -> float:
        return 1/(1 + np.exp(-x))

    def SigmoidDerivative(x: float) -> float:
        return x * (1 - x)

    def TanhDerivative(x: float) -> float:
        return 1 - np.tanh(x)*np.tanh(x)