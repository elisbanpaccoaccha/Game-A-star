#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Implementación del algoritmo BFS (Breadth-First Search) para pathfinding. solo un ejemplo
"""

from collections import deque

class BFSPathFinder:
    """Implementación del algoritmo BFS para encontrar caminos."""
    
    def __init__(self):
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 4 direcciones: arriba, derecha, abajo, izquierda
    
    def find_path(self, grid, start, goal):
        """
        Implementación de BFS para encontrar un camino.
        
        Args:
            grid: Matriz 2D que representa el mapa (0 = libre, 1 = ocupado)
            start: Tupla (x, y) con la posición inicial
            goal: Tupla (x, y) con la posición objetivo
            
        Returns:
            Una lista de tuplas (x, y) representando el camino, o una lista vacía si no hay camino.
        """
        if not grid or start == goal:
            return [start]
            
        rows, cols = len(grid), len(grid[0])
        
        # Cola para BFS
        queue = deque([start])
        
        # Diccionario para rastrear el camino
        came_from = {start: None}
        
        while queue:
            current = queue.popleft()
            
            # Si llegamos al objetivo, reconstruir el camino
            if current == goal:
                path = []
                while current != start:
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
                
                # Si no hemos visitado este vecino antes
                if neighbor not in came_from:
                    queue.append(neighbor)
                    came_from[neighbor] = current
        
        # No se encontró camino
        return []
