from matplotlib.pyplot import *
import os
from strumenti import *

np.set_printoptions(suppress=True)
immagini='/mnt/c/Users/cosmi/Desktop/Python/Tesi/Immagini'
working = os.path.realpath('/mnt/c/Users/cosmi/Desktop/Python/Tesi/Dataset/160908/Peak_Finder')
list_path = []
total_data = 0
energie, tempi = [], []

for i in os.listdir(working):
    #list_path.append(working + '/' + i)
    timestamp, data = lettura_file(working + '/' + i)
    a, b = Maxima(timestamp, data)
    energie, tempi = energie + b, tempi + a
    total_data += len(timestamp)

title('Energia vs $\Delta t$')
ylabel('Energia')
xlabel('$\Delta$ t')
scatter(tempi, energie, s=3)
savefig(immagini + '/energia_vs_tempo.png')

title('Plot Energie')
ylabel('Energia')
xlabel('# evento')
plot(energie)
savefig(immagini + '/energie.png')

title('Plot Tempi')
ylabel('$\Delta$t')
xlabel('# evento')
plot(tempi)
savefig(immagini + '/tempi.png')

title('Istogramma Energie')
ylabel('Conteggi')
xlabel('Energia')
hist(energie, bins='auto')
savefig(immagini + '/hist_energie.png')

title('Istogramma Tempi')
ylabel('Conteggi')
xlabel('$\Delta$t')
hist(tempi, bins='auto')
savefig(immagini + '/hist_tempi.png')
