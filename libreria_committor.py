import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm  
import random
from pathlib import Path

import libreria_cammini as cammini


def raccogli_samples(n_iterazioni=500, n_max_step=200000, Pe=5, larghezza=(3,15),
                     output_r=None, 
                     output_t=None):
    '''
    Simula n(=500) cammini e raccoglie tutte le posizioni in due array distinti che salva su disco.
        Input:
    n (int) = 500 n. cammini considerato;
    n_max_step (int) = 200.000 n. passi dopo cui è troncato un percorso;
    Pe (float): numero di Peclet per il percorso da generare
    output_r (str) = nome file di output dei punti visitati da percorsi finiti in R
    output_t (str) = nome file di output dei punti visitati da percorsi finiti in T

    Output: None
    '''

    Pe = float(Pe)
    if output_r == None:
        output_r = Path.cwd() / f'Dati_simulazioni/output_r_{Pe}.txt'
    if output_t == None:
        output_t = Path.cwd() / f'Dati_simulazioni/output_t_{Pe}.txt'
    array_r = np.array([[-1,0]])
    array_t = np.array([[1,0]])

    
    succesful_runs = 0
    try:
        while succesful_runs < n_iterazioni:
            r0 = [(random.random() - 0.5)*2*larghezza[0], ((random.random()-0.5)*2*larghezza[1])]
            cammino = cammini.genera_cammino(n=n_max_step, Pe=Pe, 
                                            r0=r0
                                            )
            last_step = cammino[-1]
            print(last_step)

            if cammini.check_r(last_step):
                succesful_runs += 1
                array_r = np.vstack((array_r, cammino))
            elif cammini.check_t(last_step):
                succesful_runs += 1
                array_t = np.vstack((array_t, cammino))

            if succesful_runs % 1 == 0:
                print('Raggiunto step n', succesful_runs)

    except KeyboardInterrupt:
        print('Interruzione forzata in corso: attendere il salvataggio')
        np.savetxt(output_r, array_r)
        np.savetxt(output_t, array_t)
        print('Interruzione forzata completata')
            

    np.savetxt(output_r, array_r)
    np.savetxt(output_t, array_t)

    return None



def raggruppa_dati(array_dati):
    '''
    Prende l'array di run e conta la distribuzione in una griglia
    in x [-3,3] e in y [-15,15]. Restituisce l'array compilato

    Returns:
    np.histogram2d
    '''
    bins_x = 100
    bins_y = 500

    grid_range = [[-3, 3], [-15, 15]]

    x_coords, y_coords = array_dati[:,0], array_dati[:,1]
    counts, x_edges, y_edges = np.histogram2d(
    x_coords, 
    y_coords, 
    bins=[bins_x, bins_y], 
    range=grid_range
    )

    return counts, x_edges, y_edges


def salva_conteggio(array_r, array_t):
    '''
    !!!!! FUNZIONE DEPRECATA !!!!!!
    Prende array di punti visitati, calcola la committor function
    e la sampling density
    
    Returns
    committor discrete function
    sampling density array
    '''
    hist_r = raggruppa_dati(array_r)
    print('waw')
    hist_t = raggruppa_dati(array_t)
    print('waw')

    total_counts = hist_r[0] + hist_t[0]
    ratio_1 = np.divide(
    hist_t[0], 
    total_counts, 
    out=np.zeros_like(hist_t[0], dtype=float), 
    where=total_counts != 0
    )

    #np.savetxt(Path.cwd() / f'Dati_simulazioni/committor_discrete_{Pe}.txt', ratio_1)
    #np.savetxt(Path.cwd() / f'Dati_simulazioni/committor_totalcount_{Pe}.txt', total_counts)

    return ratio_1, total_counts

def esporta_grafici(Pe):
    '''
    Esporta i grafici e i dati discreti delle simulazioni 
    (come salvati dalle funzioni precedenti) a fissato Pe.

    Input: Pe(float) numero di Peclet della simulazione considerata
    Returns: None
    '''
    if Pe == None:
        Pe = 'null'
    array_r = np.loadtxt(Path.cwd() / f'Dati_simulazioni/output_r_{Pe}.txt', delimiter=' ')
    print('waw')
    array_t = np.loadtxt(Path.cwd() / f'Dati_simulazioni/output_t_{Pe}.txt', delimiter=' ')
    print('waw')

    #script_dir = Path(__file__).resolve().parent


    grid_range = [[-3, 3], [-15, 15]]

    ratio_1, total_counts = salva_conteggio(array_r, array_t)
    ratio_masked = np.ma.masked_where(total_counts.T <= 5, ratio_1.T)








    # ================================================
    # FIGURA DELLA FUNZIONE COMMITTOR
    # ================================================

    plt.figure(figsize=(8, 6))

    im = plt.imshow(
        ratio_masked, 
        origin='lower', 
        extent=[-3, 3, -15, 15], 
        aspect='auto', 
        cmap='viridis'
    )

    plt.colorbar(im, label='Probabilità di finire prima in T')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Funzione Committor')
    plt.scatter([],[], label=f'Pe={Pe}', marker=None)
    plt.legend()
    plt.savefig(Path.cwd() / f'Grafici/distribution_masked_{Pe}.png',dpi=600, bbox_inches='tight')
    #plt.show()

    np.savetxt(Path.cwd() / f'Dati_simulazioni/committor_discrete_{Pe}', ratio_1)







    # ====================================================================+
    # FIGURA DEL CONTEGGIO DATI
    # =====================================================================

    counts_masked = np.ma.masked_where(total_counts.T <= 5, total_counts.T)
    plt.figure(figsize=(8, 6))

    im = plt.imshow(
        counts_masked, 
        origin='lower', 
        extent=[-3, 3, -15, 15], 
        aspect='auto', 
        cmap='magma',     
        norm=LogNorm()   
    )

    plt.colorbar(im, label='Numero di dati raccolti')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Conteggi totali')
    plt.scatter([],[], label=f'Pe={Pe}', marker=None)
    plt.legend()
    plt.savefig(Path.cwd() / f'Grafici/total_counts_{Pe}.png',dpi=600, bbox_inches='tight')
    plt.show()


    np.savetxt(Path.cwd() / f'Dati_simulazioni/counts_{Pe}', counts_masked)









    # ===========================================================================
    # COLLASSANDO IN UN QUARTO PER IL TOT DATI RACCOLTI
    # NON IMPLEMENTATO
    # =======================================================================

    bottom_left  = total_counts[0:50,   0:250]
    bottom_right = total_counts[50:100, 0:250]
    top_left     = total_counts[0:50,   250:500]
    top_right    = total_counts[50:100, 250:500]
            
    folded_top_left     = np.flip(top_left, axis=0)       
    folded_bottom_right = np.flip(bottom_right, axis=1)  
    folded_bottom_left  = np.flip(bottom_left, axis=(0, 1))

    folded_total = top_right + folded_top_left + folded_bottom_right + folded_bottom_left
    halfsimm_total = np.hstack((np.flip(folded_total, axis=1), folded_total))
    simm_total = np.vstack((np.flip(halfsimm_total, axis=0), halfsimm_total))

    simm_masked = np.ma.masked_where(simm_total.T <= 5, simm_total.T)
    plt.figure(figsize=(6, 6))

    im = plt.imshow(
        simm_masked,
        origin='lower',
        extent=[-3, 3, -15, 15], 
        aspect='auto',
        cmap='magma',
        norm = LogNorm()
    )

    plt.colorbar(im, label='Folded Total Counts')

    #plt.savefig(Path.cwd() / f'Committor Pe={Pe}/folded_density_{Pe}.png', dpi=600, bbox_inches='tight')
    #plt.show()
    

if __name__ == '__main__':
    #random.seed(156)
    #raccogli_samples()
    Pe = input('Pe = ')
    if Pe == None:
        for Pe in [0, 0.1, 0.25, 0.5, 1, 2, 5]:
            Pe = float(Pe)
            esporta_grafici(Pe)

    else:
        Pe = float(Pe)
        esporta_grafici(Pe)