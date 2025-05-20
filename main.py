#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CheatGame - Un juego donde un ratón debe llegar a la meta evitando ser atrapado por un gato.
El gato usa algoritmos de búsqueda (A* u otros algoritmos los cuales se podran agregar en el futuro) para perseguir al ratón.
"""

#esta parte del codigo es solamente para la inicializacion y selccion del algoritmo de busqueda
import sys
from PyQt5.QtWidgets import QApplication, QComboBox, QVBoxLayout, QLabel, QDialog, QPushButton
from game_window import GameWindow

# Importamos los diferentes algoritmos de pathfinding
from AStar import AStarPathFinder
from bfs_pathfinder import BFSPathFinder

def select_algorithm():
    """Muestra un diálogo para seleccionar el algoritmo de pathfinding."""
    dialog = QDialog()
    dialog.setWindowTitle("Seleccionar Algoritmo de Pathfinding")
    dialog.setMinimumWidth(300)
    
    layout = QVBoxLayout()
    
    label = QLabel("Selecciona el algoritmo de búsqueda:")
    layout.addWidget(label)
    
    combo = QComboBox()
    combo.addItem("A* (A-Star)", "astar")
    combo.addItem("BFS (Breadth-First Search)", "bfs") #ejemplo de como agregar mas algoritmos de busqueda
    layout.addWidget(combo)
    
    button = QPushButton("Aceptar")
    layout.addWidget(button)
    
    dialog.setLayout(layout)
    
    # Variable para almacenar la selección
    selected = ["astar"]
    
    def on_accept():
        selected[0] = combo.currentData()
        dialog.accept()
    
    button.clicked.connect(on_accept)
    dialog.exec_()
    
    return selected[0]

def create_pathfinder(algorithm_name):
    """Crea una instancia del algoritmo de pathfinding seleccionado."""
    if algorithm_name == "bfs":
        return BFSPathFinder()
    else:  # Por defecto, usamos A*
        return AStarPathFinder()

def main():
    app = QApplication(sys.argv)
    
    # Seleccionar el algoritmo de pathfinding
    algorithm_name = select_algorithm()
    
    # Crear la instancia del pathfinder seleccionado
    path_finder = create_pathfinder(algorithm_name)
    
    window = GameWindow(path_finder)
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()