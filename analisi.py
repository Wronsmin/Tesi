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

    title('Istogramma Finetime\n ($ E_{min}>%d$, Conteggi totali = %d / %d) ' %(i, len(data), len(raw_data)))
    ylabel('Conteggi')
    xlabel('Finetime')
    #yscale('log')
    hist(data['finetime'], bins=256)
    savefig(PATH + '/hist_finetime.png')
    close()

    n , bin_edges, patches = hist(tempi, bins = 'auto', density = True)
    (mu, sigma) = norm.fit(tempi)
    x = np.arange(min(bin_edges)-0.5, max(bin_edges)+0.5, 1/len(data))
    y = norm.pdf(x, mu, sigma)
    plot(x, y, color='red', label='Gaussiana')

    param = gamma.fit(tempi)
    mean, var = gamma.mean(*param), gamma.var(*param)
    y = gamma.pdf(x, *param)

    plot(x, y, color='orange', label='Gamma')

    title('$\mathrm{Istogramma\ Tempi}$ \n ($ E_{min}>%d$, Conteggi totali = %d / %d) ' %(i, len(data), len(raw_data)) )
    ylabel('Probabilità')
    xlabel('$\Delta$t (ns)')
    legend()
    draw()
    p = legend().get_window_extent()

    #legenda per Gaussiana
    textstr = '\n'.join((
        r'$\mu=%.2f$' % (mu, ),
        r'$\sigma=%.2f$' % (sigma, )))
    props = dict(boxstyle='round', facecolor='red', alpha=0.4)
    text(p.p0[0]+5,p.p0[1]-10, textstr, fontsize=9, verticalalignment='top', bbox=props, transform=None)

    #legenda per Gamma
    textstr = '\n'.join((
       r'$\mu=%.2f$' % (mean, ),
       r'$\sigma=%.2f$' % (var, )))
    props = dict(boxstyle='round', facecolor='orange', alpha=0.4)
    text(p.p0[0]+5,p.p0[1]-54, textstr, fontsize=9, verticalalignment='top', bbox=props, transform=None)

    savefig(PATH + '/hist_tempi.png')
    close()
