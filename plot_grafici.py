import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm  
import random
from pathlib import Path

import libreria_cammini as cammini
import libreria_committor as committor
from statistica_potenziale import statistica_conteggi



# Come otteniamo le barre di errore:
# suddividiamo i 4 quadranti, prendiamo la moda di ognuno
# e valutiamo la std dei 4 valori ottenuti



numeri_Pe = [0.25, 0.5, 1., 2.5, 5., 10., 20., 50.]
rapps = np.array([])
stds = np.array([])
percs = np.array([])

for Pe in numeri_Pe:
    rapp, std, perc = statistica_conteggi(Pe)
    rapps, stds, percs = np.append(rapps, [rapp]), np.append(stds, [std]), np.append(percs, [perc])

#print()
reciproci = 1/rapps
std_rec = stds / rapps**2

plt.figure(figsize=(10,6))
plt.errorbar(numeri_Pe, reciproci, yerr=std_rec, color='purple', fmt='o', label='$\\varsigma=\\frac{v}{\\mu\\cdot\\text{moda}(\\nabla U)}$')
plt.axhline(1, color='gray', linestyle='--')
#plt.xscale('log')
plt.legend(loc='center right', fontsize=30)

plt.title('Andamento di $\\varsigma$')
plt.xlabel('Pe')
plt.savefig(Path.cwd() /'Grafici/grafico_sigma.svg')
plt.savefig(Path.cwd() /'Grafici/grafico_sigma.png', dpi=1200, )
plt.show()

dati_output = np.array([numeri_Pe, reciproci, std_rec, percs])
np.savetxt(Path.cwd()/'dati_sigma.txt', dati_output)

plt.figure(figsize=(10,6))
plt.errorbar(numeri_Pe, percs, yerr=0, color='green', fmt='o', label='SC')
#plt.xscale('log')
plt.legend(loc='upper right', fontsize=10)
plt.axhline(0, color='gray', linestyle='--')

plt.xlabel('Pe')
plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
plt.savefig(Path.cwd() /'Grafici/SC.svg')
plt.savefig(Path.cwd() /'Grafici/SC.png', dpi=1200, )
plt.show()