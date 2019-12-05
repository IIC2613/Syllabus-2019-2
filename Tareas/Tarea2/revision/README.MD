# Revision Tarea 2

La metodología de evaluación consistió en la utilización de un set de 12 problemas de SLIDERS para evaluar tanto la admisibilidad de la heurística diseñada como la implementación de los algoritmos pedidos.

## Informe (0.5 puntos)
Si su entrega incluye el informe con lo solicitado.

## Evaluacion de la heurística (2.0 puntos)
Se utilizaron los estados iniciales contenidos en el archivo problems.py para estimar un valor heurístico. Si el valor estimado es menor o igual al costo óptimo de esa solucion suma 1 punto (de 12 en total)

## Test de AWA* y RWA* (2.0 ptos AWA*, 1.5 ptos RWA*)
Se utilizaron los problemas del archivo problems para realizar la búsqueda utilizando w=3 y w=1. Si el valor encontrado con su algoritmo está dentro de la cota (3 veces el costo óptimo para w=3; y el costo óptimo para w=1) suma 1 punto (de 24 en total). En el caso de RWA* se utilizó la misma metodología.
Para ámbos algoritmos, se utilizó un timebound de acuerdo al problema, tiempo suficientemente alto para encontrar una solución óptima.

Los costos óptimos y los timebound son los siguientes:
```python
costs = [2, 7, 2, 4, 4, 3, 5, 7, 2, 4, 8, 7]
time_bounds = [3, 60, 3, 3, 3, 3, 20, 60, 3, 3, 60, 60]
```

Para recorrección por favor solicitelo en el siguiente formulario:

https://forms.gle/kvKwBSFb4rfpkzM38
