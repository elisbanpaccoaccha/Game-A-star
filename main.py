#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CheatGame - Un juego donde un ratón debe llegar a la meta evitando ser atrapado por un gato.
El gato usa algoritmos de búsqueda (A* por defecto) para perseguir al ratón.
"""

import sys
from PyQt5.QtWidgets import QApplication
from game_window import GameWindow
from pathfinding import AStarPathFinder, PathFinderFactory

def main():
    """Función principal que inicializa y ejecuta el juego."""
    app = QApplication(sys.argv)
    
    # Factory para crear diferentes algoritmos de búsqueda
    path_finder_factory = PathFinderFactory()
    path_finder_factory.register_algorithm("a_star", AStarPathFinder)
    
    # Por defecto, usamos A* pero esto es fácilmente reemplazable
    path_finder = path_finder_factory.create_path_finder("a_star")
    
    # Iniciar la ventana del juego
    window = GameWindow(path_finder)
    window.show()
    
    # Ejecutar la aplicación
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()