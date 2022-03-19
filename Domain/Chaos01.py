import numpy as np
from statistics import median

from Interfaces.FunctionInterface import FunctionInterface

class Chaos01:

    def execute(signal: list, skip: int = 1, cut: int = 2) -> tuple[int, list, list, list]:
        n1 = 0
        n2 = len(signal)
        phi = [signal[i] for i in range(n1, n2, skip)]
        N = len(phi)
        R = 628
        ncut = int(np.floor(N / cut))
        x = 0
        Ephi = 0
        for j in range(N):
            Ephi = Ephi + (1 / N) * phi[j]

        Kc = np.zeros(R)
        PC = np.zeros((R, N))
        QC = np.zeros((R, N))
        for m in range(1, R):
            #   x=x+1;
            c = m / 100
            #print(m)
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
            
            for n in range(1, ncut):
                MCpom = np.zeros((N - 1 - ncut, 1))
                MCpom[0] = (pc[n] - pc[0]) ** 2 + (qc[n] - qc[0]) ** 2
                
                for j in range(N-1-ncut - 1):
                    MCpom[j + 1] = MCpom[j] + (pc[j + n] - pc[j + 1]) ** 2 + (qc[j + n] - qc[j + 1]) ** 2
                
                if N - 1 - ncut - 1 == 0:
                    Mc[n - 1] = 0
                else:
                    Mc[n - 1] = MCpom[N - 1 - ncut - 1] / (N - 1 - ncut - 1)
                Dc[n - 1] = Mc[n - 1] - Vosc[n - 1]
            
            pom = [i for i in range(ncut)]
            CR = np.corrcoef(pom, Dc)
            Kc[m-1] = CR[1][0]

        k = median(Kc)
        return k, Kc, PC, QC

    def execute_for_bifurcation_diagram(function: FunctionInterface, lineArray: list = None) -> list[dict]:
        lineArray = function.get_line_array() if lineArray is None else lineArray
        N = 500
        x = 0.5 + np.zeros(N)
        endcap = np.arange(round(N * 0.9), N)
        colors = []

        data = []
        
        for r in lineArray:
            for n in range(N - 1):
                x[n + 1] = function.get(r, x[n])

            u = np.unique(x[endcap])
            xx = r * np.ones(len(u))
            k, Kc, PC, QC = Chaos01.execute(u, 1, 20)    # 2, 8
            
            set_color = "#ff0000" if k > 0.9 else "#00ff00"
            colors = [set_color for _ in range(len(xx))]

            items = {"xx": xx, "yy": u, "colors": colors}
            data.append(items)
        
        return data