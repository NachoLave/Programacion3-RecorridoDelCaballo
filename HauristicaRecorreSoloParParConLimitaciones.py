# Importamos la librería 'time' para medir el tiempo de ejecución
import time

# Tamaño del tablero de ajedrez
N = 7
inicio = time.time()

# Movimientos posibles del caballo en el tablero
movimientos_caballo = [
    (2, 1), (1, 2), (-1, 2), (-2, 1), 
    (-2, -1), (-1, -2), (1, -2), (2, -1),
]

# Límite de movimientos basado en el tamaño del tablero
limite_movimientos = int(N * N * 1.5)

# Inicialización del tablero de ajedrez
tablero = [[-1 for _ in range(N)] for _ in range(N)]

# Función para verificar si una posición es válida en el tablero
def es_valido(x, y, tablero):
    return 0 <= x < N and 0 <= y < N and tablero[x][y] == -1

# Heurística de Warnsdorff modificada: clasifica los movimientos primero por paridad y luego por la cantidad de movimientos posibles
def ordenar_movimientos(x, y, tablero):
    movimientos_ordenados = []
    movimientos_par_impar = []
    movimientos_impar_par = []

    for mov in movimientos_caballo:
        nx, ny = x + mov[0], y + mov[1]
        if es_valido(nx, ny, tablero):
            if (nx + ny) % 2 == 0:
                movimientos_par_impar.append((nx, ny, contar_opciones_futuras(nx, ny, tablero)))
            else:
                movimientos_impar_par.append((nx, ny, contar_opciones_futuras(nx, ny, tablero)))

    movimientos_par_impar.sort(key=lambda m: m[2])
    movimientos_impar_par.sort(key=lambda m: m[2])

    movimientos_ordenados.extend(movimientos_par_impar)
    movimientos_ordenados.extend(movimientos_impar_par)

    return [(nx, ny) for nx, ny, _ in movimientos_ordenados]

# Función para contar las opciones futuras de un movimiento
def contar_opciones_futuras(x, y, tablero):
    count = 0
    for mov in movimientos_caballo:
        nx, ny = x + mov[0], y + mov[1]
        if es_valido(nx, ny, tablero):
            count += 1
    return count

# Función de Backtracking para resolver el recorrido del caballo con poda basada en límite de movimientos
def recorrido_caballo(x, y, movimiento, tablero, contador_nodos, contador_backtrack):
    # Incrementa el contador de nodos visitados
    contador_nodos[0] += 1

    # Caso base: si el tablero está completo, se encontró una solución
    if movimiento == N * N:
        return True

    # Poda: Si el número de movimientos supera el límite máximo permitido, se detiene la exploración
    if contador_nodos[0] > limite_movimientos:
        contador_backtrack[0] += 1
        return False

    # Generar todos los movimientos posibles desde la posición actual, ordenados según la heurística
    movimientos_ordenados = ordenar_movimientos(x, y, tablero)

    # Intentar cada movimiento posible, en el orden de prioridad
    for nx, ny in movimientos_ordenados:
        if es_valido(nx, ny, tablero):
            # Marcar el movimiento en el tablero
            tablero[nx][ny] = movimiento
            # Llamada recursiva para el siguiente movimiento
            if recorrido_caballo(nx, ny, movimiento + 1, tablero, contador_nodos, contador_backtrack):
                return True
            # Desmarcar si no lleva a una solución (backtracking)
            tablero[nx][ny] = -1
            # Incrementa el contador de backtracking
            contador_backtrack[0] += 1

    return False

# Función para iniciar el recorrido del caballo
def resolver_recorrido_inicial(x_inicio, y_inicio):
    tablero = [[-1 for _ in range(N)] for _ in range(N)]
    tablero[x_inicio][y_inicio] = 0  # Empezar desde la posición inicial
    contador_nodos = [0]  # Contador de nodos visitados
    contador_backtrack = [0]  # Contador de veces que se hace backtracking

    # Medir el tiempo de ejecución
    start_time = time.time()
    if recorrido_caballo(x_inicio, y_inicio, 1, tablero, contador_nodos, contador_backtrack):
        end_time = time.time()
        print(f"Solución encontrada en {end_time - start_time:.4f} segundos")
        print("Nodos visitados:", contador_nodos[0])
        print("Backtracking realizado:", contador_backtrack[0])
        for fila in tablero:
            print(fila)
    else:
        print("No se encontró solución")

# Iniciar el recorrido desde una posición inicial en el tablero (por ejemplo, esquina superior izquierda)
for x in range(0, N, 2):
    for y in range(0, N, 2):
        print(f"Probando inicio en: ({x}, {y})")
        resolver_recorrido_inicial(x, y)
        print("--------------------")

print(time.time() - inicio)