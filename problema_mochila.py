import time
import random
import tracemalloc
import matplotlib.pyplot as plt

# datos del problema
pesos = [2, 3, 4, 5]
valores = [3, 4, 5, 6]
capacidad = 5

# solucion con Greedy Algorithm
def greedy(pesos, valores, capacidad):
    tracemalloc.start()
    tiempo_inicio = time.perf_counter()
    
    items = sorted(zip(valores, pesos), key=lambda x: x[0] / x[1], reverse=True)
    total_valor = 0
    total_pesos = 0
    for valor, peso in items:
        if total_pesos + peso <= capacidad:
            total_valor += valor
            total_pesos += peso
    
    tiempo_final = time.perf_counter()
    memoria_actual, memoria_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return total_valor, round((tiempo_final - tiempo_inicio) * 1000, 2), round(memoria_pico / 1024, 2)

# solucion con Tabu Search
def tabu(pesos, valores, capacidad, iteraciones=100, tabu_size=5):
    tracemalloc.start()
    tiempo_inicio = time.perf_counter()
    
    n = len(pesos)
    solucion_actual = [random.randint(0, 1) for _ in range(n)]
    mejor_solucion = solucion_actual[:]
    lista_tabu = []
    
    def fitness(solucion):
        peso = sum(p if s else 0 for p, s in zip(pesos, solucion))
        valor = sum(v if s else 0 for v, s in zip(valores, solucion))
        return valor if peso <= capacidad else 0

    for _ in range(iteraciones):
        vecinos = []
        for i in range(n):
            vecino = solucion_actual[:]
            vecino[i] = 1 - vecino[i]
            if vecino not in lista_tabu:
                vecinos.append((vecino, fitness(vecino)))
        if not vecinos: 
            break
        vecinos.sort(key=lambda x: x[1], reverse=True)
        solucion_actual = vecinos[0][0]
        lista_tabu.append(solucion_actual)
        if len(lista_tabu) > tabu_size:
            lista_tabu.pop(0)
        if fitness(solucion_actual) > fitness(mejor_solucion):
            mejor_solucion = solucion_actual[:]
    
    tiempo_final = time.perf_counter()
    memoria_actual, memoria_pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    return fitness(mejor_solucion), round((tiempo_final - tiempo_inicio) * 1000, 2), round(memoria_pico / 1024, 2)  # ms y KB

# ejecucciones de los algoritmos
resultado_greedy, tiempo_greedy, memoria_greedy = greedy(pesos, valores, capacidad)
resultado_tabu, tiempo_tabu, memoria_tabu = tabu(pesos, valores, capacidad)

# resultados
print("-----------------------------------")
print("Problema de la Mochila - Caso Neutral")
print("-----------------------------------")
print("Greedy Algorithm:")
print(f" - Valor optimo: {resultado_greedy}")
print(f" - Tiempo: {tiempo_greedy:.2f} ms")
print(f" - Memoria Pico: {memoria_greedy:.2f} KB")

print("\nTabu Search:")
print(f" - Valor optimo: {resultado_tabu}")
print(f" - Tiempo: {tiempo_tabu:.2f} ms")
print(f" - Memoria Pico: {memoria_tabu:.2f} KB")

# graficamos
labels = ['Greedy Algorithm', 'Tabu Search']
valores_tiempo = [tiempo_greedy, tiempo_tabu]
valores_memoria = [memoria_greedy, memoria_tabu]

x = range(len(labels))
width = 0.35
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

# grafico de barras para el tiempo
grafico_tiempo = ax1.bar(x, valores_tiempo, width, color='blue', label='Tiempo (ms)')
ax1.set_title('Comparacion de Tiempo')
ax1.set_ylabel('Tiempo (ms)')
ax1.set_xticks(x)
ax1.set_xticklabels(labels)
ax1.legend()

for rect in grafico_tiempo:
    height = rect.get_height()
    ax1.annotate(f'{height:.2f}', xy=(rect.get_x() + rect.get_width() / 2, height),
                 xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')

# grafico de barras para la memoria
grafico_memoria = ax2.bar(x, valores_memoria, width, color='orange', label='Memoria (KB)')
ax2.set_title('Comparacion de Memoria')
ax2.set_ylabel('Memoria (KB)')
ax2.set_xticks(x)
ax2.set_xticklabels(labels)
ax2.legend()

for rect in grafico_memoria:
    height = rect.get_height()
    ax2.annotate(f'{height:.2f}', xy=(rect.get_x() + rect.get_width() / 2, height),
                 xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')

fig.suptitle('Comparacion de Algoritmos: Tiempo y Memoria', fontsize=14)
plt.tight_layout()
plt.show()



# codigo para el caso del problema favorable para tabu search


'''
Enunciado:
Dado un conjunto de objetos, encuentra el subconjunto que maximice el valor total. 
Los pesos y valores tienen una distribución menos regular.

Datos del problema:
Pesos: [3, 4, 5, 9, 12, 1]
Valores: [8, 9, 10, 20, 30, 1]
Capacidad Máxima: 15

En este caso, Tabu Search tiene ventaja porque puede explorar combinaciones más complejas 
y evitar soluciones iniciales subóptimas.
'''








# codigo para el caso del problema favorable para greedy algorithm

'''
Enunciado:
Dado un conjunto de objetos con una clara relación proporcional entre valor y peso, 
encuentra el subconjunto que maximice el valor total.

Datos del problema:
Pesos: [2, 4, 6, 8, 10]
Valores: [4, 8, 12, 16, 20]
Capacidad Máxima: 15

En este caso, Greedy Algorithm es ideal porque las decisiones locales conducen a una 
solución óptima global.
'''



