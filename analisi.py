import numpy as np
from scipy.signal import find_peaks
from scipy.optimize import curve_fit

def f(x, a, b, c):
    yield a * x ** 2 + b * x + c

def vertice(array):
    yield -array[1] / 2*array[0], -(array[1]**2 - 4*array[2]*array[2]) / 4*array[0]

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx, array[idx]

def Maxima():
    for i in FILE:
        x = readfile
        massimi, _ = find_peaks(x)
        #printare i dati per farsi una bella idea dell'andamento dei grafici

        for j in massimi:
            xdata = [j-1, j, j+1]
            popt, pcov = curve_fit(f, xdata, x[xdata])
            tmax, Emax = vertice(popt)
            t_needed, E_needed = find_nearest( x[t_max-10:t_max], Emax / 2.0)

