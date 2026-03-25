import random
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D  # necesario para 3D

# =========================
#   UTILIDADES TSP
# =========================

def distancia(ciudad1, ciudad2):
    return math.sqrt((ciudad1[0] - ciudad2[0])**2 + (ciudad1[1] - ciudad2[1])**2)

def distancia_ruta(ruta, ciudades):
    total = 0
    for i in range(len(ruta)):
        c_actual = ciudades[ruta[i]]
        c_sig = ciudades[ruta[(i + 1) % len(ruta)]]
        total += distancia(c_actual, c_sig)
    return total

def fitness(ruta, ciudades):
    return 1.0 / distancia_ruta(ruta, ciudades)

def crear_individuo(n_ciudades):
    ruta = list(range(n_ciudades))
    random.shuffle(ruta)
    return ruta

def crear_poblacion(tam_pob, n_ciudades):
    return [crear_individuo(n_ciudades) for _ in range(tam_pob)]

def seleccion_torneo(poblacion, ciudades, k=3):
    candidatos = random.sample(poblacion, k)
    return max(candidatos, key=lambda r: fitness(r, ciudades))

def cruza_ox(p1, p2, tasa_cruza):
    if random.random() > tasa_cruza:
        return p1[:]

    n = len(p1)
    inicio = random.randint(0, n - 2)
    fin = random.randint(inicio + 1, n - 1)

    hijo = [None] * n
    hijo[inicio:fin] = p1[inicio:fin]

    pos = fin
    for ciudad in p2:
        if ciudad not in hijo:
            if pos >= n:
                pos = 0
            hijo[pos] = ciudad
            pos += 1

    return hijo

def mutacion_swap(ruta, tasa_mut):
    for i in range(len(ruta)):
        if random.random() < tasa_mut:
            j = random.randint(0, len(ruta) - 1)
            ruta[i], ruta[j] = ruta[j], ruta[i]
    return ruta

# =========================
#   ALGORITMO GENÉTICO
# =========================

def genetico(ciudades,
             tam_pob=80,
             generaciones=120,
             tasa_cruza=0.9,
             tasa_mut=0.03):
    poblacion = crear_poblacion(tam_pob, len(ciudades))
    historial = []

    for gen in range(generaciones):
        nueva_pob = []
        for _ in range(tam_pob):
            p1 = seleccion_torneo(poblacion, ciudades)
            p2 = seleccion_torneo(poblacion, ciudades)
            hijo = cruza_ox(p1, p2, tasa_cruza)
            hijo = mutacion_swap(hijo, tasa_mut)
            nueva_pob.append(hijo)

        poblacion = nueva_pob
        mejor = min(poblacion, key=lambda r: distancia_ruta(r, ciudades))
        dist = distancia_ruta(mejor, ciudades)
        historial.append(dist)
        print(f"Gen {gen}: distancia = {dist:.3f}")

    mejor_final = min(poblacion, key=lambda r: distancia_ruta(r, ciudades))
    return mejor_final, historial

# =========================
#   VISUALIZACIONES 2D
# =========================

def dibujar_ruta(ciudades, ruta):
    xs = [ciudades[i][0] for i in ruta] + [ciudades[ruta[0]][0]]
    ys = [ciudades[i][1] for i in ruta] + [ciudades[ruta[0]][1]]

    plt.figure(figsize=(8, 7))
    plt.plot(xs, ys, '-o', color='royalblue', linewidth=2, markersize=8)

    for i in range(len(ruta)):
        x_start, y_start = ciudades[ruta[i]]
        x_end, y_end = ciudades[ruta[(i + 1) % len(ruta)]]
        dx = x_end - x_start
        dy = y_end - y_start
        plt.arrow(
            x_start, y_start,
            dx * 0.85, dy * 0.85,
            head_width=0.15,
            length_includes_head=True,
            color='darkorange'
        )

    for idx, (x, y) in enumerate(ciudades):
        plt.text(x + 0.1, y + 0.1, f"{idx}", fontsize=12, color="black")

    dist = distancia_ruta(ruta, ciudades)
    plt.title(f"Ruta óptima (distancia = {dist:.3f})", fontsize=14)
    plt.xlabel("Coordenada X")
    plt.ylabel("Coordenada Y")
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

def graficar_convergencia(historial, titulo="Convergencia del Algoritmo Genético"):
    plt.figure(figsize=(7, 5))
    plt.plot(historial, color='green')
    plt.title(titulo)
    plt.xlabel("Generación")
    plt.ylabel("Distancia mínima")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# =========================
#   ANIMACIÓN
# =========================

def animar_ruta(ciudades, ruta, intervalo=800):
    xs = [ciudades[i][0] for i in ruta] + [ciudades[ruta[0]][0]]
    ys = [ciudades[i][1] for i in ruta] + [ciudades[ruta[0]][1]]

    fig, ax = plt.subplots(figsize=(8, 7))
    ax.set_title("Animación del recorrido TSP")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True)

    ax.scatter(xs, ys, color='blue')
    for idx, (x, y) in enumerate(ciudades):
        ax.text(x + 0.1, y + 0.1, str(idx), fontsize=12)

    linea, = ax.plot([], [], '-o', color='red')

    def actualizar(frame):
        linea.set_data(xs[:frame+1], ys[:frame+1])
        return linea,

    anim = FuncAnimation(fig, actualizar, frames=len(xs), interval=intervalo, repeat=False)
    plt.show()

# =========================
#   COMPARACIÓN DE RUTAS
# =========================

def comparar_rutas(ciudades, rutas, titulos=None):
    n = len(rutas)
    fig, axes = plt.subplots(1, n, figsize=(6*n, 6))

    if n == 1:
        axes = [axes]

    if titulos is None:
        titulos = [f"Ruta {i+1}" for i in range(n)]

    for ax, ruta, titulo in zip(axes, rutas, titulos):
        xs = [ciudades[i][0] for i in ruta] + [ciudades[ruta[0]][0]]
        ys = [ciudades[i][1] for i in ruta] + [ciudades[ruta[0]][1]]
        dist = distancia_ruta(ruta, ciudades)

        ax.plot(xs, ys, '-o', color='green')
        ax.set_title(f"{titulo}\nDistancia = {dist:.3f}")
        ax.grid(True)

        for idx, (x, y) in enumerate(ciudades):
            ax.text(x + 0.1, y + 0.1, str(idx), fontsize=12)

    plt.tight_layout()
    plt.show()

# =========================
#   VISUALIZACIÓN 3D
# =========================

def ruta_3d(ciudades, ruta):
    xs = [ciudades[i][0] for i in ruta] + [ciudades[ruta[0]][0]]
    ys = [ciudades[i][1] for i in ruta] + [ciudades[ruta[0]][1]]
    zs = list(range(len(xs)))

    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection='3d')

    ax.plot(xs, ys, zs, '-o', color='purple')
    ax.set_title("Ruta TSP en 3D (orden de visita)")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Orden")

    plt.tight_layout()
    plt.show()

# =========================
#   MAIN DE DEMOSTRACIÓN
# =========================

if __name__ == "__main__":
    # Puedes cambiar estas coordenadas o generar más ciudades
    ciudades = [
        (0, 0),
        (1, 5),
        (5, 2),
        (6, 6),
        (8, 3),
        (2, 1)
    ]

    # Corrida base
    mejor, historial = genetico(
        ciudades,
        tam_pob=80,
        generaciones=120,
        tasa_cruza=0.9,
        tasa_mut=0.03
    )

    print("\nMejor ruta encontrada:", mejor)
    print("Distancia total:", distancia_ruta(mejor, ciudades))

    # Convergencia
    graficar_convergencia(historial, titulo="Convergencia (Pob=80, mut=0.03)")

    # Ruta final 2D
    dibujar_ruta(ciudades, mejor)

    # Animación del recorrido
    animar_ruta(ciudades, mejor)

    # Comparación con otras configuraciones
    mejor2, _ = genetico(ciudades, tam_pob=50, generaciones=120, tasa_cruza=0.8, tasa_mut=0.05)
    mejor3, _ = genetico(ciudades, tam_pob=150, generaciones=120, tasa_cruza=0.9, tasa_mut=0.02)

    comparar_rutas(
        ciudades,
        [mejor, mejor2, mejor3],
        ["Pob=80, mut=0.03", "Pob=50, mut=0.05", "Pob=150, mut=0.02"]
    )

    # Visualización 3D de la mejor ruta
    ruta_3d(ciudades, mejor)
