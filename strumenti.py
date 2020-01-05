import numpy as np
from scipy.optimize import curve_fit
import pandas as pd
import os

pd.options.mode.chained_assignment = None

def retta(x):
    return m * x + q

def interpolazione(E1, E2, Emax):
    #m = np.divide(E2 - E1, t2 - t1)
    #q = -t2 * m + E2
    #return -np.divide(q, m)
    return (Emax - E1) * 255/(E2-E1)

def parabola(x, a, b, c):
    return a * x ** 2 + b * x + c

def find_nearest(array, value):
    for i in array:
        if i < value:
            Emin = i
    pos = array.tolist().index(Emin)
    if array[pos] == array[pos + 1]:
        pos += 1
    return pos, Emin

def Maxima(raw_data, Emin):
    data = raw_data.query('d > %d & a<b<c<d & d>e' %Emin)

    popt = pd.DataFrame({'a': 0.5 * data['c'] + data['d'] + 0.5*data['e'],
                         'b': -0.5 * data['c'] + 0.5 * data['e'],
                         'c': data['d']})

    data.loc[:,'tmax'] = np.divide(-popt['b'], 2.*popt['a']) + 3
    data.loc[:,'Emax'] = np.divide(-np.power(popt['b'],2.), 4.*popt['a']) + popt['c']
    data.loc[:,'Emax05'] = np.multiply(data.Emax, 0.5)

    data['t_retta'] = 0

    mask = (((data.a) <= (data.Emax05)) & ((data.Emax05) <= (data.b))) 
    data.loc[mask, 't_retta'] = (data['Emax05'] - data['a']) * 1/(data['b'] - data['a'])

    mask = (((data.b) <= (data.Emax05)) & ((data.Emax05) <= (data.c)))
    data.loc[mask, 't_retta'] = (data['Emax05'] - data['b']) * 1/(data['c'] - data['b']) + 1

    mask = (((data.c) <= (data.Emax05)) & ((data.Emax05) <= (data.d)))
    data.loc[mask, 't_retta'] = (data['Emax05'] - data['c']) * 1/(data['d'] - data['c']) +2

    return data

def lettura_file(path):
    files = os.listdir(path)
    df_from_each_file = (pd.read_csv(path + f, sep=' ') for f in files)
    data = pd.concat(df_from_each_file, ignore_index = True)
    data = data.rename(columns={'1st_sample': 'a', '2nd_sample': 'b', '3rd_sample': 'c', '4th_sample': 'd','5th_sample': 'e'})
    return data
