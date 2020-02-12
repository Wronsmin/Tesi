import os.path
import pandas as pd
from matplotlib.pyplot import *
from matplotlib.table import Table
from collections import Counter

folder_path = os.getcwd()
file_path = folder_path + '/Picchi'

x= []
y = []
interv = [13,26,39,56]

colori = ['grey', 'gold', 'orange', 'red']
for i, f in enumerate(os.listdir(file_path)):
    data = pd.read_csv(file_path + '/' + f, sep= ' ')

    for j in range(len(data)):
        if data.loc[j,'fpga'] == 'PP0':
            x.append(i), y.append(data.loc[j,'channel'])
        elif data.loc[j,'fpga'] == 'PP1':
            x.append(i), y.append(data.loc[j,'channel']+8)
        elif data.loc[j,'fpga'] == 'PP2':
            x.append(i), y.append(data.loc[j,'channel']+16)
        elif data.loc[j,'fpga'] == 'PP3':
            x.append(i), y.append(data.loc[j,'channel']+24)
        else: pass

combos = list(zip(x, y))
unici = list(set(combos))
counts = Counter(combos)
frequenze = []
colors = []
for i in unici:
    frequenze.append(counts[i])

for i in frequenze:
    if 0 <= i < interv[0]:
        colors.append(colori[0])
    elif interv[0] <= i < interv[1]:
        colors.append(colori[1])
    elif interv[1] <= i < interv[2]:
        colors.append(colori[2])
    elif interv[2] <= i <= interv[3]:
        colors.append(colori[3])

unici= list(zip(*unici))
scatter(unici[0], unici[1], c=colors) #, marker='s'
show()
