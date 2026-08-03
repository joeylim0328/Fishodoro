import sys
from PySide6.QtWidgets import QApplication
from src.ui.main_window import FishodoroApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FishodoroApp()
    window.show()
    sys.exit(app.exec())
