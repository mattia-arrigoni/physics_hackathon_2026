import numpy as np
import matplotlib.pyplot as plt
#import random
#import time
#import math

from scipy import optimize 
from scipy import stats 
from scipy import integrate 


# ============================================================








def U(r,  k_x=6, x_0=1, k_y=20):
    x = r[0]
    y = r[1]
    return k_x * (x**2 - x_0**2)**2 + (k_y / 2) * y**2

def gradU(r, k_x=6, x_0=1, k_y=20):
    x = r[0]
    y = r[1]
    du_dx = 4 * k_x * x * (x**2 - x_0**2)
    du_dy = k_y * y
    return np.array([du_dx, du_dy])

def update_r(r, theta, dt, v, mu=0.1, D=0.1, k_x=6, x_0=1, k_y=20):
    '''
    Genera r(i+1) dal microstato attuale
    (col metodo brute-force).
      Input:
    r (np.array) [x,y]: posizione r(i)
    theta (float): theta(i)
    dt (float): step di integrazione
    v (float): velocità di attività della particella
    mu, D, k_x, k_y (floats): parametri del potenziale e del fenomeno browniano
    
      Returns:
    r(i+1) (np.array) [x,y]
    '''

    # Direzione di propulsione u_i
    u = np.array([np.cos(theta), np.sin(theta)])

    # Gradiente del potenziale in r_i = (x, y)
    grad_U = gradU(r, k_x=k_x, x_0=x_0, k_y=k_y)

    # Rumore casuale gaussiano 2D (media 0, deviazione standard 1)
    xi = np.random.normal(0, 1, size=2)

    # Aggiornamento posizione
    r_next = r + v * u * dt - mu * grad_U * dt + np.sqrt(2 * D * dt) * xi
    return r_next

def update_theta(theta, dt, D_theta=1):
    '''
    Genera theta(i+1) dal microstato attuale.

      Input:
    theta (float): theta(i)
    dt (float): step di integrazione
    D_theta: coefficiente di diffusione del moto in theta

      Returns:
    theta(i+1) (float)
    '''
    # Rumore casuale gaussiano scalare
    eta = np.random.normal(0, 1)

    # Aggiornamento angolo
    theta_next = theta + np.sqrt(2 * D_theta * dt) * eta

    # Mantiene l'angolo compreso tra -pi e pi (opzionale ma consigliato)
    return (theta_next + np.pi) % (2 * np.pi) - np.pi















# ===================================================================================
# MODELLO TPS
# NON IMPLEMENTATO
# =============================================================================

def update_r_backward(r_next, theta_next, dt, v, mu=0.1, D=0.1, k_x=6, x_0=1, k_y=20):
    # Per il modello backwards
    # Direzione di propulsione al tempo i+1
    u_next = np.array([np.cos(theta_next), np.sin(theta_next)])

    # Gradiente del potenziale calcolato in r_{i+1}
    grad_U = gradU(r_next[0], r_next[1], k_x=k_x, x_0=x_0, k_y=k_y)

    # Rumore casuale gaussiano 2D
    xi = np.random.normal(0, 1, size=2)

    # Aggiornamento all'indietro: nota il meno davanti al termine v * u_next
    r_prev = (
        r_next
        - v * u_next * dt
        - mu * grad_U * dt
        + np.sqrt(2 * D * dt) * xi
    )
    return r_prev

def update_theta_backward(theta_next, dt, D_theta=1): # Per il modello backwards
  # Rumore casuale gaussiano scalare
  eta = np.random.normal(0, 1)

  # Aggiornamento all'indietro dell'angolo
  theta_prev = theta_next + np.sqrt(2 * D_theta * dt) * eta

  # Normalizzazione tra -pi e pi
  return (theta_prev + np.pi) % (2 * np.pi) - np.pi

# ===============================================================











def check_t(r): # True se r è nella regione target
  ''' 
  Restituisce True se r è nella regione target (x>0, U(R)<=2)
  '''
  if r[0] <= 0:
    return False
  if U(r) <= 2: #(k_B T è 1)
    return True
  return False

def check_r(r): # True se r è nella regione reagente
  '''
  Restituisce True se r è nella regione reagente (x<0, U(R)<=2)
  '''
  if r[0] >= 0:
    return False
  if U(r) <= 2: #(k_B T è 1)
    return True
  return False

def genera_cammino(n=10000, Pe = 5, D = 0.1, D_theta = 1, seed=None, r0=np.array([-1,0])): # genera un evento (calcolato con brute-force)
  '''
  Genera un cammino partendo dal punto r0. Restituisce l'array delle posizioni visitate.

    Input:
  n (int o float): numero di posizioni
  D, D_theta (float): coefficienti di diffusione per il moto browniano e per la diffusione dell'angolo di attività
  seed (int): seed libreria random
  r0 (2x2 float np.ndarray o list): posizione di partenza

    Returns:
  (2xN float np.2darray)
  '''
  n=int(n)
  v = Pe / np.sqrt(3  / (4 * D * D_theta))
  theta = (np.random.random () - 0.5 ) * 2 * np.pi  #genera da -pi a +pi
  np.random.seed(seed)
  if type(r0) != np.ndarray:
     r0 = np.array(r0)
  r=r0 
  dt = 0.0005
  posizioni = [r0]

  for i in range(n):
    r_next = update_r(r, theta, dt, v)
    theta_next = update_theta(theta, dt)
    r=r_next
    theta=theta_next
    posizioni.append(r)
    if check_t(r) or check_r(r):
      break
  return posizioni

def grafico(xmax, ymax):
  x = np.linspace(-2.5,2.5, 500)
  y = np.linspace(-ymax*1.1, ymax*1.1, 500)
  X, Y = np.meshgrid(x, y)
  Z = U([X,Y])

  plt.figure(figsize=(8,6))
  custom_levels = np.sort(
      list(map(
          lambda x: x**2, range(2,max(4, int(ymax*10)),2)
          )) + [6] + [10]
      )
  contours = plt.contour(X, Y, Z, levels=custom_levels, cmap='viridis')
  plt.clabel(contours, inline=True, fontsize=8)
  plt.colorbar(contours, label="Function value f(x, y)")

  contour_2 = plt.contour(X, Y, Z, levels=[2], colors="red", linewidths=2.5)
  plt.clabel(contour_2, inline=True, fontsize=8, fmt="%1.0f")

  plt.text(x=-1, y=0, s='R', fontsize=12, color='black', ha='center', va='center')
  plt.text(x=1, y=0, s='T', fontsize=12, color='black', ha='center', va='center')

  plt.title("Level Lines of a 2D Function")
  plt.xlabel("X axis")
  plt.ylabel("Y axis")

# ================================================








if __name__=='__main__':
  # Generazione ed estrazione coordinate
  cammino = np.array(genera_cammino())

  while not check_t(cammino[-1]):
    cammino = np.array(genera_cammino())

  x_cammino = cammino[:, 0]
  y_cammino = cammino[:, 1]
  # grafico di fondo (linee di livello)
  grafico(2, max(2, np.max(np.abs(y_cammino))))

  # Sovrapponi la traiettoria (x contro y)
  plt.plot(x_cammino, y_cammino, color="darkorange", linewidth=2, label="Traiettoria")


  plt.legend(loc=1)
  plt.savefig('fig.png')
  plt.show()
  
