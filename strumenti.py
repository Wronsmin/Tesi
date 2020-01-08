import numpy as np
from scipy.optimize import curve_fit
import pandas as pd
import os

pd.options.mode.chained_assignment = None

def Maxima(raw_data, Emin):
    data = raw_data.query('d > %d & a<b<c<d & d>e' %Emin) #filtraggio dei dati in modo da selezionare solo gli eventi che soddisfano la condizione del query
    #parametri della parabola generica di eq ax^2 + bx + c  
    popt = pd.DataFrame({'a': 0.5 * data['c'] + data['d'] + 0.5*data['e'],
                         'b': -0.5 * data['c'] + 0.5 * data['e'],
                         'c': data['d']})

    data.loc[:,'tmax'] = np.divide(-popt['b'], 2.*popt['a']) + 3
    data.loc[:,'Emax'] = np.divide(-np.power(popt['b'],2.), 4.*popt['a']) + popt['c']
    data.loc[:,'Emax05'] = np.multiply(data.Emax, 0.5)

    data['t_retta'] = 0

    #calcolo delle interpolazioni in base a dove capita Emax/2
    mask = (((data.a) <= (data.Emax05)) & ((data.Emax05) <= (data.b))) #a<Emax/2<b
    data.loc[mask, 't_retta'] = (data['Emax05'] - data['a']) * 1/(data['b'] - data['a'])

    mask = (((data.b) <= (data.Emax05)) & ((data.Emax05) <= (data.c))) #b<Emax/2<c
    data.loc[mask, 't_retta'] = (data['Emax05'] - data['b']) * 1/(data['c'] - data['b']) + 1

    mask = (((data.c) <= (data.Emax05)) & ((data.Emax05) <= (data.d))) #c<Emax/2<d
    data.loc[mask, 't_retta'] = (data['Emax05'] - data['c']) * 1/(data['d'] - data['c']) +2

    return data

def lettura_file(path):
    files = os.listdir(path)
    df_from_each_file = (pd.read_csv(path + f, sep=' ') for f in files)
    data = pd.concat(df_from_each_file, ignore_index = True)
    data = data.rename(columns={'1st_sample': 'a',
                                '2nd_sample': 'b',
                                '3rd_sample': 'c',
                                '4th_sample': 'd',
                                '5th_sample': 'e'}) #ho dovuto rinominare le colonne per problemi con il query
    return data

def pile_up(path):
    files = os.listdir(path)
    for i in files:
        data = pd.read_csv(path + i, sep=' ')
        data = data.rename(columns={'1st_sample': 'a',
                                    '2nd_sample': 'b',
                                    '3rd_sample': 'c',
                                    '4th_sample': 'd',
                                    '5th_sample': 'e'})
        data = data.query('a<b & b>c & c<d & d>e & b<d')
