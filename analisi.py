import os.path
from strumenti import *


pd.options.mode.chained_assignment = None
np.set_printoptions(suppress=True)

folder_path = os.getcwd()
immagini= folder_path + '/Immagini'
path = folder_path + '/Dataset/160908/Peak_Finder/'

E_min = [64,128,192]
E_max = [128,192,256]

raw_data = lettura_file(path)

analisi(raw_data, E_min, E_max)

picchi(path)
