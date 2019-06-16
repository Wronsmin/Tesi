import numpy as np
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
import pandas as pd
import os

np.set_printoptions(suppress=True)

def f(x, a, b, c):
    return a * x ** 2 + b * x + c

def vertice(array):
    return -array[1] / 2*array[0], -(array[1]**2 - 4*array[2]*array[2]) / 4*array[0]

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx, array[idx]

def Maxima(time, data):
    for index, i in enumerate(data):
        maximum = np.argmax(i)
        xdata = [time[index], time[index], time[index]]
        popt, pcov = curve_fit(f, i[maximum-1:maximum+1])
        tmax, Emax = vertice(popt)
        t_needed, E_needed = find_nearest( data[t_max-10:t_max], Emax / 2.0)

def lettura_file():
    #working = os.path.realpath('/run/media/wronsmin/Storage/Dataset/160908/Peak_Finder')
    #list_path = []
    #for i in os.listdir(working):
    #    list_path.append(working + '/' + i)

    data = pd.read_csv('peak_finder_dump_fifo_1ch_lkrl0-fe-1a01_Thu__08_Sep_2016_15-28-46.csv', sep=' ')

    data = np.transpose(data.values)
    data = data.tolist()
    timestamp = data[14]; del data[14]; time = np.asarray(time)
    del data[0:9]
    data = np.transpose(np.asarray(data, dtype=np.float64))
    data = pd.DataFrame(data)
    data = data[data.columns[::-1]]
    data = data.values
    return timestamp, data

#main program
if __main__=="__main__"
