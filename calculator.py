import sys
import math
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout, 
                             QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scientific Calculator - Techonet Day 2")
        self.setFixedSize(400, 550)
        self.setStyleSheet("background-color: #1e1e2e;")
        
        # Variables
        self.current_input = ""
        self.memory = 0
        self.is_dark_mode = True
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Display
        self.display = QLineEdit()
        self.display.setFixedHeight(80)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setText("0")
        self.display.setFont(QFont("Segoe UI", 24, QFont.Bold))
        self.display.setStyleSheet("""
            QLineEdit {
                background-color: #181825;
                color: #cdd6f4;
                border: 2px solid #313244;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        main_layout.addWidget(self.display)
        
        # Memory + Theme buttons
        mem_layout = QHBoxLayout()
        for text, func in [("MC", self.memory_clear), ("MR", self.memory_recall), 
                          ("M+", self.memory_add), ("M-", self.memory_sub),
                          ("🌙", self.toggle_theme)]:
            btn = self.create_button(text, func, "#89b4fa", height=35)
            mem_layout.addWidget(btn)
        main_layout.addLayout(mem_layout)
        
        # Main buttons grid
        grid = QGridLayout()
        grid.setSpacing(8)
        
        buttons = [
            ('C', self.clear, '#f38ba8'), ('DEL', self.backspace, '#f38ba8'), 
            ('%', self.add_operator, '#f9e2af'), ('÷', self.add_operator, '#f9e2af'),
            ('7', self.add_digit, '#313244'), ('8', self.add_digit, '#313244'),
            ('9', self.add_digit, '#313244'), ('×', self.add_operator, '#f9e2af'),
            ('4', self.add_digit, '#313244'), ('5', self.add_digit, '#313244'),
            ('6', self.add_digit, '#313244'), ('-', self.add_operator, '#f9e2af'),
            ('1', self.add_digit, '#313244'), ('2', self.add_digit, '#313244'),
            ('3', self.add_digit, '#313244'), ('+', self.add_operator, '#f9e2af'),
            ('√', self.sqrt, '#89b4fa'), ('0', self.add_digit, '#313244'),
            ('.', self.add_decimal, '#313244'), ('=', self.calculate, '#a6e3a1'),
            ('x²', self.square, '#89b4fa'), ('π', self.add_pi, '#89b4fa'),
            ('sin', self.sin, '#89b4fa'), ('cos', self.cos, '#89b4fa')
        ]
        
        row, col = 0, 0
        for text, func, color in buttons:
            btn = self.create_button(text, func, color)
            if text == '=':
                btn.setStyleSheet(btn.styleSheet() + "font-size: 20px;")
            grid.addWidget(btn, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        main_layout.addLayout(grid)
        
    def create_button(self, text, func, color, height=55):
        """Helper to create styled buttons"""
        btn = QPushButton(text)
        btn.setFixedHeight(height)
        btn.setFont(QFont("Segoe UI", 14, QFont.Bold))
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: {'#1e1e2e' if color != '#313244' else '#cdd6f4'};
                border: none;
                border-radius: 10px;
            }}
            QPushButton:hover {{
                background-color: {self.lighten_color(color)};
            }}
            QPushButton:pressed {{
                background-color: {self.darken_color(color)};
            }}
        """)
        btn.clicked.connect(func)
        return btn
    
    def lighten_color(self, hex_color):
        return "#45475a" if hex_color == "#313244" else hex_color
    
    def darken_color(self, hex_color):
        return "#1e1e2e" if hex_color == "#313244" else hex_color
    
    # Core Functions
    def add_digit(self):
        sender = self.sender().text()
        if self.current_input == "0" or self.current_input == "Error":
            self.current_input = sender
        else:
            self.current_input += sender
        self.update_display()
    
    def add_decimal(self):
        parts = self.current_input.split() if