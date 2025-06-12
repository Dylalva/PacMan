#Librerias/modulos utilizados
import heapq

from PACMAN.Interface.constants import DOWN, LEFT, RIGHT, STOP, UP, PORTAL

"""
Modulo de 'Servicio' este modulo tendra los metodos necesarios para realizar las busquedas
en el grafo de juego
"""
#=================================================================================================
# Heurística de distancia Manhattan (distancia entre dos puntos en un plano)
def heuristic(nodeA, nodeB):
    (x1, y1) = nodeA.get_coordinate()
    (x2, y2) = nodeB.get_coordinate()
    return abs(x1 - x2) + abs(y1 - y2)  # Calcular la distancia Manhattan entre dos puntos

# Algoritmo A* para buscar el camino mas corto
#Fuente base: https://www.geeksforgeeks.org/a-search-algorithm-in-python/
# El metodo fue adaptado para este proyecto
def a_star_search(nodeStart, nodeGoal):
    # Verificar si las posiciones de inicio o destino son inválidas
    if not nodeStart or not nodeGoal:
        print("Posiciones de inicio o destino inválidas")
        return None

    # Inicializar la lista abierta (open list) como una cola de prioridad
    frontier = []
    heapq.heappush(frontier, (0.0, nodeStart))  # Añadir el nodo inicial a la lista (prioridad, nodo)
    came_from = {}  # Diccionario para rastrear de dónde vino cada nodo
    cost_so_far = {}  # Diccionario para almacenar el costo total hasta cada nodo

    came_from[nodeStart] = None
    cost_so_far[nodeStart] = 0

    while frontier:
        # Obtener el nodo con el menor valor de f (prioridad)
        _, current = heapq.heappop(frontier)

        # Verificar si actual alcanzó al nodo objetivo
        if current == nodeGoal:
            break

        # Para cada vecino del nodo actual
        for neighbor, weight in current.get_neighbors():
            new_cost = cost_so_far[current] + weight  # Calcular el nuevo costo hasta el vecino
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, nodeGoal)
                heapq.heappush(frontier, (priority, neighbor))
                came_from[neighbor] = current  # Registrar de dónde vino el vecino

    return came_from, cost_so_far  # Devolver el camino y los costos


#Metodo adaptado en base al metodo A*
def a_star_search_forbidden(nodeStart, nodeGoal, forbidden_nodes):
    if not nodeStart or not nodeGoal:
        print("Posiciones de inicio o destino inválidas")
        return None
    if not isinstance(forbidden_nodes, list):
        forbidden_nodes = [forbidden_nodes]  # Convertir a lista si es un solo nodo
    # Inicializar la lista abierta (open list) como una cola de prioridad
    frontier = []
    heapq.heappush(frontier, (0.0, nodeStart))  # Añadir el nodo inicial a la lista (prioridad, nodo)
    came_from = {}  # Diccionario para rastrear de dónde vino cada nodo
    cost_so_far = {}  # Diccionario para almacenar el costo total hasta cada nodo

    came_from[nodeStart] = None
    cost_so_far[nodeStart] = 0

    while frontier:
        # Obtener el nodo con el menor valor de f (prioridad)
        _, current = heapq.heappop(frontier)

        # Verificar si el nodo actual es el nodo prohibido o está en la lista de nodos prohibidos
        if current == nodeGoal:
            break

        # Para cada vecino del nodo actual
        for neighbor, weight in current.get_neighbors():
            if neighbor in forbidden_nodes and neighbor == nodeGoal:
                print(f"Nodo prohibido: {neighbor}")
                continue
            new_cost = cost_so_far[current] + weight  # Calcular el nuevo costo hasta el vecino
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, nodeGoal)
                heapq.heappush(frontier, (priority, neighbor))
                came_from[neighbor] = current  # Registrar de dónde vino el vecino
    if nodeGoal not in came_from:
        came_from[nodeGoal] = None  # Marcar el nodo como no alcanzable
        print("No se encontró un camino al nodo objetivo")
    return came_from, cost_so_far  # Devolver el camino y los costos


#Metodo adaptado en base al metodo A*
def a_star_search_with_direction(nodeStart, nodeGoal, initial_direction):
    if not nodeStart or not nodeGoal:
        print("Posiciones de inicio o destino inválidas")
        return None, None

    frontier = []
    heapq.heappush(frontier, (0.0, nodeStart, initial_direction))
    came_from = {}
    cost_so_far = {}

    came_from[nodeStart] = (None, initial_direction)
    cost_so_far[nodeStart] = 0

    direction_opposite = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT, STOP: STOP}

    while frontier:
        _, current, current_direction = heapq.heappop(frontier)

        if current == nodeGoal:
            break

        for neighbor, weight, direction in current.get_neighbors_with_direction():
            if direction != PORTAL and direction_opposite.get(current_direction) == direction and current_direction != STOP:
                continue

            new_cost = cost_so_far[current] + weight
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, nodeGoal)
                heapq.heappush(frontier, (priority, neighbor, direction))
                came_from[neighbor] = (current, direction) # Marcar el nodo como no alcanzable
    return came_from, cost_so_far

#Metodo auxiliar por si el fantasma no encuentra una ruta accesible
def move_any_node(start, goal):
    if not start:
        return None
    neighbors = start.get_neighbors()
    node_ear = None
    mini = float('inf')
    for neighbor,_ in neighbors:
        heuristic_value = heuristic(neighbor, goal)
        if heuristic_value < mini:
            mini = heuristic_value
            node_ear = neighbor

    return node_ear