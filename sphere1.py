# sphere_rotation_visible_fast_menu.py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import cm
from matplotlib.widgets import Button

# ----- Paramètres visibles -----
r = 1200
n = 80                 # résolution
omega = 1.5        # vitesse rotation
vz = 16             # vitesse montée
frames = 20
interval_ms = 20

# ----- Grille sphérique -----
theta = np.linspace(0, np.pi, n)
phi   = np.linspace(0, 2*np.pi, 2*n)
TH, PH = np.meshgrid(theta, phi)

X0 = r * np.sin(TH) * np.cos(PH)
Y0 = r * np.sin(TH) * np.sin(PH)
Z0 = r * np.cos(TH)

# Bandes de longitude (pour “voir” la rotation)
u = (PH % (2*np.pi)) / (2*np.pi)
facecolors0 = cm.hsv(u)
facecolors0[..., 3] = 0.95

# ----- Figure + espace pour le menu -----
fig = plt.figure(figsize=(6, 6))
plt.subplots_adjust(top=0.88)  # on laisse de la place pour les boutons
ax = fig.add_subplot(111, projection="3d")
ax.set_proj_type('persp')
ax.set_title("Sphère: rotation + montée (menu export en haut)")

asc_max = vz * frames
L = r + 2 + asc_max
ax.set_xlim(-L, L); ax.set_ylim(-L, L); ax.set_zlim(-L, L)
ax.set_box_aspect((1, 1, 1))

def update(frame):
    ax.cla()
    ax.set_proj_type('persp')
    ax.set_title("Sphère: rotation + montée (menu export en haut)")
    ax.set_xlim(-L, L); ax.set_ylim(-L, L); ax.set_zlim(-L, L)
    ax.set_box_aspect((1, 1, 1))
    ax.set_xlabel("X"); ax.set_ylabel("Y"); ax.set_zlabel("Z")

    # Rotation + montée
    ang = omega * frame
    c, s = np.cos(ang), np.sin(ang)
    X = c*X0 - s*Y0
    Y = s*X0 + c*Y0
    Z = Z0 + vz * frame

    ax.plot_surface(
        X, Y, Z,
        rstride=2, cstride=2,
        facecolors=facecolors0,
        linewidth=0, edgecolor=None, antialiased=False
    )
    ax.view_init(elev=22, azim=20)
    return ax,

ani = FuncAnimation(fig, update, frames=frames, interval=interval_ms, blit=False)

# ----- Boutons du mini-menu -----
# zones des boutons (left, bottom, width, height) en unités [0..1]
ax_gif = plt.axes([0.12, 0.93, 0.30, 0.05])
ax_mp4 = plt.axes([0.58, 0.93, 0.30, 0.05])
btn_gif = Button(ax_gif, "Export GIF")
btn_mp4 = Button(ax_mp4, "Export MP4")

def export_gif(event):
    from matplotlib.animation import PillowWriter
    try:
        print("Export GIF…")
        ani.event_source.stop()
        fps = max(1, int(1000 / interval_ms))
        ani.save("sphere.gif", writer=PillowWriter(fps=fps))
        print("✅ GIF créé : sphere.gif")
    except Exception as e:
        print("❌ Erreur GIF :", e)
    finally:
        ani.event_source.start()

def export_mp4(event):
    try:
        print("Export MP4… (ffmpeg requis)")
        ani.event_source.stop()
        fps = max(1, int(1000 / interval_ms))
        ani.save("sphere.mp4", writer="ffmpeg", fps=fps)
        print("✅ MP4 créé : sphere.mp4")
    except FileNotFoundError:
        print("❌ ffmpeg introuvable. Installe-le (ex: Termux -> pkg install ffmpeg).")
    except Exception as e:
        print("❌ Erreur MP4 :", e)
    finally:
        ani.event_source.start()

btn_gif.on_clicked(export_gif)
btn_mp4.on_clicked(export_mp4)

plt.show()