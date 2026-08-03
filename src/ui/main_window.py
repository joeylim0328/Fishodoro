from PySide6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget
from PySide6.QtCore import Qt

class FishodoroApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configure the window
        self.setWindowTitle("Fishodoro 🐟")
        self.resize(500, 400)
        
        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Placeholder label
        self.label = QLabel("Welcome to Fishodoro! 🐟⏳\n(Waiting patiently for your instructions...)")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 16px; color: #2C3E50; font-family: Arial;")
        layout.addWidget(self.label)
        
        # Basic background styling
        self.setStyleSheet("background-color: #EBF5FB;")
