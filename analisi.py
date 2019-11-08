from matplotlib.pyplot import *
from strumenti import *

np.set_printoptions(suppress=True)

if __name__ == '__main__':
    #working = os.path.realpath('/run/media/wronsmin/Storage/Dataset/160908/Peak_Finder')
    #list_path = []
    #for i in os.listdir(working):
    #    list_path.append(working + '/' + i)

    tmp = 'peak_finder_dump_fifo_1ch_lkrl0-fe-1a01_Thu__08_Sep_2016_15-28-46.csv'
    timestamp, data = lettura_file(tmp)
    tempi, energie = Maxima(timestamp, data)
    plot(energie)
    show()
