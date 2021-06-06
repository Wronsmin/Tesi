import pandas as pd
import os
import pandas as pd
from matplotlib.pyplot import *
from parse import parse
from scipy.stats import *


def Maxima(raw_data, Emin, Emax):
    data = raw_data.query(f'd< {Emax}')
    data = data.query(
        f'd > {Emin} & a<b<c<d & d>e')  # filtraggio dei dati in modo da selezionare solo gli eventi che soddisfano la condizione del query

    # parametri della parabola generica di eq ax^2 + bx + c
    popt = pd.DataFrame({'a': 0.5 * data['c'] - data['d'] + 0.5 * data['e'],
                         'b': -0.5 * data['c'] + 0.5 * data['e'],
                         'c': data['d']})

    data.loc[:, 'tmax'] = 4 + np.divide(-popt['b'], 2. * popt['a'])
    data.loc[:, 'Emax'] = np.divide(-np.power(popt['b'], 2.), 4. * popt['a']) + popt['c']

    data['t_s'] = 0

    # calcolo delle interpolazioni in base a dove capita Emax/2
    mask = (((data.a) <= (data.Emax * 0.5)) & ((data.Emax * 0.5) <= (data.b)))  # a<Emax/2<b
    data.loc[mask, 't_s'] = (data['Emax'] * 0.5 - data['a']) * 1 / (data['b'] - data['a']) + 1

    mask = (((data.b) <= (data.Emax * 0.5)) & ((data.Emax * 0.5) <= (data.c)))  # b<Emax/2<c
    data.loc[mask, 't_s'] = (data['Emax'] * 0.5 - data['b']) * 1 / (data['c'] - data['b']) + 2

    mask = (((data.c) <= (data.Emax * 0.5)) & ((data.Emax * 0.5) <= (data.d)))  # c<Emax/2<d
    data.loc[mask, 't_s'] = (data['Emax'] * 0.5 - data['c']) * 1 / (data['d'] - data['c']) + 3

    # calcolo delle interpolazioni in base a dove capita Emax/2
    data['finetime'] = 0
    mask = (((data.a) <= (data.Emax * 0.5)) & ((data.Emax * 0.5) <= (data.b)))  # a<Emax/2<b
    data.loc[mask, 'finetime'] = (data['Emax'] * 0.5 - data['a']) * 255 / (data['b'] - data['a'])

    mask = (((data.b) <= (data.Emax * 0.5)) & ((data.Emax * 0.5) <= (data.c)))  # b<Emax/2<c
    data.loc[mask, 'finetime'] = (data['Emax'] * 0.5 - data['b']) * 255 / (data['c'] - data['b'])

    mask = (((data.c) <= (data.Emax * 0.5)) & ((data.Emax * 0.5) <= (data.d)))  # c<Emax/2<d
    data.loc[mask, 'finetime'] = (data['Emax'] * 0.5 - data['c']) * 255 / (data['d'] - data['c'])

    data['delta t'] = data['tmax'] - data['t_s']

    return data


def lettura_file(path):
    files = os.listdir(path)
    df_from_each_file = (pd.read_csv(path + f, sep=' ') for f in files)
    data = pd.concat(df_from_each_file, ignore_index=True)
    data = data.rename(columns={'1st_sample': 'a',
                                '2nd_sample': 'b',
                                '3rd_sample': 'c',
                                '4th_sample': 'd',
                                '5th_sample': 'e'})  # ho dovuto rinominare le colonne per problemi con il query
    return data


def picchi(path):
    for i, f in enumerate(os.listdir(path)):
        data = pd.read_csv(path + f, sep=' ')
        data = data.rename(columns={'1st_sample': 'a',
                                    '2nd_sample': 'b',
                                    '3rd_sample': 'c',
                                    '4th_sample': 'd',
                                    '5th_sample': 'e'})
        data = data.query('d< 256')
        data = data.query('d > 64 & a<b<c<d & d>e')
        pattern = 'peak_finder_dump_fifo_1ch_lkrl0-fe-1{code}_Thu__08_Sep_2016_15-28-46.csv'
        c = parse(pattern, f)
        os.makedirs(os.getcwd() + '/Picchi/', exist_ok=True)
        if 'a' in c['code']:
            data.to_csv(os.getcwd() + '/Picchi/' + '%.2d%s.csv' % (i + 14, c['code']), sep=' ')
        elif 'b' in c['code']:
            data.to_csv(os.getcwd() + '/Picchi/' + '%.2d%s.csv' % (27 - i, c['code']), sep=' ')
        else:
            pass
    return None


def analisi(raw_data, E_min, E_max):
    folder_path = os.getcwd()
    immagini = folder_path + '/Immagini'
    o = 0

    for i, j in zip(E_min, E_max):
        data = Maxima(raw_data, i, j)
        tempi = np.asarray(abs(data['delta t'])) * 25
        PATH = immagini + "/E_min" + str(i)
        os.makedirs(PATH, exist_ok=True)
        o = o + 1

        title('Istogramma Finetime\n ($%2.1f<E<%2.1f$ GeV , Conteggi totali = %d / %d) ' % (
        i * 0.056, j * 0.056, len(data), len(raw_data)))
        ylabel('Conteggi')
        xlabel('Finetime')
        hist(data['finetime'], bins=32, alpha=0.70)
        savefig(PATH + '/hist_finetime%d.png' % o)
        close()

        n, bin_edges, patches = hist(tempi, bins='auto', density=True, alpha=0.75)
        (mu, sigma) = norm.fit(tempi)
        x = np.arange(min(bin_edges) - 0.5, max(bin_edges) + 0.5, 1 / len(data))
        y = norm.pdf(x, mu, sigma)
        plot(x, y, color='red', label='Gaussiana')

        title('$\mathrm{Distribuzione\ Tempi}$ \n ($%2.1f<E<%2.1f$ GeV, Conteggi totali = %d / %d) ' % (
        i * 0.056, j * 0.056, len(data), len(raw_data)))
        ylabel('Probabilità')
        xlabel('$\Delta$t (ns)')
        legend()
        # p = legend().get_window_extent()  # per grafici migliori
        draw()

        # legenda per Gaussiana
        textstr = '\n'.join((
            r'$\mu=%.2f$' % (mu,),
            r'$\sigma=%.2f$' % (sigma,)))
        props = dict(boxstyle='round', facecolor='red', alpha=0.4)
        # text(p.p0[0]+5,p.p0[1]-10, textstr, fontsize=9, verticalalignment='top', bbox=props, transform=None)

        savefig(PATH + '/hist_tempi%d.png' % o)
        close()
    return None


def energie(raw_data):
    data = raw_data.query('d > 0 & a<b<c<d & d>e')

    popt = pd.DataFrame({'a': 0.5 * data['c'] - data['d'] + 0.5 * data['e'],
                         'b': -0.5 * data['c'] + 0.5 * data['e'],
                         'c': data['d']})

    data.loc[:, 'tmax'] = 4 + np.divide(-popt['b'], 2. * popt['a'])
    data.loc[:, 'Emax'] = np.divide(-np.power(popt['b'], 2.), 4. * popt['a']) + popt['c']

    data['t_s'] = 0

    # calcolo delle interpolazioni in base a dove capita Emax/2
    mask = (((data.a) <= (data.Emax * 0.5)) & ((data.Emax * 0.5) <= (data.b)))  # a<Emax/2<b
    data.loc[mask, 't_s'] = (data['Emax'] * 0.5 - data['a']) * 1 / (data['b'] - data['a']) + 1

    mask = (((data.b) <= (data.Emax * 0.5)) & ((data.Emax * 0.5) <= (data.c)))  # b<Emax/2<c
    data.loc[mask, 't_s'] = (data['Emax'] * 0.5 - data['b']) * 1 / (data['c'] - data['b']) + 2

    mask = (((data.c) <= (data.Emax * 0.5)) & ((data.Emax * 0.5) <= (data.d)))  # c<Emax/2<d
    data.loc[mask, 't_s'] = (data['Emax'] * 0.5 - data['c']) * 1 / (data['d'] - data['c']) + 3

    data['delta t'] = data['tmax'] - data['t_s']

    folder_path = os.getcwd()
    immagini = folder_path + '/Immagini'

    hist(data['Emax'] * 0.056, bins='auto', alpha=0.75)
    title('$\mathrm{Istogramma\ Energie}$ \n (E>%2.1f GeV, Conteggi totali = %d / %d) ' % (
    20 * 0.056, len(data), len(raw_data)))
    yscale('log')
    ylabel('Conteggi')
    xlabel('Energia (GeV)')
    savefig(immagini + '/hist_energie.png')
    close()
    return None
