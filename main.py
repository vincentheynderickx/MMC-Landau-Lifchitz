import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Ellipse

# Paramètres de l'animation
omega = 2*np.pi/10
fps = 60           # Frames par seconde
a = 1

# Définiion d'une fonction b(t) affine par morceaux qui passe par les palliers 1, 0.9, 0.5, 0.1 et qui évolue avec une pente 1 entre ces palliers
deltaTEvo = 0.2
deltaTPallier = 8
def b(t):
    if t < deltaTPallier:
        return 1
    elif deltaTPallier <= t < deltaTPallier + deltaTEvo:
        return 1 - (t - deltaTPallier)/deltaTEvo * 0.1
    elif deltaTPallier + deltaTEvo <= t < 2*deltaTPallier + deltaTEvo:
        return 0.9
    elif 2*deltaTPallier + deltaTEvo <= t < 2*deltaTPallier + 2*deltaTEvo:
        return 0.9 - (t - 2*deltaTPallier - deltaTEvo)/deltaTEvo * 0.4
    elif 2*deltaTPallier + 2*deltaTEvo <= t < 3*deltaTPallier + 2*deltaTEvo:
        return 0.5
    elif 3*deltaTPallier + 2*deltaTEvo <= t < 3*deltaTPallier + 3*deltaTEvo:
        return 0.5 - (t - 3*deltaTPallier - 2*deltaTEvo)/deltaTEvo * 0.4
    else:     
        return 0.1

T = 4*deltaTPallier + 3*deltaTEvo

# Création de la figure et des axes
fig, ax = plt.subplots()
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)

# Création de l'ellipse
ellipse = Ellipse((0,0), 2*a, 2*b(0), fill=False, edgecolor='black', linewidth=3, linestyle='--')
ax.add_patch(ellipse)

# Initialisation du point
points, = ax.plot([], [], '+', markersize=2, animated=True)

# Ajout du texte pour afficher la valeur de t
time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
b_text = ax.text(0.02, 0.85, '', transform=ax.transAxes)

# Fonction d'initialisation de l'animation
def init():
    ellipse.set_angle(0)
    points.set_data([], [])
    time_text.set_text('')
    b_text.set_text('')
    return ellipse, points, time_text, b_text,

# Paramètres des points
N = 70
theta = np.linspace(0, 2*np.pi, N)
x1_0 = np.cos(theta)
x2_0 = 2*np.sin(theta)
X1_0, X2_0 = np.meshgrid(x1_0, x2_0)
def equation(x, y):
    return (x**2) + (y**2) - 1
X1_inside = X1_0[equation(X1_0, X2_0) < 0]
X2_inside = X2_0[equation(X1_0, X2_0) < 0]

# Fonction d'animation
def animate(frame):
    t = frame / fps
    b_val = b(t)
    omega_ellipse = omega*(2*a*b_val)/(a**2+b_val**2)  # Recalcul de la vitesse angulaire en radians par seconde
    X1 = (a)*X1_inside * np.cos(-omega_ellipse*t)  - (a)*X2_inside * np.sin(-omega_ellipse*t)  # Calcul de la position en x
    X2 = (b_val)*X2_inside * np.cos(-omega_ellipse*t) + (b_val)*X1_inside * np.sin(-omega_ellipse*t)  # Calcul de la position en y
    X1_rotated = np.cos(omega*t)*X1 - np.sin(omega*t)*X2  # Calcul de la position en x après rotation
    X2_rotated = np.sin(omega*t)*X1 + np.cos(omega*t)*X2  # Calcul de la position en y après rotation
    X1_grid, X2_grid = np.meshgrid(X1_rotated, X2_rotated)
    points.set_data(X1_rotated, X2_rotated)
    ellipse.set_angle(omega * t * 180 / np.pi)
    ellipse.set_height(2*b(t))
    time_text.set_text('t = {:.2f}'.format(t))  # Affichage de la valeur de t
    b_text.set_text('b = {:.2f}'.format(b(t)))
    return ellipse, points, time_text, b_text,

# Configuration de l'animation
ani = FuncAnimation(fig, animate, frames=np.arange(0, T*fps, 1),
                    init_func=init, blit=True, interval=1000/fps)

# Affichage de l'animation
ax.set_aspect('equal')
ax.grid(False)
plt.show()