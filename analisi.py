from matplotlib.pyplot import *
import matplotlib.mlab as mlab
import os
from strumenti import *
from scipy.stats import *

np.set_printoptions(suppress=True)

immagini='/mnt/c/Users/cosmi/Desktop/Python/Tesi/Immagini'
working = os.path.realpath('/mnt/c/Users/cosmi/Desktop/Python/Tesi/Dataset/160908/Peak_Finder')
list_path = []
total_data = 0
timestamp, data = [], []

E_min = [20, 30, 40, 200]

for i in os.listdir(working):
    a, b = lettura_file(working + '/' + i)
    timestamp.extend(a), data.extend(b)

for i in E_min:
    tempi, energie = Maxima(timestamp, data, i) 
    tempi = np.asarray(tempi) * 25

    title('Energia vs $\Delta t$')
    ylabel('Energia')
    xlabel('$\Delta$ t (ns)')
    scatter(tempi, energie, s=3)
    savefig(immagini + "/E_min"  + str(i)  + '/energia_vs_tempo.png')
    close()

    title('Plot Energie')
    ylabel('Energia')
    xlabel('# evento')
    plot(energie)
    savefig(immagini + "/E_min"  + str(i)  + '/energie.png')
    close()

    title('Plot Tempi')
    ylabel('$\Delta$t (ns)')
    xlabel('# evento')
    plot(tempi)
    savefig(immagini + "/E_min"  + str(i)  + '/tempi.png')
    close()

    title('Istogramma Energie')
    ylabel('Probabilità')
    xlabel('Energia')
    hist(energie, bins='auto')
    savefig(immagini + "/E_min"  + str(i)  + '/hist_energie.png')
    close()

    n , bin_edges, patches = hist(tempi, bins = 'auto', normed = True)
    (mu, sigma) = norm.fit(tempi)
    x = np.arange(min(bin_edges)-0.5, max(bin_edges)+0.5, 1/len(tempi))
    y = mlab.normpdf(x, mu, sigma)
    param = gamma.fit(tempi)
    mean, var = gamma.mean(*param), gamma.var(*param)

    textstr = '\n'.join((
        r'$\mu=%.2f$' % (mu, ),
        r'$\sigma=%.2f$' % (sigma, )))
    props = dict(boxstyle='round', facecolor='red', alpha=0.4)
    text(int(max(bin_edges))-4, 0.045, textstr, fontsize=9, verticalalignment='top', bbox=props)

    plot(x, y, color='red', label='Gaussiana')
    y = gamma.pdf(x, *param)

    textstr = '\n'.join((
        r'$\mu=%.2f$' % (mean, ),
        r'$\sigma=%.2f$' % (var, )))
    props = dict(boxstyle='round', facecolor='orange', alpha=0.4)
    text(int(max(bin_edges))-4, 0.038, textstr, fontsize=9, verticalalignment='top', bbox=props)

    plot(x, y, color='orange', label='Gamma')
    title('$\mathrm{Istogramma\ Tempi}$ \n ($ E_{min}>%d$, Conteggi totali = %d) ' %(i, len(tempi)) )
    ylabel('Probabilità')
    xlabel('$\Delta$t (ns)')
    legend()
    savefig(immagini + "/E_min"  + str(i)  + '/hist_tempi.png')
    close()
    #print(sum(n))

