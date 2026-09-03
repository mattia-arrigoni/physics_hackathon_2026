# Questo file è utilizzato solo per lanciare la funzione "raccogli_samples"


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm  
import random
from pathlib import Path

import libreria_cammini as cammini
import libreria_committor as committor

#random.seed(1241)
committor.raccogli_samples(Pe=0.25, n_iterazioni=2000, larghezza=[2,10])