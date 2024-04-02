import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, Button, RadioButtons
from matplotlib.patches import Ellipse

# Création de la figure et des axes
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)


# Paramètres de l'ellipse
centre_x = 0   # coordonnée x du centre
centre_y = 0   # coordonnée y du centre
a = 2    # largeur de l'ellipse
b = 1    # hauteur de l'ellipse
angle = 0  # angle de rotation (en degrés)
omega = 10    # vitesse de rotation (en rad/s)

k = omega*(a**2 - b**2)/(a**2 + b**2)

# Définir la zone d'intérêt en créant une grille de points
x1_min, x1_max = -1, 1
x2_min, x2_max = -1, 1
step = 0.1  # Pas de la grille
x1 = np.arange(x1_min, x1_max, step)
x2 = np.arange(x2_min, x2_max, step)
X1, X2 = np.meshgrid(x1, x2)

# Définition d'une particule dans la zone d'intérêt et tracé de son point de départ
po1 = 0.6
po2 = 0.2
p = np.array([po1, po2])
part = plt.plot(p[0], p[1], 'ro')


mask = np.ones_like(X1, dtype=bool)

V1 = np.zeros_like(X1)
V2 = np.zeros_like(X2)
V1[mask] = k*X2[mask]  
V2[mask] = k*X1[mask]

l = plt.quiver(X1[mask], X2[mask], V1[mask], V2[mask])



ellipse = Ellipse((centre_x, centre_y), width=a, height=b, angle=angle*np.pi/180, edgecolor='b', facecolor='none')
ax.add_patch(ellipse)

axtime = plt.axes([0.25, 0.025, 0.65, 0.03])
stime = Slider(axtime, 'Time', 0, 10.0, valinit=0)
# Configuration des axes
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.set_aspect('equal')
ax.grid(True)

# Fonction de mise à jour de l'ellipse
def update(val):
    angle = omega*stime.val
    ellipse.set_angle(angle*180/np.pi)
    #rotate the grid as wel
    X1_rot = X1*np.cos(angle) - X2*np.sin(angle)
    X2_rot = X1*np.sin(angle) + X2*np.cos(angle)
    l.set_offsets(np.c_[X1_rot[mask], X2_rot[mask]])
    V1 = np.zeros_like(X1)
    V2 = np.zeros_like(X2)
    V1[mask] = k*X2_rot[mask]
    V2[mask] = k*X1_rot[mask]
    l.set_UVC(V1[mask], V2[mask])

    #evolution de la position de la particule et modification de sa position sachant que sa vitesse est V = k*position
    d0 = po1-po2
    p[0]=0.5(d0 + np.exp(2*k*stime.val)*d0)
    p[1]=0.5(d0 - np.exp(2*k*stime.val)*d0)
    part[0].set_xdata(p[0])
    part[0].set_ydata(p[1])

    



stime.on_changed(update)



# Affichage de la figure
plt.show()
