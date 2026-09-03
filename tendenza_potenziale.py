# IL PRESENTE FOGLIO DI CODICE
# calcola i potenziali parametri critici per la caratterizzazione
# dei percorsi al variare dell'attività (cioè di Pe)
# e li stampa su stdout

# Verifica infine il rapporto critico



import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm  
import random
from pathlib import Path

import libreria_cammini as cammini
import libreria_committor as committor

def norma_2d(v):
    return np.sqrt(v[0]**2 + v[1]**2)


def rapporto_critico(Pe, moda_gradU):
    '''
    Calcola il rapporto critico come ipotizzato
    Input: Pe
    Output: rapporto
    '''

    mu, D, D_theta, dt = 0.1, 0.1, 1, 0.0005

    denom = Pe * np.sqrt(4*D*D_theta / 3) #+ np.sqrt(np.pi * D / dt)
    rapporto = moda_gradU * mu / denom
    return rapporto


Pe = float(input('Pe = '))
total_counts_file = Path.cwd() / f'Dati_simulazioni/counts_{Pe}'


bins_x = 100
bins_y = 500
grid_range = [[-3, 3], [-15, 15]]

x_edges = np.linspace(grid_range[0][0], grid_range[0][1], bins_x + 1)
y_edges = np.linspace(grid_range[1][0], grid_range[1][1], bins_y + 1)

counts = np.loadtxt(total_counts_file).T

# CALCOLO DEL GRADU
x_centers = (x_edges[:-1] + x_edges[1:]) / 2
y_centers = (y_edges[:-1] + y_edges[1:]) / 2
R = np.meshgrid(x_centers, y_centers, indexing="ij")
gradU_values = norma_2d(cammini.gradU(R))
weighted_avg = np.average(gradU_values, weights=counts)

print("GradU medio:", weighted_avg)

variance = np.average((gradU_values - weighted_avg) ** 2, weights=counts**2)
std_dev = np.sqrt(variance)

print('STD:', std_dev)

x_limit = np.sqrt(1 + 1 / np.sqrt(3))
y_mid_idx = len(y_centers) // 2
x_mask = np.abs(x_centers) < x_limit+0.03
selected_counts = counts[x_mask, y_mid_idx]
total_sum = selected_counts.sum()

print('Passaggi nel rettangolo centrale:', total_sum)

fraction_passaggi = total_sum / counts.sum()
print('Passaggi / tot conteggi:', fraction_passaggi)

# GRAD U DELLA MODA

flat_index = np.argmax(counts)
row, col = np.unravel_index(flat_index, counts.shape)
modev = norma_2d(cammini.gradU([x_centers[row], y_centers[col]]))
print('gradU alla moda:', modev)

# CALCOLO DEL POTENZIALE
gradU_values = cammini.U(R)
weighted_avg = np.average(gradU_values, weights=counts)

print("U medio:", weighted_avg)

variance = np.average((gradU_values - weighted_avg) ** 2, weights=counts**2)
std_dev = np.sqrt(variance)

print('STD:', std_dev)


modeu = (cammini.U([x_centers[row], y_centers[col]]))
print('U alla moda:', modeu)

print()
rapp = rapporto_critico(Pe, modev)
print('Rapporto critico:', rapp)

