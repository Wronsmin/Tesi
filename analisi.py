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

    title('Energia vs $\Delta t$')
    ylabel('Energia')
    xlabel('$\Delta$ t')
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
    ylabel('$\Delta$t')
    xlabel('# evento')
    plot(tempi)
    savefig(immagini + "/E_min"  + str(i)  + '/tempi.png')
    close()

    title('Istogramma Energie')
    ylabel('Conteggi')
    xlabel('Energia')
    hist(energie, bins='auto')
    savefig(immagini + "/E_min"  + str(i)  + '/hist_energie.png')
    close()

    n , bin_edges, patches = hist(tempi, bins = 30, normed = True)
    (mu, sigma) = norm.fit(tempi)
    x = np.arange(1, 3, 1/len(tempi))
    y = mlab.normpdf( x, mu, sigma)
    plot(x, y)
    title('$\mathrm{Istogramma\ Tempi}\ \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
    ylabel('Conteggi')
    xlabel('$\Delta$t')
    savefig(immagini + "/E_min"  + str(i)  + '/hist_tempi.png')
    close()

