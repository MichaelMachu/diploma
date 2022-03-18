import numpy as np
from statistics import median

from Interfaces.FunctionInterface import FunctionInterface

class Chaos01:

    def execute(signal: list, skip: int = 1, cut: int = 2) -> tuple[int, list, list, list]:
        n1 = 0
        n2 = len(signal)
        phi = [signal[i] for i in range(n1, n2, skip)]
        N = len(phi)
        ncut = int(np.floor(N / cut))
        x = 0
        Ephi = 0
        for j in range(N):
            Ephi = Ephi + (1 / N) * phi[j]

        Kc = np.zeros(628)
        PC = np.zeros((628, N))
        QC = np.zeros((628, N))
        for m in range(1, 628):
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

    def bifurcation_diagram(function: FunctionInterface, start: float = 1.4, end: float = 4, values: int = 100) -> None:
        lineArray = np.linspace(start, end, values) # 1000
        N = 500
        x = 0.5 + np.zeros(N)
        endcap = np.arange(round(N * 0.9), N)
        colors = []
        fig = pl.figure()
        ax = fig.add_subplot(111)
        #u, r = [], []
        for r in lineArray:
            for n in range(N - 1):
                x[n + 1] = function.get(r, x[n])
            #colors.append("#000000")

            u = np.unique(x[endcap])
            xx = r * np.ones(len(u))
            k, Kc, PC, QC = Chaos01.execute(u, 1, 20)    # 2, 8
            #k = 4
            #print(k)
            set_color = "#ff0000" if k > 0.9 else "#00ff00"
            colors = [set_color for _ in range(len(xx))]
            #u.append(np.unique(x[endcap]))
            #r.append(a * np.ones(len(u)))
            #pl.plot(r, u, 'k.', markersize=1)
            #pl.plot(r, u, c=colors, markersize=1)
            ax.scatter(xx, u, s=1, c=colors)

        pl.show()

    def test_sin() -> tuple[list, list]:
        x = np.linspace(0, t, int(fs*t), endpoint=False)
        signal = np.sin(x)

        return x, signal

    def f_random(x, a) -> list:
        return a * np.random.normal(scale=0.1, size=len(x)) * (1 - x)

    def test_random() -> tuple[list, list]:
        x = np.linspace(1, 100)
        signal = Chaos01.f_random(x, 4)

        return x, signal

    def logistic_map(start: float = 1.4, end: float = 4, values: int = 100) -> None:
        aline = np.linspace(start, end, values) # 1000
        N = 500
        x = 0.5 + np.zeros(N)
        endcap = np.arange(round(N * 0.9), N)
        colors = []
        fig = pl.figure()
        ax = fig.add_subplot(111)
        #u, r = [], []
        for a in aline:
            for n in range(N - 1):
                x[n + 1] = a * x[n] * (1 - x[n])
            #colors.append("#000000")

            u = np.unique(x[endcap])
            r = a * np.ones(len(u))
            k, Kc, PC, QC = Chaos01.execute(u, 1, 20)    # 2, 8
            #k = 4
            #print(k)
            set_color = "#ff0000" if k > 0.9 else "#00ff00"
            colors = [set_color for _ in range(len(r))]
            #u.append(np.unique(x[endcap]))
            #r.append(a * np.ones(len(u)))
            #pl.plot(r, u, 'k.', markersize=1)
            #pl.plot(r, u, c=colors, markersize=1)
            ax.scatter(r, u, s=1, c=colors)

        pl.show()

    def test_sin_chaos():
        fs = 10
        t = 10
        aline = np.linspace(0, t, int(fs*t), endpoint=False)
        N = 500
        x = 0.5 + np.zeros(N)
        endcap = np.arange(round(N * 0.9), N)
        colors = []
        fig = pl.figure()
        ax = fig.add_subplot(111)
        #u, r = [], []
        for a in aline:
            for n in range(N - 1):
                #x[n + 1] = a * x[n] * (1 - x[n])
                x[n + 1] = np.sin(a)
            #colors.append("#000000")

            u = np.unique(x[endcap])
            r = a * np.ones(len(u))
            k, Kc, PC, QC = Chaos01.execute(u, 1, 20)    # 2, 8
            #k = 4
            #print(k)
            set_color = "#ff0000" if k > 0.9 else "#00ff00"
            colors = [set_color for _ in range(len(r))]
            #u.append(np.unique(x[endcap]))
            #r.append(a * np.ones(len(u)))
            #pl.plot(r, u, 'k.', markersize=1)
            #pl.plot(r, u, c=colors, markersize=1)
            ax.scatter(r, u, s=1, c=colors)

        pl.show()

    def test_rand_chaos():
        aline = np.linspace(1, 100)
        N = 500
        x = 0.5 + np.zeros(N)
        endcap = np.arange(round(N * 0.9), N)
        colors = []
        fig = pl.figure()
        ax = fig.add_subplot(111)
        #u, r = [], []
        for a in aline:
            for n in range(N - 1):
                #x[n + 1] = a * x[n] * (1 - x[n])
                x[n + 1] = 4 * np.random.normal(scale=0.1) * (1 - a)    # np.random.normal(scale=0.1)  np.random.uniform(0, 1)
            #colors.append("#000000")

            u = np.unique(x[endcap])
            r = a * np.ones(len(u))
            k, Kc, PC, QC = Chaos01.execute(u, 1, 20)    # 2, 8
            #k = 4
            #print(k)
            set_color = "#ff0000" if k > 0.9 else "#00ff00"
            colors = [set_color for _ in range(len(r))]
            #u.append(np.unique(x[endcap]))
            #r.append(a * np.ones(len(u)))
            #pl.plot(r, u, 'k.', markersize=1)
            #pl.plot(r, u, c=colors, markersize=1)
            ax.scatter(r, u, s=1, c=colors)

        pl.show()

import matplotlib.pyplot as pl
import numpy as np

x = np.linspace(1, 100)

#fs = 44100
fs = 10
t = 10

#xsin = np.linspace(1, 10)
xsin = np.linspace(0, t, int(fs*t), endpoint=False)
#xsin = np.arange(t * fs) / fs

def f(x):
    return np.sin(x) + np.random.normal(scale=0.1, size=len(x))

def f2(x, a):
    return a * np.random.normal(scale=0.1, size=len(x)) * (1 - x)

def test_sin():
    x = np.linspace(0, t, int(fs*t), endpoint=False)
    signal = np.sin(x)

    return x, signal

def test_random():
    x = np.linspace(1, 100)
    signal = f2(x, 4)

    return x, signal

def logistic_map():
    aline = np.linspace(1.4, 4, 100) # 1000
    N = 500
    x = 0.5 + np.zeros(N)
    endcap = np.arange(round(N * 0.9), N)
    colors = []
    fig = pl.figure()
    ax = fig.add_subplot(111)
    #u, r = [], []
    for a in aline:
        for n in range(N - 1):
            x[n + 1] = a * x[n] * (1 - x[n])
        #colors.append("#000000")

        u = np.unique(x[endcap])
        r = a * np.ones(len(u))
        k, Kc, PC, QC = Chaos01.execute(u, 1, 20)    # 2, 8
        #k = 4
        #print(k)
        set_color = "#ff0000" if k > 0.9 else "#00ff00"
        colors = [set_color for _ in range(len(r))]
        #u.append(np.unique(x[endcap]))
        #r.append(a * np.ones(len(u)))
        #pl.plot(r, u, 'k.', markersize=1)
        #pl.plot(r, u, c=colors, markersize=1)
        ax.scatter(r, u, s=1, c=colors)

    pl.show()


#logistic_map()


#x, signal = test_sin()

#x, signal = Chaos01.test_sin()
#
#pl.plot(x, signal)
#pl.show()


#k, Kc, PC, QC = Chaos01.execute(signal)
#print("k: {}".format(k))
#print("k: {}\nKc: {}\nPC: {}\nQC: {}".format(k, Kc, PC, QC))

#Chaos01.test_rand_chaos()
"""ncut = 5
a = np.arange(1, ncut + 1).reshape(-1)
b = [i for i in range(1, ncut + 1)]
print(a, b)"""