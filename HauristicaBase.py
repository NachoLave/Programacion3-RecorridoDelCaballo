# Importamos la librería 'time' para medir el tiempo de ejecución
import time

# Tamaño del tablero de ajedrez
N = 9 
inicio = time.time()

# Movimientos posibles del caballo en el tablero
movimientos_caballo = [
    (2, 1),
    (1, 2),
    (-1, 2),
    (-2, 1),
    (-2, -1),
    (-1, -2),
    (1, -2),
    (2, -1),
]

# Inicialización del tablero de ajedrez
tablero = [[-1 for _ in range(N)] for _ in range(N)]

# Contadores globales para total de nodos y soluciones encontradas
total_nodos = 0
total_soluciones = 0


# Función para verificar si una posición es válida en el tablero
def es_valido(x, y, tablero):
    return 0 <= x < N and 0 <= y < N and tablero[x][y] == -1


# Heurística de Warnsdorff: calcula el número de movimientos posibles desde una posición dada
def contar_opciones_futuras(x, y, tablero):
    count = 0
    for mov in movimientos_caballo:
        nx, ny = x + mov[0], y + mov[1]
        if es_valido(nx, ny, tablero):
            count += 1
    return count


# Función de Backtracking para resolver el recorrido del caballo
def recorrido_caballo(x, y, movimiento, tablero, contador_nodos, contador_backtrack):
    # Incrementa el contador de nodos visitados
    contador_nodos[0] += 1

    # Caso base: si el tablero está completo, se encontró una solución
    if movimiento == N * N:
        return True

    # Generar todos los movimientos posibles desde la posición actual
    # Ordenarlos según la heurística de Warnsdorff para minimizar opciones futuras
    movimientos_ordenados = sorted(
        movimientos_caballo,
        key=lambda m: contar_opciones_futuras(x + m[0], y + m[1], tablero),
    )

    # Intentar cada movimiento posible, en el orden de prioridad
    for mov in movimientos_ordenados:
        nx, ny = x + mov[0], y + mov[1]
        if es_valido(nx, ny, tablero):
            # Marcar el movimiento en el tablero
            tablero[nx][ny] = movimiento
            # Llamada recursiva para el siguiente movimiento
            if recorrido_caballo(
                nx, ny, movimiento + 1, tablero, contador_nodos, contador_backtrack
            ):
                return True
            # Desmarcar si no lleva a una solución (backtracking)
            tablero[nx][ny] = -1
            # Incrementa el contador de backtracking
            contador_backtrack[0] += 1

    return False


# Función para iniciar el recorrido del caballo
def resolver_recorrido_inicial(x_inicio, y_inicio):
    global total_nodos, total_soluciones
    # Inicializar el tablero y los contadores
    tablero = [[-1 for _ in range(N)] for _ in range(N)]
    tablero[x_inicio][y_inicio] = 0  # Empezar desde la posición inicial
    contador_nodos = [0]  # Contador de nodos visitados
    contador_backtrack = [0]  # Contador de veces que se hace backtracking

    # Medir el tiempo de ejecución
    start_time = time.time()
    if recorrido_caballo(
        x_inicio, y_inicio, 1, tablero, contador_nodos, contador_backtrack
    ):
        end_time = time.time()
        print(f"Solución encontrada en {end_time - start_time:.4f} segundos")
        print("Nodos visitados en esta solución:", contador_nodos[0])
        print("Backtracking realizado en esta solución:", contador_backtrack[0])
        for fila in tablero:
            print(fila)

        # Actualizar contadores globales
        total_nodos += contador_nodos[0]
        total_soluciones += 1
    else:
        total_nodos += contador_nodos[0]
        print("No se encontró solución")


# Iniciar el recorrido desde varias posiciones en el tablero
if N % 2 == 1:
    for x in range(0, N): 
        if x % 2 == 1:
            for y in range(1, N, 2):
                print(f"Probando inicio en: ({x}, {y})")
                resolver_recorrido_inicial(x, y)
                print(
                    "--------------------"
            )
        else:
            for y in range(0, N, 2):
                print(f"Probando inicio en: ({x}, {y})")
                resolver_recorrido_inicial(x, y)
                print(
                    "--------------------"
                )  # Separador de resultados para cada posición inicial del tablero

    # Mostrar el total de nodos visitados y soluciones encontradas
    print("Tiempo total de ejecución:", time.time() - inicio)
    print("Total de nodos visitados en todas las soluciones:", total_nodos)
    print("Total de soluciones encontradas:", total_soluciones)
else:
    
    for x in range(N):
        for y in range(N):
            print(f"Probando inicio en: ({x}, {y})")
            resolver_recorrido_inicial(x, y)
            print(
                "--------------------"
        )
        

    # Mostrar el total de nodos visitados y soluciones encontradas
    print("Tiempo total de ejecución:", time.time() - inicio)
    print("Total de nodos visitados en todas las soluciones:", total_nodos)
    print("Total de soluciones encontradas:", total_soluciones)
