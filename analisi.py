from matplotlib.pyplot import *
import os
from strumenti import *

np.set_printoptions(suppress=True)

immagini='/mnt/c/Users/cosmi/Desktop/Python/Tesi/Immagini'
working_linux = os.path.realpath('/mnt/c/Users/cosmi/Desktop/Python/Tesi/Dataset/160908/Peak_Finder')
list_path = []
total_data = 0
timestamp, data = [], []
energie, tempi = [], []

for i in os.listdir(working):
    timestamp, data += lettura_file(working + '/' + i)

E_min = [20, 30, 40, 50]

for i in E_min:
    energie, tempi = Maxima(timestamp, data, E_min)

    title('Energia vs $\Delta t$')
    ylabel('Energia')
    xlabel('$\Delta$ t')
    scatter(tempi, energie, s=3)
    savefig(immagini + "/E_min"  + str(i)  + '/energia_vs_tempo.png')
    show()

    title('Plot Energie')
    ylabel('Energia')
    xlabel('# evento')
    plot(energie)
    savefig(immagini + "/E_min"  + str(i)  + '/energie.png')
    show()

    title('Plot Tempi')
    ylabel('$\Delta$t')
    xlabel('# evento')
    plot(tempi)
    savefig(immagini + "/E_min"  + str(i)  + '/tempi.png')
    show()

    title('Istogramma Energie')
    ylabel('Conteggi')
    xlabel('Energia')
    hist(energie, bins='auto')
    savefig(immagini + "/E_min"  + str(i)  + '/hist_energie.png')
    show()

    title('Istogramma Tempi')
    ylabel('Conteggi')
    xlabel('$\Delta$t')
    hist(tempi, bins='auto')
    savefig(immagini + "/E_min"  + str(i)  + '/hist_tempi.png')
    show()

