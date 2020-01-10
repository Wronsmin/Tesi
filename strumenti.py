import numpy as np
from scipy.optimize import curve_fit
import pandas as pd
import os
from parse import parse

pd.options.mode.chained_assignment = None

def Maxima(raw_data, Emin, Emax):
    data = raw_data.query('d< %d' %Emax)
    data = raw_data.query('d > %d & a<b<c<d & d>e' %Emin) #filtraggio dei dati in modo da selezionare solo gli eventi che soddisfano la condizione del query
    #parametri della parabola generica di eq ax^2 + bx + c  
    popt = pd.DataFrame({'a': 0.5 * data['c'] - data['d'] + 0.5*data['e'],
                         'b': -0.5 * data['c'] + 0.5 * data['e'],
                         'c': data['d']})

    data.loc[:,'tmax'] = np.divide(-popt['b'], 2.*popt['a'])
    data.loc[:,'Emax'] = np.divide(-np.power(popt['b'],2.), 4.*popt['a']) + popt['c']
    data.loc[:,'Emax05'] = np.multiply(data.Emax, 0.5)

    data['t_retta'] = 0

    #calcolo delle interpolazioni in base a dove capita Emax/2
    mask = (((data.a) <= (data.Emax05)) & ((data.Emax05) <= (data.b))) #a<Emax/2<b
    data.loc[mask, 't_retta'] = (data['Emax05'] - data['a']) * 1/(data['b'] - data['a']) -3

    mask = (((data.b) <= (data.Emax05)) & ((data.Emax05) <= (data.c))) #b<Emax/2<c
    data.loc[mask, 't_retta'] = (data['Emax05'] - data['b']) * 1/(data['c'] - data['b']) -2

    mask = (((data.c) <= (data.Emax05)) & ((data.Emax05) <= (data.d))) #c<Emax/2<d
    data.loc[mask, 't_retta'] = (data['Emax05'] - data['c']) * 1/(data['d'] - data['c']) -1

#calcolo delle interpolazioni in base a dove capita Emax/2
    data['finetime'] = 0
    mask = (((data.a) <= (data.Emax05)) & ((data.Emax05) <= (data.b))) #a<Emax/2<b
    data.loc[mask, 'finetime'] = (data['Emax05'] - data['a']) * 255/(data['b'] - data['a'])

    mask = (((data.b) <= (data.Emax05)) & ((data.Emax05) <= (data.c))) #b<Emax/2<c
    data.loc[mask, 'finetime'] = (data['Emax05'] - data['b']) * 255/(data['c'] - data['b'])

    mask = (((data.c) <= (data.Emax05)) & ((data.Emax05) <= (data.d))) #c<Emax/2<d
    data.loc[mask, 'finetime'] = (data['Emax05'] - data['c']) * 255/(data['d'] - data['c'])

    data['delta t'] = data['tmax'] - data['t_retta']

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
       data = data[~ (((data.a)<(data.b))&((data.b)<(data.c))&((data.c)<(data.d)))]
       pattern = 'peak_finder_dump_fifo_1ch_lkrl0-fe-{code}_Thu__08_Sep_2016_15-28-46.csv'
       c = parse(pattern, i)
       os.makedirs(os.getcwd() + '/Pile_Up/', exist_ok=True)
       data.to_csv(os.getcwd() + '/Pile_Up/' + '%s.csv' %(c['code']), sep= ' ')
