import matplotlib.pyplot as plt
import random
import math

def distancia(ciudad1, ciudad2):
    return math.sqrt((ciudad1[0]-ciudad2[0])**2 + (ciudad1[1]-ciudad2[1])**2)

def distancia_total(ruta, ciudades):
    distancia_total = 0
    for i in range(len(ruta)-1):
        distancia_total += distancia(ciudades[ruta[i]], ciudades[ruta[i+1]])
    distancia_total += distancia(ciudades[ruta[-1]], ciudades[ruta[0]])
    return distancia_total

def generar_solucion(ciudades, k):
    vendedores = list(range(k))
    ruta = [random.choice(vendedores) for _ in range(len(ciudades))]
    while any(ruta.count(vendedor) < 2 for vendedor in vendedores):
        ruta = [random.choice(vendedores) for _ in range(len(ciudades))]
    return ruta

def generar_vecino(solucion):
    i = random.randint(0, len(solucion)-1)
    j = random.randint(0, len(solucion)-1)
    while solucion[i] == solucion[j]:
        j = random.randint(0, len(solucion)-1)
    vecino = solucion[:]
    vecino[i], vecino[j] = vecino[j], vecino[i]
    return vecino

def recocido_simulado(ciudades, temperatura_inicial, temperatura_final, factor_enfriamiento, k):
    mejor_solucion_global = None
    mejor_distancia_global = float('inf')
    temperatura = temperatura_inicial
    soluciones = [[] for _ in range(k)]
    for i in range(k):
        soluciones[i] = generar_solucion(ciudades,k)
    mejor_distancias = []
    while temperatura > temperatura_final:
        for i in range(k):
            solucion_actual = soluciones[i]
            vecino = generar_vecino(solucion_actual)
            distancia_actual = distancia_total(solucion_actual, ciudades)
            distancia_vecino = distancia_total(vecino, ciudades)
            if distancia_vecino < distancia_actual:
                soluciones[i] = vecino
                if distancia_vecino < mejor_distancia_global:
                    mejor_solucion_global = vecino
                    mejor_distancia_global = distancia_vecino
            else:
                probabilidad = math.exp(-(distancia_vecino - distancia_actual) / temperatura)
                if random.random() < probabilidad:
                    soluciones[i] = vecino
        mejor_distancias.append(mejor_distancia_global)
        temperatura *= factor_enfriamiento
    return mejor_solucion_global, mejor_distancia_global, mejor_distancias

ciudades = [(0,0), (1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7), (8,8), (9,9)]
temperatura_inicial = 100
temperatura_final = 1
factor_enfriamiento = 0.99
k = 2
solucion, distancia, mejor_distancias = recocido_simulado(ciudades, temperatura_inicial, temperatura_final, factor_enfriamiento, k)
print("Mejor solución encontrada:", solucion)
print("Distancia total de la mejor solución:", distancia)
plt.plot(mejor_distancias)
plt.xlabel('Iteración')
plt.ylabel('Distancia')
plt.show()
