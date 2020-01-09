from matplotlib.pyplot import *
import os.path
from strumenti import *
from scipy.stats import *

np.set_printoptions(suppress=True)

folder_path = os.getcwd()
immagini= folder_path + '/Immagini'
path = folder_path + '/Dataset/160908/Peak_Finder/'

E_min = [64,128,192] #incrementare a passi di 64

raw_data = lettura_file(path)
raw_data = raw_data.query('d < 256')

for i in E_min:
    data = Maxima(raw_data, i)
    tempi = np.asarray(abs(data['tmax']-data['t_retta'])) * 25
    PATH = immagini + "/E_min"  + str(i)
    os.makedirs(PATH, exist_ok=True)

    title('Istogramma Finetime')
    ylabel('Probabilità')
    xlabel('Energia')
    #yscale('log')
    hist(data['finetime'], bins=256)
    savefig(PATH + '/hist_finetime.png')
    close()

    n , bin_edges, patches = hist(tempi, bins = 'auto', density = True)
    (mu, sigma) = norm.fit(tempi)
    x = np.arange(min(bin_edges)-0.5, max(bin_edges)+0.5, 1/len(data))
    y = norm.pdf(x, mu, sigma)

    textstr = '\n'.join((
        r'$\mu=%.2f$' % (mu, ),
        r'$\sigma=%.2f$' % (sigma, )))
    props = dict(boxstyle='round', facecolor='red', alpha=0.4)
    text(int(max(bin_edges))-4, 0.05, textstr, fontsize=9, verticalalignment='top', bbox=props)

    plot(x, y, color='red', label='Gaussiana')
    title('$\mathrm{Istogramma\ Tempi}$ \n ($ E_{min}>%d$, Conteggi totali = %d / %d) ' %(i, len(data), len(raw_data)) )
    ylabel('Probabilità')
    xlabel('$\Delta$t (ns)')
    legend()
    savefig(PATH + '/hist_tempi.png')
    close()
