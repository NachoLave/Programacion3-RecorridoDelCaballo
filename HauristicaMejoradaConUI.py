# Importamos la librería 'time' para medir el tiempo de ejecución
import time

import tkinter as tk
from tkinter import messagebox

# Tamaño del tablero de ajedrez
# N = 8

# inicio_x, inicio_y = 4, 2  # Coordenadas de inicio, ajustables


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

# # Inicialización del tablero de ajedrez
# tablero = [[-1 for _ in range(N)] for _ in range(N)]


# Función para verificar si una posición es válida en el tablero
def es_valido(x, y, tablero, N):
    return 0 <= x < N and 0 <= y < N and tablero[x][y] == -1


# Heurística de Warnsdorff modificada: clasifica los movimientos primero por paridad y luego por la cantidad de movimientos posibles
def ordenar_movimientos(x, y, tablero, N):
    movimientos_ordenados = []

    # Crear dos listas para las posiciones (par, par) y (impar, impar) por un lado,
    # y (par, impar) o (impar, par) por otro
    movimientos_par_impar = []
    movimientos_impar_par = []

    for mov in movimientos_caballo:
        nx, ny = x + mov[0], y + mov[1]
        if es_valido(nx, ny, tablero, N):
            # Verificar si la casilla destino es (par, par) o (impar, impar) o (par, impar) o (impar, par)
            if (nx + ny) % 2 == 0:  # (par, par) o (impar, impar)
                movimientos_par_impar.append(
                    (nx, ny, contar_opciones_futuras(nx, ny, tablero, N))
                )
            else:  # (par, impar) o (impar, par)
                movimientos_impar_par.append(
                    (nx, ny, contar_opciones_futuras(nx, ny, tablero, N))
                )

    # Ordenar ambos grupos por la cantidad de movimientos futuros (menor cantidad primero)
    movimientos_par_impar.sort(key=lambda m: m[2])
    movimientos_impar_par.sort(key=lambda m: m[2])

    # Concatenar ambos grupos
    movimientos_ordenados.extend(movimientos_par_impar)
    movimientos_ordenados.extend(movimientos_impar_par)

    # Solo devolver las posiciones sin el conteo de movimientos futuros
    return [(nx, ny) for nx, ny, _ in movimientos_ordenados]


# Función para contar las opciones futuras de un movimiento
def contar_opciones_futuras(x, y, tablero, N):
    count = 0
    for mov in movimientos_caballo:
        nx, ny = x + mov[0], y + mov[1]
        if es_valido(nx, ny, tablero, N):
            count += 1
    return count


# Función de Backtracking para resolver el recorrido del caballo
def recorrido_caballo(x, y, N, movimiento, tablero, contador_nodos, contador_backtrack, recorrido):
    # Incrementa el contador de nodos visitados
    contador_nodos[0] += 1

    # Caso base: si el tablero está completo, se encontró una solución
    if movimiento == N * N:
        return True

    # Generar todos los movimientos posibles desde la posición actual, ordenados según la nueva heurística
    movimientos_ordenados = ordenar_movimientos(x, y, tablero, N)

    # Intentar cada movimiento posible, en el orden de prioridad
    for nx, ny in movimientos_ordenados:
        if es_valido(nx, ny, tablero, N):
            # Marcar el movimiento en el tablero
            tablero[nx][ny] = movimiento
            recorrido.append((nx, ny))
            # Llamada recursiva para el siguiente movimiento
            if recorrido_caballo(
                nx, ny, N, movimiento + 1, tablero, contador_nodos, contador_backtrack, recorrido
            ):
                return True
            # Desmarcar si no lleva a una solución (backtracking)
            tablero[nx][ny] = -1
            recorrido.pop()
            # Incrementa el contador de backtracking
            contador_backtrack[0] += 1

    return False


# Función para iniciar el recorrido del caballo
def resolver_recorrido_inicial(x_inicio, y_inicio, N):
    # Inicializar el tablero y los contadores
    tablero = [[-1 for _ in range(N)] for _ in range(N)]
    tablero[x_inicio][y_inicio] = 0  # Empezar desde la posición inicial
    recorrido = [(x_inicio, y_inicio)]
    contador_nodos = [0]  # Contador de nodos visitados
    contador_backtrack = [0]  # Contador de veces que se hace backtracking

    # Medir el tiempo de ejecución
    start_time = time.time()
    if recorrido_caballo(
        x_inicio, y_inicio, N, 1, tablero, contador_nodos, contador_backtrack, recorrido
    ):
        end_time = time.time() - start_time
        # print(f"Solución encontrada en {end_time - start_time:.4f} segundos")
        # print("Recorrido:", recorrido)
        # print("Nodos visitados:", contador_nodos[0])
        # print("Backtracking realizado:", contador_backtrack[0])
        # for fila in tablero:
        #     print(fila)
        solucion_encontrada = True
    else:
        print("No se encontró solución")
        solucion_encontrada = False
        
    return solucion_encontrada, recorrido, end_time, contador_nodos[0], contador_backtrack[0]


# Iniciar el recorrido desde una posición inicial en el tablero (por ejemplo, esquina superior izquierda)
# for x in range(0, N, 2):
#     for y in range(0, N, 2):
#         print(f"Probando inicio en: ({x}, {y})")
#         resolver_recorrido_inicial(x, y)
#         print(
#             "--------------------"
#         )  # Separador de resultados para cada posición inicial del tablero

print(time.time() - inicio)



# Crear interfaz gráfica para la visualización del recorrido
class InterfazCaballo:
    def __init__(self, root, recorrido, tiempo_resolucion, nodos_visitados, backtracking_realizado, N):
        self.root = root
        self.root.title("Recorrido del Caballo")
        self.recorrido = recorrido
        self.tiempo_resolucion = tiempo_resolucion
        self.paso = 0
        self.automatico = False
        self.movimiento_activo = False

        # Crear el tablero
        self.canvas = tk.Canvas(root, width=50 * N, height=50 * N)
        self.canvas.pack()

        self.N = N
        
        # Dibujar el tablero
        self.dibujar_tablero()

        # Mostrar el tiempo de resolución
        self.label_tiempo = tk.Label(root, text=f"Tiempo de resolución: {self.tiempo_resolucion:.6f} segundos")
        self.label_tiempo.pack()
        
        # Mostrar el número de nodos visitados
        self.label_nodos = tk.Label(root, text=f"Nodos visitados: {nodos_visitados}")
        self.label_nodos.pack()
        
        # Mostrar el número de veces que se realizó backtracking
        self.label_backtrack = tk.Label(root, text=f"Backtracking realizado: {backtracking_realizado}")
        self.label_backtrack.pack()
        
        # Separador
        self.separador = tk.Label(root, text="----------------------------------")
        self.separador.pack()
        
        
        
        # self.boton_auto = tk.Button(root, text="Iniciar", command=self.toggle_movimiento)
        # self.boton_auto.pack(padx=10)
        
        # self.boton_detener = tk.Button(root, text="Detener Movimiento", command=self.detener_movimiento)
        # self.boton_detener.pack( padx=10)
        
        
        # Botones para avanzar y retroceder en los pasos del recorrido
        self.boton_anterior = tk.Button(root, text="Paso Anterior", command=self.mostrar_paso_anterior)
        self.boton_anterior.pack(side="left", padx=10, pady=10)
        
        self.boton_toggle = tk.Button(root, text="Iniciar", command=self.toggle_movimiento)
        self.boton_toggle.pack(side="left", padx=10)
        
        self.boton_siguiente = tk.Button(root, text="Siguiente Paso", command=self.mostrar_siguiente_paso)
        self.boton_siguiente.pack(side="left", padx=10, pady=10)
        
    def toggle_movimiento(self):
        if self.movimiento_activo:
            self.detener_movimiento()
            self.boton_toggle.config(text="Iniciar")
        else:
            self.iniciar_movimiento_automatico()
            self.boton_toggle.config(text="Detener Movimiento")
        self.movimiento_activo = not self.movimiento_activo

    def dibujar_tablero(self):
        # Crear celdas del tablero
        for i in range(self.N):
            for j in range(self.N):
                color = "white" if (i + j) % 2 == 0 else "gray"
                self.canvas.create_rectangle(j * 50, i * 50, (j + 1) * 50, (i + 1) * 50, fill=color)
    
    def mostrar_siguiente_paso(self):
        # Mostrar siguiente paso del recorrido
        if self.paso < len(self.recorrido):
            x, y = self.recorrido[self.paso]
            color = "blue" if self.paso != 0 else "red"  # Azul para pasos normales, rojo para el inicio
            self.canvas.create_text(y * 50 + 25, x * 50 + 25, text=str(self.paso + 1), fill=color, font=("Arial", 20))
            
            # self.canvas.create_oval(y * 50 + 10, x * 50 + 10, y * 50 + 40, x * 50 + 40, fill=color)
            self.paso += 1
            if self.automatico:
                self.root.after(500, self.mostrar_siguiente_paso)
        else:
            self.automatico = False  # Detener el avance automático al final del recorrido
            messagebox.showinfo("Recorrido completo", "El caballo ha completado su recorrido.")
    
    def mostrar_paso_anterior(self):
        # Retroceder un paso en el recorrido
        if self.paso > 0:
            self.paso -= 1
            x, y = self.recorrido[self.paso]
            # Redibuja la celda actual para "borrar" el paso del caballo
            color = "white" if (x + y) % 2 == 0 else "gray"
            self.canvas.create_rectangle(y * 50, x * 50, (y + 1) * 50, (x + 1) * 50, fill=color)
            
    def iniciar_movimiento_automatico(self):
        if not self.automatico:
            self.automatico = True
            self.mostrar_siguiente_paso()

    def detener_movimiento(self):
        self.automatico = False

# Crear ventana para configurar el tablero y posición inicial
class VentanaConfiguracion:
    def __init__(self, root):
        self.root = root
        self.root.title("Configuración del Tablero")

        # Etiquetas y entradas
        self.label_tamaño = tk.Label(root, text="Tamaño del tablero (N):")
        self.label_tamaño.pack()
        self.entry_tamaño = tk.Entry(root)
        self.entry_tamaño.insert(0, "7")  # Valor por defecto
        self.entry_tamaño.pack()

        self.label_inicio = tk.Label(root, text="Posición inicial del caballo (x, y):")
        self.label_inicio.pack()
        self.entry_inicio_x = tk.Entry(root)
        self.entry_inicio_x.insert(0, "0")  # Valor por defecto
        self.entry_inicio_x.pack()
        self.entry_inicio_y = tk.Entry(root)
        self.entry_inicio_y.insert(0, "0")  # Valor por defecto
        self.entry_inicio_y.pack()

        # Botón para guardar configuración
        self.boton_guardar = tk.Button(root, text="Guardar y Continuar", command=self.guardar_configuracion)
        self.boton_guardar.pack()

    def guardar_configuracion(self):
        try:
            # Obtener valores de la entrada
            N = int(self.entry_tamaño.get())
            inicio_x = int(self.entry_inicio_x.get())
            inicio_y = int(self.entry_inicio_y.get())

            # Validar los valores
            if N <= 0 or inicio_x < 0 or inicio_x >= N or inicio_y < 0 or inicio_y >= N:
                raise ValueError("Valores no válidos.")
            
            # Cerrar la ventana de configuración
            self.root.destroy()

            # Llamar a la función de resolución del tablero con los valores proporcionados
            self.iniciar_visualizacion(N, inicio_x, inicio_y)
        except ValueError as e:
            messagebox.showerror("Error de configuración", f"Por favor ingrese valores válidos.\n{e}")

    def iniciar_visualizacion(self, N, inicio_x, inicio_y):
        solucion_encontrada, recorrido, tiempo_resolucion, contador_nodos, contador_backtrack = resolver_recorrido_inicial(inicio_x, inicio_y, N)

        if solucion_encontrada:
            root = tk.Tk()
            interfaz = InterfazCaballo(root, recorrido, tiempo_resolucion, contador_nodos, contador_backtrack, N)
            root.mainloop()
        else:
            messagebox.showinfo("No hay solución", "No se encontró una solución para el recorrido del caballo.")

# Resolver el tablero y obtener la solución
# solucion_encontrada, recorrido, tiempo_resolucion, contador_nodos, contador_backtrack = resolver_recorrido_inicial(inicio_x, inicio_y)
# print(recorrido)
# # Mostrar la interfaz gráfica si hay solución
# if solucion_encontrada:
#     root = tk.Tk()
#     interfaz = InterfazCaballo(root, recorrido, tiempo_resolucion, contador_nodos, contador_backtrack)
#     root.mainloop()
# else:
#     print("No se encontró solución para el recorrido del caballo desde la posición inicial.")

root = tk.Tk()
ventana_config = VentanaConfiguracion(root)
root.mainloop()