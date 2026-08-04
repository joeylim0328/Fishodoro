from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QSystemTrayIcon, QMenu, QTabWidget, QLabel
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import QCoreApplication, Qt
from src.ui.widgets.timer_widget import TimerWidget

class FishodoroApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configure the window
        self.setWindowTitle("Fishodoro 🐟")
        self.resize(550, 480)  # Slightly enlarged to accommodate tabs and lists
        
        # --- Tab Widget Setup ---
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        
        # Style the Tab Widget to look cozy and aquatic
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #2E86C1;
                border-radius: 8px;
                background-color: #EBF5FB;
                padding: 10px;
            }
            QTabBar::tab {
                background-color: #D4E6F1;
                color: #1F618D;
                font-weight: bold;
                padding: 8px 15px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                margin-right: 4px;
            }
            QTabBar::tab:selected, QTabBar::tab:hover {
                background-color: #2E86C1;
                color: white;
            }
        """)
        
        # Tab 1: 🎣 Fishing Deck
        self.timer_widget = TimerWidget(self)
        self.tabs.addTab(self.timer_widget, "🎣 Fishing Deck")
        
        # Tab 2: 🌊 My Pond (Placeholder for now)
        self.pond_placeholder = QWidget()
        pond_layout = QVBoxLayout()
        self.pond_placeholder.setLayout(pond_layout)
        pond_label = QLabel("Welcome to your virtual Pond! 🌊\nYour caught fih will swim here soon...")
        pond_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pond_label.setStyleSheet("font-size: 16px; color: #1F618D; font-family: 'Segoe UI', Arial; font-style: italic;")
        pond_layout.addWidget(pond_label)
        self.tabs.addTab(self.pond_placeholder, "🌊 My Pond")
        
        # Tab 3: 📊 Statistics (Placeholder for now)
        self.stats_placeholder = QWidget()
        stats_layout = QVBoxLayout()
        self.stats_placeholder.setLayout(stats_layout)
        stats_label = QLabel("Statistics Logs 📊\nYour Fih-tribution heatmap will be shown here soon...")
        stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        stats_label.setStyleSheet("font-size: 16px; color: #1F618D; font-family: 'Segoe UI', Arial; font-style: italic;")
        stats_layout.addWidget(stats_label)
        self.tabs.addTab(self.stats_placeholder, "📊 Stats")
        
        # Basic background styling for the window itself
        self.setStyleSheet("background-color: #D4E6F1;")
        
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


