import numpy as np
from statistics import median
from typing import Tuple, List

from Interfaces.FunctionInterface import FunctionInterface

class Chaos01:

    def __init__(self, skip: int = 1, cut: int = 2) -> None:
        self.set_skip(skip)
        self.set_cut(cut)
        self.R = 628
        self.INCREASE = 1e-15   # small increase because of division at fraction in corrcoef function

    def minimum_skip(self) -> int:
        return 1

    def minimum_cut(self) -> int:
        return 2

    def set_skip(self, value: int) -> None:
        self.skip = value if value > self.minimum_skip() else self.minimum_skip()

    def set_cut(self, value: int) -> None:
        self.cut = value if value > self.minimum_cut() else self.minimum_cut()

    # Object functions
    def execute(self, signal: list) -> Tuple[int, list, list, list]:
        n1 = 0
        n2 = len(signal)
        phi = [signal[i] for i in range(n1, n2, self.skip)]
        N = len(phi)
        self.R = 628
        ncut = int(np.floor(N / self.cut))
        Ephi = 0
        for j in range(N):
            Ephi = Ephi + (1 / N) * phi[j]

        Kc = np.zeros(self.R)
        PC = np.zeros((self.R, N))
        QC = np.zeros((self.R, N))
        for m in range(1, self.R):
            c = m / 100
            pc = np.zeros(N)
            qc = np.zeros(N)
            pc[0] = phi[0] * np.cos(c)
            qc[0] = phi[0] * np.sin(c)
            
            for i in range(2, N):
                pc[i - 1] = pc[i - 2] + phi[i - 1] * np.cos((i) * c)
                qc[i - 1] = qc[i - 2] + phi[i - 1] * np.sin((i) * c)
            PC[m-1,:] = pc
            QC[m-1,:] = qc
            Vosc = np.zeros(ncut)
            
            for n in range(1, ncut):
                if c == 0:
                    Vosc[n - 1] = 0 # cos(0) = 1 => (1 - cos(0)) = 0 =/= / 0 can not divide by zero
                    continue
                Vosc[n - 1] = Ephi * Ephi * ((1 - np.cos(n * c)) / (1 - np.cos(c)))
            
            Mc = np.zeros(ncut)
            Dc = np.zeros(ncut)
            #Dc = np.full(ncut, INCREASE)
            
            for n in range(1, ncut):
                MCpom = np.zeros((N - 1 - ncut, 1))
                MCpom[0] = (pc[n] - pc[0]) ** 2 + (qc[n] - qc[0]) ** 2
                
                for j in range(N-1-ncut - 1):
                    MCpom[j + 1] = MCpom[j] + (pc[j + n] - pc[j + 1]) ** 2 + (qc[j + n] - qc[j + 1]) ** 2
                
                if N - 1 - ncut - 1 == 0:
                    Mc[n - 1] = 0
                else:
                    Mc[n - 1] = MCpom[N - 1 - ncut - 1] / (N - 1 - ncut - 1)
                Dc[n - 1] = Mc[n - 1] - Vosc[n - 1] + self.INCREASE
            
            if ncut <= 1:
                CR = [[0, 0], [0, 0]]
            else:
                pom = [i for i in range(ncut)]
                CR = np.corrcoef(pom, Dc)
            Kc[m-1] = CR[1][0]

        k = median(Kc)
        return k, Kc, PC, QC

    # Class functions
    def execute_for_bifurcation_diagram(chaos01: "Chaos01", function: FunctionInterface, lineArray: list = None) -> List[dict]:
        lineArray = function.get_line_array() if lineArray is None else lineArray
        N = 500
        x = 0.5 + np.zeros(N)
        endcap = np.arange(round(N * 0.9), N)

        data = []
        
        for r in lineArray:
            for n in range(N - 1):
                x[n + 1] = function.get(r, x[n])

            u = np.unique(x[endcap])
            xx = r * np.ones(len(u))
            k, Kc, PC, QC = chaos01.execute(u)    # , 1, 20        2, 8
            
            items = {"xx": xx, "yy": u, "k": k, "Kc": Kc, "PC": PC, "QC": QC}
            data.append(items)
        
        return data

    def execute_for_iteration(chaos01: "Chaos01", historyData: list) -> List[dict]: # lineArray: list = None
        data = []
        i = 0
        INCREMENT = 1/len(historyData[0])    # 1e-2
        size = len(historyData)

        for index, items in enumerate(historyData):
            k, Kc, PC, QC = chaos01.execute(items)  # , 4
            print(k)
            segment = []
            
            for item in items:
                i += INCREMENT
                segment.append([i, item])
            
            if index + 1 < size:
                segment.append([i+INCREMENT, historyData[index + 1][0]]) # add join between two segments
            
            items = {"segment": segment, "k": k, "Kc": Kc, "PC": PC, "QC": QC}
            data.append(items)
        
        return data