import numpy as np
from scipy.optimize import curve_fit
import pandas as pd
import os
from matplotlib.pyplot import *
import matplotlib.pyplot as plt

np.set_printoptions(suppress=True)

Risultati_parabola = []
Risultati_retta = []

def retta(x):
    return m * x + q

def interpolazione(t1, t2, E1, E2):
    m = np.divide(E2 - E1, t2 - t1)
    q = -t2 * m + E2
    return -np.divide(q, m)

def parabola(x, a, b, c):
    return a * x ** 2 + b * x + c

def vertice(array):
    return np.divide(-array[1], 2.*array[0]), np.divide(-np.power(array[1],2.), 4.*array[0]) + array[2]

def find_nearest(array, value):
    for i in array:
        if i < value:
            Emin = i
    pos = array.tolist().index(Emin)
    if array[pos] == array[pos + 1]:
        pos += 1
    return pos, Emin

def Maxima(time, data):
    global Risultati_retta, Risultati_parabola

    for index, i in enumerate(data):
        maximum = np.argmax(i)
        xdata = [2, 3, 4]
        if all( [maximum == 3,
                i[maximum] > 20,
                i[0]<i[1]<i[2]<i[3],
                i[3] > i [4]]
                ):
            popt, _ = curve_fit(parabola, xdata, i[maximum-1:maximum+2])
            tmax, Emax = vertice(popt)
            t_needed, E_needed = find_nearest(i[0:4], Emax / 2.0)
            t_retta = interpolazione(t_needed, t_needed + 1, i[t_needed], i[t_needed + 1])
            Risultati_retta.append(t_retta), Risultati_parabola.append([tmax, Emax])
            np.savez('risutati.npz', np.array(Risultati_retta), np.array(Risultati_parabola))
        else:
            pass

def lettura_file(files):
    data = pd.read_csv(files, sep=' ')
    data = np.transpose(data.values)
    data = data.tolist()
    timestamp = data[14]; del data[14]; time = np.asarray(timestamp)
    del data[0:9]
    data = np.transpose(np.asarray(data, dtype=np.float64))
    data = pd.DataFrame(data)
    data = data.values
    return timestamp, data

if __name__ == '__main__':
    #working = os.path.realpath('/run/media/wronsmin/Storage/Dataset/160908/Peak_Finder')
    #list_path = []
    #for i in os.listdir(working):
    #    list_path.append(working + '/' + i)

    tmp = 'peak_finder_dump_fifo_1ch_lkrl0-fe-1a01_Thu__08_Sep_2016_15-28-46.csv'
    timestamp, data = lettura_file(tmp)
    Maxima(timestamp, data)
