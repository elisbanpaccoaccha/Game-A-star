#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Implementación del algoritmo A*
"""

import heapq
import math

class AStarPathFinder:
    """Implementación del algoritmo A* para encontrar caminos."""
    
    def __init__(self):
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 4 direcciones: arriba, derecha, abajo, izquierda
    
    def heuristic(self, a, b):#Distancia Manhattan como heurística
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def find_path(self, grid, start, goal):
        """Implementación de A* para encontrar el camino óptimo."""
        if not grid or start == goal:
            return [start]
            
        rows, cols = len(grid), len(grid[0])
        
        open_set = []
        counter = 0
        heapq.heappush(open_set, (0, counter, start))
        
        g_score = {start: 0}
        came_from = {}
        
        while open_set:
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
            
            for dx, dy in self.directions:
                neighbor = (current[0] + dx, current[1] + dy)
                
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

