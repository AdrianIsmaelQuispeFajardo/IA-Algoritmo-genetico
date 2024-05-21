import random
from itertools import combinations

def funcion_objetivo(x):
    return x**3 - 60*x**2 + 900*x + 100

def decimal_a_binario(x):
    binario_x = bin(x)[2:].zfill(5)  # Representación binaria de 5 bits
    return binario_x

def generar_poblacion(tamaño):
    poblacion = []
    for i in range(tamaño):
        x = random.randint(0, 31)
        binario_x = decimal_a_binario(x)
        puntaje_fitness = funcion_objetivo(x)
        poblacion.append((i+1, x, binario_x, puntaje_fitness))  # Agregando el valor de f(x) al individuo
    return poblacion

def fitness(poblacion):
    puntajes_fitness = []
    for individuo in poblacion:
        x = individuo[1]
        puntaje_fitness = funcion_objetivo(x)
        puntajes_fitness.append(puntaje_fitness)
    return puntajes_fitness

def seleccion_torneo(poblacion, puntajes_fitness):
    poblacion_seleccionada = []
    individuos_restantes = poblacion.copy()

    # Realizar tres enfrentamientos
    for _ in range(len(poblacion) // 2):
        # Escoger dos individuos aleatorios que no se hayan enfrentado aún
        individuo1 = random.choice(individuos_restantes)
        individuos_restantes.remove(individuo1)
        individuo2 = random.choice([ind for ind in individuos_restantes if ind[0] != individuo1[0]])
        individuos_restantes.remove(individuo2)

        # Obtener los puntajes de fitness de los dos individuos en el enfrentamiento
        apt1, apt2 = individuo1[3], individuo2[3]

        # Mostrar los enfrentamientos y los puntajes de fitness comparados
        print(f"Enfrentamiento: Individuo {individuo1[0]} vs Individuo {individuo2[0]}")
        print(f"Puntajes de fitness comparados: Individuo {individuo1[0]} - {apt1}, Individuo {individuo2[0]} - {apt2}")

        # Seleccionar el individuo con el mejor puntaje de fitness y mostrar quién gana
        if apt1 > apt2:
            poblacion_seleccionada.append(individuo1)
            print(f"Individuo {individuo1[0]} gana")
        else:
            poblacion_seleccionada.append(individuo2)
            print(f"Individuo {individuo2[0]} gana")

    return poblacion_seleccionada

def asignar_puntos_cruce(poblacion_seleccionada):
    puntos_cruce = []
    pares_restantes = list(combinations(poblacion_seleccionada, 2))  # Generar todas las combinaciones posibles de pares

    random.shuffle(pares_restantes)  # Mezclar aleatoriamente los pares

    for par in pares_restantes[:3]:  # Tomar tres pares únicos
        individuo1, individuo2 = par
        punto_cruce = random.randint(1, 5)
        puntos_cruce.append((individuo1[0], individuo2[0], punto_cruce))

    return puntos_cruce

def duplicar_individuos(poblacion):
    poblacion_duplicada = poblacion.copy()
    for individuo in poblacion:
        poblacion_duplicada.append(individuo)
    return poblacion_duplicada

def cruce(poblacion_seleccionada, puntos_cruce):
    nueva_poblacion = []

    for par, punto in puntos_cruce:
        indice1, indice2 = par
        punto -= 1  # Ajustamos el punto de cruce para usarlo como índice

        # Extraemos los números binarios de los individuos
        binario1 = list(poblacion_seleccionada[indice1 - 1][2])
        binario2 = list(poblacion_seleccionada[indice2 - 1][2])

        # Realizamos el cruce en el punto especificado
        for i in range(punto, len(binario1)):
            binario1[i], binario2[i] = binario2[i], binario1[i]

        # Convertimos los números binarios de vuelta a enteros y los agregamos a la nueva población
        nueva_poblacion.append((indice1, int(''.join(binario1), 2)))
        nueva_poblacion.append((indice2, int(''.join(binario2), 2)))

    return nueva_poblacion

def mutacion(poblacion, tasa_mutacion):
    total_genes = len(poblacion[0][2]) * len(poblacion)  # Total de genes en la población
    num_mutaciones = int(tasa_mutacion * total_genes)  # Número de mutaciones

    for _ in range(num_mutaciones):
        # Seleccionar aleatoriamente un individuo para la mutación
        indice_individual = random.randint(0, len(poblacion) - 1)
        individuo = poblacion[indice_individual]

        # Seleccionar aleatoriamente un gen para mutar
        indice_gen = random.randint(0, len(individuo[2]) - 1)

        # Realizar la mutación: cambiar el bit en la posición indice_gen
        representacion_binaria = list(individuo[2])
        representacion_binaria[indice_gen] = '1' if representacion_binaria[indice_gen] == '0' else '0'
        binario_mutado = ''.join(representacion_binaria)

        # Actualizar el individuo mutado en la población
        poblacion[indice_individual] = (individuo[0], individuo[1], binario_mutado, funcion_objetivo(individuo[1]))

    return poblacion

# Ejemplo de ejecución
tamaño_poblacion = 6
poblacion = generar_poblacion(tamaño_poblacion)
print("Población inicial:")
for individuo in poblacion:
    print(f"Individuo {individuo[0]}: x={individuo[1]}, representación binaria={individuo[2]}, f(x)={individuo[3]}")
puntajes_fitness = fitness(poblacion)
print("Puntajes de fitness:")
print(puntajes_fitness)
poblacion_seleccionada = seleccion_torneo(poblacion, puntajes_fitness)
print("Población seleccionada:")
for individuo in poblacion_seleccionada:
    print(f"Individuo {individuo[0]}: x={individuo[1]},representación binaria={individuo[2]}, f(x)={individuo[3]}")
poblacion_duplicada = duplicar_individuos(poblacion_seleccionada)
print("Población duplicada:")
for individuo in poblacion_duplicada:
    print(f"Individuo {individuo[0]}: x={individuo[1]}, representación binaria={individuo[2]}, f(x)={individuo[3]}")

puntos_cruce = asignar_puntos_cruce(poblacion_seleccionada)
print("Puntos de cruce asignados:")
for par in puntos_cruce:
    print(f"Par {par[0]} - {par[1]}: Punto de cruce = {par[2]}")