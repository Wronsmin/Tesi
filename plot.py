import os.path
from collections import Counter
import matplotlib.patches as mpatches
import pandas as pd
from matplotlib.pyplot import *

folder_path = os.getcwd()
file_path = folder_path + '/Picchi'

x= []
y = []
interv = [3,13,26,39,56]

colori = ['w', 'grey', 'gold', 'orange', 'red']
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
    elif interv[2] <= i < interv[3]:
        colors.append(colori[3])
    elif interv[3] <= i <= interv[4]:
        colors.append(colori[4])

unici= list(zip(*unici))

pop_a = mpatches.Patch(color='grey', label='3 $\leq$ Frequenza < 13')
pop_b = mpatches.Patch(color='gold', label='13 $\leq$ Frequenza < 26')
pop_c = mpatches.Patch(color='orange', label='26 $\leq$ Frequenza < 39')
pop_d = mpatches.Patch(color='red', label='39 $\leq$ Frequenza $\leq$ 56')

legend(handles=[pop_a,pop_b,pop_c,pop_d], loc='upper center')
ylim(0,36)
scatter(unici[0], unici[1], c=colors, marker='s') #, marker='s'
show()
