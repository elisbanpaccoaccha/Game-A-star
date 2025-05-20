#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Módulo de algoritmos de pathfinding para el juego CheatGame.
Incluye la implementación del algoritmo A* y un factory para crear diferentes algoritmos.
"""

import heapq
from abc import ABC, abstractmethod
import math

class PathFinder(ABC):
    """Clase base abstracta para algoritmos de búsqueda de caminos."""
    
    @abstractmethod
    def find_path(self, grid, start, goal):
        """
        Encuentra un camino del punto de inicio al punto objetivo.
        
        Args:
            grid: Matriz 2D que representa el mapa (0 = libre, 1 = ocupado)
            start: Tupla (x, y) con la posición inicial
            goal: Tupla (x, y) con la posición objetivo
            
        Returns:
            Una lista de tuplas (x, y) representando el camino, o una lista vacía si no hay camino.
        """
        pass

class AStarPathFinder(PathFinder):
    """Implementación del algoritmo A* para encontrar caminos."""
    
    def __init__(self):
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 4 direcciones: arriba, derecha, abajo, izquierda
    
    def heuristic(self, a, b):
        """Distancia Manhattan como heurística."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def find_path(self, grid, start, goal):
        """Implementación de A* para encontrar el camino óptimo."""
        if not grid or start == goal:
            return [start]
            
        rows, cols = len(grid), len(grid[0])
        
        # Cola de prioridad para el algoritmo A*
        open_set = []
        # Formato de la cola: (f_score, contador, posición)
        # f_score = g_score + heurística
        # contador para desempatar cuando f_score es igual
        # posición = (x, y)
        counter = 0
        heapq.heappush(open_set, (0, counter, start))
        
        # Diccionarios para g_score y came_from
        g_score = {start: 0}
        came_from = {}
        
        while open_set:
            # Obtener el nodo con menor f_score
            current_f, _, current = heapq.heappop(open_set)
            
            # Si llegamos al objetivo, reconstruir el camino
            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                return path
            
            # Explorar vecinos
            for dx, dy in self.directions:
                neighbor = (current[0] + dx, current[1] + dy)
                
                # Comprobar si el vecino está dentro de los límites
                if not (0 <= neighbor[0] < cols and 0 <= neighbor[1] < rows):
                    continue
                
                # Comprobar si el vecino es un obstáculo
                if grid[neighbor[1]][neighbor[0]] == 1:
                    continue
                
                # Calcular g_score tentativo
                tentative_g_score = g_score[current] + 1
                
                # Si encontramos un camino mejor, actualizar
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + self.heuristic(neighbor, goal)
                    counter += 1
                    heapq.heappush(open_set, (f_score, counter, neighbor))
        
        # No se encontró camino
        return []

class PathFinderFactory:
    """Fábrica para crear diferentes algoritmos de búsqueda de caminos."""
    
    def __init__(self):
        self.algorithms = {}
    
    def register_algorithm(self, name, algorithm_class):
        """Registra un algoritmo en la fábrica."""
        self.algorithms[name] = algorithm_class
    
    def create_path_finder(self, name):
        """Crea una instancia del algoritmo especificado."""
        if name not in self.algorithms:
            raise ValueError(f"Algoritmo de búsqueda '{name}' no está registrado")
        
        return self.algorithms[name]()