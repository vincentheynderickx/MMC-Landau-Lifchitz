import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Ellipse

# Paramètres de l'animation
omega = 2*np.pi/10
fps = 60           # Frames par seconde
a = 1
b = 0.2
omega_ellipse = omega*(2*a*b)/(a**2+b**2)  # Vitesse angulaire en radians par seconde

# Création de la figure et des axes
fig, ax = plt.subplots()
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)

# Création de l'ellipse
ellipse = Ellipse((0,0), 2*a, 2*b, fill=False, edgecolor='b')
ax.add_patch(ellipse)

# Initialisation du point
point, = ax.plot([], [], 'ro')

# Fonction d'initialisation de l'animation
def init():
    ellipse.set_angle(0)
    point.set_data([], [])
    return ellipse, point,


# Fonction d'animation
def animate(frame):
    t = frame / fps
    x = 0.8*a*np.cos(-omega_ellipse * t)  # Calcul de la position en x
    y = 0.8*b*np.sin(-omega_ellipse * t)  # Calcul de la position en y
    x_rotated = np.cos(omega*t)*x - np.sin(omega*t)*y  # Calcul de la position en x après rotation
    y_rotated = np.sin(omega*t)*x + np.cos(omega*t)*y  # Calcul de la position en y après rotation
    point.set_data(x_rotated, y_rotated)
    ellipse.set_angle(omega * t * 180 / np.pi)
    return ellipse, point,



# Configuration de l'animation
ani = FuncAnimation(fig, animate, frames=np.arange(0, 1000, 1), 
                    init_func=init, blit=True, interval=1000/fps)


# Affichage de l'animation
ax.set_aspect('equal')
ax.grid(True)
plt.show()
