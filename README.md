# AlgoritmoGenetico
 Algoritmo Genético para el Problema del Viajero (TSP)
Este proyecto implementa un Algoritmo Genético (AG) para resolver el Problema del Viajero (TSP), un clásico de la optimización combinatoria. El objetivo es encontrar la ruta más corta que visita todas las ciudades una vez y regresa al punto de inicio.

El código está escrito en Python, pensado para ser ejecutado en PyCharm, e incluye herramientas de visualización avanzadas para analizar el comportamiento del algoritmo.
Características principales
Algoritmo Genético completo
Representación basada en permutaciones de ciudades

Selección por torneo

Cruza OX (Order Crossover)

Mutación por intercambio (swap mutation)

Registro de la distancia mínima por generación

Configuración flexible de:

Tamaño de población

Tasa de cruza

Tasa de mutación

Número de generaciones
1. Gráfica de convergencia
Muestra cómo disminuye la distancia mínima a lo largo de las generaciones.

2. Visualización 2D de la ruta final
Puntos para cada ciudad

Flechas indicando el orden de visita

Distancia total mostrada en el título

3. Animación del recorrido
Una animación paso a paso mostrando cómo se recorre la ruta final.

4. Comparación visual entre varias rutas
Permite comparar rutas obtenidas con diferentes parámetros del AG.

5. Visualización 3D
Representa la ruta en un espacio tridimensional donde el eje Z indica el orden de visita.
¿Cómo funciona el algoritmo?
Inicialización  
Se genera una población inicial de rutas aleatorias.

Evaluación  
Cada ruta se evalúa según su distancia total.

Selección  
Se eligen padres mediante torneo, favoreciendo rutas más cortas.

Cruza OX  
Combina dos rutas preservando el orden relativo de las ciudades.

Mutación  
Intercambia dos ciudades para mantener diversidad genética.

Reemplazo  
La nueva generación sustituye a la anterior.

Convergencia  
El proceso continúa hasta alcanzar el número de generaciones definido.


El programa generará:

La mejor ruta encontrada

La distancia total

La gráfica de convergencia

La visualización 2D

La animación del recorrido

La comparación entre rutas

La visualización 3D

Requisitos
Python 3.8+

matplotlib

numpy (opcional)

PyCharm (recomendado)
