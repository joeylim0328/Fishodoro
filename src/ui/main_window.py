from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QSystemTrayIcon, QMenu, QTabWidget, QLabel
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import QCoreApplication, Qt
from src.ui.widgets.timer_widget import TimerWidget
from src.ui.widgets.pond_widget import PondWidget
from src.ui.widgets.stats_widget import StatsWidget

class FishodoroApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configure the window
        self.setWindowTitle("Fishodoro 🐟")
        self.resize(550, 600)  # Sized beautifully for our content panels
        
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
        
        # Tab 2: 🌊 My Pond (Using our new PondWidget)
        self.pond_widget = PondWidget()
        self.tabs.addTab(self.pond_widget, "🌊 My Pond")
        
        # Tab 3: 📊 Statistics (Using our new StatsWidget)
        self.stats_widget = StatsWidget()
        self.tabs.addTab(self.stats_widget, "📊 Stats")
        
        # Basic background styling for the window itself
        self.setStyleSheet("""
            background-color: #D4E6F1;
        """)
        
        # Style QToolTip globally for clear black text and beautiful light cozy background
        QCoreApplication.instance().setStyleSheet("""
            QToolTip {
                background-color: #F8F9F9;
                color: #2C3E50;
                font-family: 'Segoe UI', Arial;
                font-size: 12px;
                border: 1px solid #2E86C1;
                border-radius: 4px;
                padding: 5px;
            }
        """)
        
        # Connect tab changes so that selecting the Stats tab automatically refreshes it
        self.tabs.currentChanged.connect(self.on_tab_changed)
        
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

    def on_tab_changed(self, index):
        # If the user clicks on the Pond tab (index 1), automatically refresh it
        if index == 1:
            self.pond_widget.refresh_pond()
        # If the user clicks on the Stats tab (index 2), automatically refresh it
        elif index == 2:
            self.stats_widget.refresh_stats()



