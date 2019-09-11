import numpy as np
import pandas as pd
import os
from scipy.optimize import curve_fit
from matplotlib.pyplot import *
import matplotlib.pyplot as plt

def retta(x, a, b):
    return a * x + b

def parabola(x, c, d, e):
    return c * x ** 2 + d * x + e

def Maxima(time, data):

    for index, i in enumerate(data):
        maximum = np.argmax(i)
        xdata1 = [0, 1]
        xdata2 = [2, 3, 4]
        if all(  [maximum == 3,
                 i[maximum] > 20,
                 i[0]<i[1]<i[2]<i[3],
                 i[3] > i[4] ]
                ):
            p_retta, _ = curve_fit(retta, xdata1, i[0:1])
            p_parab, _ = curve_fit(parabola, xdata2, i[maximum-1:maximum+2])
            plot(i)
            plot(np.arange(0, 1,2000), retta(np.arange(0, 1,2000), p_retta[0], p_retta[1]))
            plot(np.arange(1,5,2000), parabola(np.arange(1,5,2000), p_parab[0], p_parab[1], p_parab[2]))
            show()

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

tmp = 'peak_finder_dump_fifo_1ch_lkrl0-fe-1a01_Thu__08_Sep_2016_15-28-46.csv'
timestamp, data = lettura_file(tmp)
Maxima(timestamp, data)
