from matplotlib.pyplot import *
import os.path
from strumenti import *
from scipy.stats import *

pd.options.mode.chained_assignment = None
np.set_printoptions(suppress=True)

folder_path = os.getcwd()
immagini= folder_path + '/Immagini'
path = folder_path + '/Dataset/160908/Peak_Finder/'

E_min = [64,128,192]
E_max = [128,192,256]

raw_data = lettura_file(path)

for i,j in zip(E_min, E_max):
    #pile_up(path, j, i)

    data = Maxima(raw_data, i,j)
    tempi = np.asarray(abs(data['tmax']-data['t_retta'])) * 25
    PATH = immagini + "/E_min"  + str(i)
    os.makedirs(PATH, exist_ok=True)

    title('Istogramma Finetime\n ($%2.1f<E<%2.1f$ GeV , Conteggi totali = %d / %d) ' %(i*0.056,j*0.056, len(data), len(raw_data)))
    ylabel('Conteggi')
    xlabel('Finetime')
    #yscale('log')
    hist(data['finetime'], bins=256, alpha=0.70)
    savefig(PATH + '/hist_finetime.png')
    close()

    n , bin_edges, patches = hist(tempi, bins = 'auto', density = True, alpha=0.70)
    hist(data['finetime'], bins=256, alpha=0.75)
    #savefig(PATH + '/hist_finetime.png')
    close()

    n , bin_edges, patches = hist(tempi, bins = 'auto', density = True, alpha=0.75)
    (mu, sigma) = norm.fit(tempi)
    x = np.arange(min(bin_edges)-0.5, max(bin_edges)+0.5, 1/len(data))
    y = norm.pdf(x, mu, sigma)
    plot(x, y, color='red', label='Gaussiana')

    title('$\mathrm{Istogramma\ Tempi}$ \n ($%2.1f<E<%2.1f$ GeV, Conteggi totali = %d / %d) ' %(i*0.056,j*0.056, len(data), len(raw_data)) )
    ylabel('Probabilità')
    xlabel('$\Delta$t (ns)')
    legend()
    draw()
    p = legend().get_window_extent() #per grafici migliori

    #legenda per Gaussiana
    textstr = '\n'.join((
        r'$\mu=%.2f$' % (mu, ),
        r'$\sigma=%.2f$' % (sigma, )))
    props = dict(boxstyle='round', facecolor='red', alpha=0.4)
    text(p.p0[0]+5,p.p0[1]-10, textstr, fontsize=9, verticalalignment='top', bbox=props, transform=None)

    savefig(PATH + '/hist_tempi.png')
    close()
