import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Ellipse

# Paramètres de l'animation
omega = 2*np.pi/10
fps = 60           # Frames par seconde
a = 1
b = 0.4
omega_ellipse = omega*(2*a*b)/(a**2+b**2)  # Vitesse angulaire en radians par seconde

# Création de la figure et des axes
fig, ax = plt.subplots()
ax.set_xlim(-1.2, 1.2)
ax.set_ylim(-1.2, 1.2)

# Création de l'ellipse
ellipse = Ellipse((0,0), 2*a, 2*b, fill=False, edgecolor='b')
ax.add_patch(ellipse)

# Initialisation du point
points, = ax.plot([], [], '+', markersize=2, animated=True)

# Fonction d'initialisation de l'animation
def init():
    ellipse.set_angle(0)
    points.set_data([], [])
    return ellipse, points,

# Paramètres des points
# Paramètres des points
N = 70
theta = np.linspace(0, 2*np.pi, N)
x1_0 = np.cos(theta)
x2_0 = np.sin(theta)
X1_0, X2_0 = np.meshgrid(x1_0, x2_0)
def equation(x, y):
    return (x**2) + (y**2) - 1
X1_inside = X1_0[equation(X1_0, X2_0) < 0]
X2_inside = X2_0[equation(X1_0, X2_0) < 0]

# Fonction d'animation
def animate(frame):
    t = frame / fps
    X1 = (a)*X1_inside * np.cos(-omega_ellipse*t)  - (a)*X2_inside * np.sin(-omega_ellipse*t)  # Calcul de la position en x
    X2 = (b)*X2_inside * np.cos(-omega_ellipse*t) + (b)*X1_inside * np.sin(-omega_ellipse*t)  # Calcul de la position en y
    X1_rotated = np.cos(omega*t)*X1 - np.sin(omega*t)*X2  # Calcul de la position en x après rotation
    X2_rotated = np.sin(omega*t)*X1 + np.cos(omega*t)*X2  # Calcul de la position en y après rotation
    X1_grid, X2_grid = np.meshgrid(X1_rotated, X2_rotated)
    points.set_data(X1_rotated, X2_rotated)
    ellipse.set_angle(omega * t * 180 / np.pi)
    return ellipse, points,



# Configuration de l'animation
ani = FuncAnimation(fig, animate, frames=np.arange(0, 1000, 1), 
                    init_func=init, blit=True, interval=1000/fps)


# Affichage de l'animation
ax.set_aspect('equal')
ax.grid(True)
plt.show()
