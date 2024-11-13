# Importamos la librería 'time' para medir el tiempo de ejecución
import time

# Tamaño del tablero de ajedrez
N = 5
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
        print("Nodos visitados:", contador_nodos[0])
        print("Backtracking realizado:", contador_backtrack[0])
        for fila in tablero:
            print(fila)
    else:
        print("No se encontró solución")


# Iniciar el recorrido desde una posición inicial en el tablero (por ejemplo, esquina superior izquierda)
for x in range(0, N):
    for y in range(0, N):
        print(f"Probando inicio en: ({x}, {y})")
        resolver_recorrido_inicial(x, y)
        print(
            "--------------------"
        )  # Separador de resultados para cada posición inicial del tablero

print(time.time() - inicio)