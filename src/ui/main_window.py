from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import QCoreApplication
from src.ui.widgets.timer_widget import TimerWidget

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
        
        # Add our cozy Timer widget (passing a reference to this window so it can use notifications)
        self.timer_widget = TimerWidget(self)
        layout.addWidget(self.timer_widget)
        
        # Basic background styling
        self.setStyleSheet("background-color: #EBF5FB;")
        
        # --- System Tray Icon ---
        self.tray_icon = QSystemTrayIcon(self)
        
        # Using a standard system icon as fallback (or we can use our emoji if we have an image, 
        # but standard system information icon works instantly)
        self.tray_icon.setIcon(self.style().standardIcon(self.style().StandardPixmap.SP_MessageBoxInformation))
        
        # Create context menu for tray icon
        tray_menu = QMenu()
        show_action = QAction("Show Fishodoro", self)
        show_action.triggered.connect(self.showNormal)
        quit_action = QAction("Exit", self)
        quit_action.triggered.connect(QCoreApplication.quit)
        
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        
        # Show tray icon in Windows system tray
        self.tray_icon.show()

    def show_notification(self, title, message):
        # Native Windows notification balloon tip
        if self.tray_icon.isVisible():
            self.tray_icon.showMessage(
                title,
                message,
                QSystemTrayIcon.MessageIcon.Information,
                5000  # Notification duration (5 seconds)
            )


