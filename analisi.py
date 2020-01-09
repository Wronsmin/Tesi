from matplotlib.pyplot import *
import os.path
from strumenti import *
from scipy.stats import *

np.set_printoptions(suppress=True)

folder_path = os.getcwd()
immagini= folder_path + '/Immagini'
path = folder_path + '/Dataset/160908/Peak_Finder/'

E_min = [180] #incrementare a passi di 64

raw_data = lettura_file(path)
raw_data = raw_data.query('d < 256')

for i in E_min:
    data = Maxima(raw_data, i)
    tempi = np.asarray(abs(data['tmax']-data['t_retta'])) * 25
    PATH = immagini + "/E_min"  + str(i)
    os.makedirs(PATH, exist_ok=True)

    title('Energia vs $\Delta t$')
    ylabel('Energia')
    xlabel('$\Delta$ t (ns)')
    scatter(data['tmax']-data['t_retta'], data['Emax'], s=3)
    savefig(PATH + '/energia_vs_tempo.png')
    close()

    title('Plot Energie')
    ylabel('Energia')
    xlabel('# evento')
    plot(data['Emax'])
    savefig(PATH + '/energie.png')
    close()

    title('Plot Tempi')
    ylabel('$\Delta$t (ns)')
    xlabel('# evento')
    plot(data['tmax']-data['t_retta'])
    savefig(PATH + '/tempi.png')
    close()

    title('Istogramma max')
    ylabel('Probabilità')
    xlabel('Energia')
    #yscale('log')
    hist(data['tmax'], bins='auto')
    savefig(PATH + '/hist_energie.png')
    close()

    n , bin_edges, patches = hist(tempi, bins = 'auto', density = True)
    (mu, sigma) = norm.fit(tempi)
    x = np.arange(min(bin_edges)-0.5, max(bin_edges)+0.5, 1/len(data))
    y = norm.pdf(x, mu, sigma)
    print(mu, sigma)

    textstr = '\n'.join((
        r'$\mu=%.2f$' % (mu, ),
        r'$\sigma=%.2f$' % (sigma, )))
    props = dict(boxstyle='round', facecolor='red', alpha=0.4)
    text(int(max(bin_edges))-4, 0.11, textstr, fontsize=9, verticalalignment='top', bbox=props)

    plot(x, y, color='red', label='Gaussiana')
    title('$\mathrm{Istogramma\ Tempi}$ \n ($ E_{min}>%d$, Conteggi totali = %d / %d) ' %(i, len(data), len(raw_data)) )
    ylabel('Probabilità')
    xlabel('$\Delta$t (ns)')
    legend()
    savefig(PATH + '/hist_tempi.png')
    close()
