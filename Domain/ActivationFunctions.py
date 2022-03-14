import numpy as np

# Aktivační funkce
class ActivationFunctions:

    def Signum(self, x):
        return np.sign(x)

    def ReLU(self, x):
        np.max(0, x)

    def Sigmoid(self, x):
        return 1/(1 + np.exp(-x))
        #return 1/(1 + np.e**(-x))

    def SigmoidDerivative(self, x):
        return x * (1 - x)