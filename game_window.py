#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Esta parte del codigo es la interfaz UI -> usando QT5
Ademas del manejo la lógica del juego.
"""

import random
import time
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QPainter, QColor, QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QTimer, QRect, QPoint

class GameObject:    
    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
    
    def draw(self, painter):
        painter.fillRect(self.x * self.size, self.y * self.size, 
                        self.size, self.size, self.color)
    
    def get_position(self):
        return (self.x, self.y)
    
    def set_position(self, x, y):
        self.x = x
        self.y = y

class Mouse(GameObject): # control para el manejo por el usuario por teclas o keywords
    
    def __init__(self, x, y, size):
        super().__init__(x, y, size, QColor(200, 200, 255))
    
    def draw(self, painter):
        painter.setBrush(self.color)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(
            self.x * self.size, 
            self.y * self.size, 
            self.size, 
            self.size
        )

class Cat(GameObject): #control para el manejo del algoritmo de busqueda que usara el gato
    
    def __init__(self, x, y, size, path_finder):
        super().__init__(x, y, size, QColor(255, 120, 120))
        self.path_finder = path_finder
        self.path = []
        self.last_update = time.time()
        self.update_interval = 0.2  # Renderizado por segundos entre actualizaciones del camino
    
    def draw(self, painter):
        """Dibuja el gato en forma de cuadrado con borde."""
        painter.setBrush(self.color)
        painter.setPen(QColor(200, 40, 40))
        painter.drawRect(
            self.x * self.size, 
            self.y * self.size, 
            self.size, 
            self.size
        )

        if self.path:
            painter.setPen(QColor(255, 140, 140, 100))
            for x, y in self.path[1:]:  # Excluimos la posición actual
                painter.drawRect(
                    x * self.size + self.size // 4, 
                    y * self.size + self.size // 4, 
                    self.size // 2, 
                    self.size // 2
                )
    
    def update_path(self, grid, target_pos): #actualizaion dle algoritmo de busqueda hacia el objetivo (raton) en cada movimiento
        current_time = time.time()
        if current_time - self.last_update >= self.update_interval:
            self.path = self.path_finder.find_path(grid, (self.x, self.y), target_pos)
            self.last_update = current_time

    def move(self):
        if len(self.path) > 1: 
            next_pos = self.path[1] 
            self.x, self.y = next_pos
            # Actualizamos el camino para eliminar la posición a la que nos movimos
            self.path = self.path[1:]

class Goal(GameObject): #esta clase es para la meta

    def __init__(self, x, y, size):
        super().__init__(x, y, size, QColor(120, 255, 120))
    
    def draw(self, painter):
        painter.setBrush(self.color)
        painter.setPen(Qt.NoPen)
        
        center_x = self.x * self.size + self.size // 2
        center_y = self.y * self.size + self.size // 2
        radius = self.size // 2

        painter.drawEllipse(
            self.x * self.size, 
            self.y * self.size, 
            self.size, 
            self.size
        )

class Wall(GameObject): #aqui creamos los obtaculos que estaran en el juego de manera ramdon
    
    def __init__(self, x, y, size):
        super().__init__(x, y, size, QColor(80, 80, 80))

class GameArea(QWidget): #en esta clase se encuentra el area de juego es decir el mapa
    
    def __init__(self, parent, path_finder):
        super().__init__(parent)
        self.setFocusPolicy(Qt.StrongFocus)
        
        # Configuración del mapa
        self.grid_size = 20  # Tamaño en píxeles de cada celda
        self.grid_width = 30  # Número de celdas horizontales
        self.grid_height = 20  # Número de celdas verticales
        
        self.grid = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        
        # Objetos del juego
        self.path_finder = path_finder
        self.mouse = Mouse(1, 1, self.grid_size)
        self.cat = Cat(self.grid_width - 2, self.grid_height - 2, self.grid_size, path_finder)
        self.goal = Goal(self.grid_width - 2, 1, self.grid_size)
        self.walls = []
        
        # Estado del juego, para ver si gano o no el raton
        self.game_over = False
        self.game_won = False
        self.move_directions = {
            Qt.Key_Up: (0, -1),
            Qt.Key_Down: (0, 1),
            Qt.Key_Left: (-1, 0),
            Qt.Key_Right: (1, 0),
        }
        
        self.game_timer = QTimer(self)
        self.game_timer.timeout.connect(self.update_game)
        self.game_timer.start(200)  # Actualiza el juego cada 100ms (ajustable)
        
        self.generate_walls()
        
        self.setFixedSize(self.grid_width * self.grid_size, self.grid_height * self.grid_size)
    
    def generate_walls(self): #genera las paredes aleatorias
        self.walls = []
        
        self.grid = [[0 for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        
        num_walls = int(self.grid_width * self.grid_height * 0.2)  # 20% del área
        
        reserved_positions = [
            self.mouse.get_position(),
            self.cat.get_position(),
            self.goal.get_position()
        ]
        
        walls_added = 0
        while walls_added < num_walls:
            x = random.randint(0, self.grid_width - 1)
            y = random.randint(0, self.grid_height - 1)
            
            if (x, y) not in reserved_positions and self.grid[y][x] == 0:
                self.grid[y][x] = 1
                self.walls.append(Wall(x, y, self.grid_size))
                walls_added += 1
        
        # Nos aseguramos que hay un camino válido del ratón a la meta
        mouse_pos = self.mouse.get_position()
        goal_pos = self.goal.get_position()
        
        path = self.path_finder.find_path(self.grid, mouse_pos, goal_pos)
        
        if not path:
            self.generate_walls()
    
    def paintEvent(self, event): #esta funcion evalua el estado del juego es decir dibuja todo el mapa para que se vea
        painter = QPainter(self)
        
        painter.fillRect(0, 0, self.width(), self.height(), QColor(240, 240, 240))
        
        painter.setPen(QColor(220, 220, 220))
        for i in range(self.grid_width + 1):
            painter.drawLine(i * self.grid_size, 0, i * self.grid_size, self.height())
        for i in range(self.grid_height + 1):
            painter.drawLine(0, i * self.grid_size, self.width(), i * self.grid_size)
        
        for wall in self.walls:
            wall.draw(painter)
    
        self.goal.draw(painter)
        
        self.mouse.draw(painter)
        
        self.cat.draw(painter)
        
        if self.game_over or self.game_won:
            painter.fillRect(0, 0, self.width(), self.height(), QColor(0, 0, 0, 150))
            painter.setPen(QColor(255, 255, 255))
            painter.setFont(QFont('Arial', 20, QFont.Bold))
            
            message = "¡GANASTE!" if self.game_won else "¡PERDISTE!"
            
            # Centrar texto
            rect = QRect(0, 0, self.width(), self.height())
            painter.drawText(rect, Qt.AlignCenter, message)
    
    def update_game(self):
        if self.game_over or self.game_won:
            return

        self.cat.update_path(self.grid, self.mouse.get_position())
        
        self.cat.move()
        
        if self.cat.get_position() == self.mouse.get_position():
            self.game_over = True
            self.game_timer.stop()
            
        if self.mouse.get_position() == self.goal.get_position():
            self.game_won = True
            self.game_timer.stop()
            
        self.update()
    
    def keyPressEvent(self, event): #manejo del teclado para el raton
        if self.game_over or self.game_won:
            if event.key() == Qt.Key_R:
                self.reset_game()
            return
        
        if event.key() in self.move_directions:
            dx, dy = self.move_directions[event.key()]
            new_x = self.mouse.x + dx
            new_y = self.mouse.y + dy
            
            if 0 <= new_x < self.grid_width and 0 <= new_y < self.grid_height:
                if self.grid[new_y][new_x] == 0:
                    self.mouse.set_position(new_x, new_y)
        
        self.update()
    
    def reset_game(self):
        self.mouse.set_position(1, 1)
        self.cat.set_position(self.grid_width - 2, self.grid_height - 2)
        self.game_over = False
        self.game_won = False
        self.generate_walls()
        self.game_timer.start()

class GameWindow(QMainWindow):
    
    def __init__(self, path_finder):
        super().__init__()
        
        self.path_finder = path_finder
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('CheatGame - Gato vs Ratón')
        #self.setWindowIcon(QIcon('icon.png'))
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        
        self.game_area = GameArea(self, self.path_finder)
        layout.addWidget(self.game_area)
        
        info_label = QLabel("Controles: Flechas - Mover ratón | presione R - para reiniciar el juego")
        info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label)
        
        restart_button = QPushButton("Reiniciar")
        restart_button.clicked.connect(self.game_area.reset_game)
        layout.addWidget(restart_button)
        
        self.adjustSize()
        
        self.center()
    
    def center(self):
        frame_geometry = self.frameGeometry()
        screen_center = self.screen().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())