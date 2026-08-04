from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton
from PySide6.QtCore import Qt, QTimer

class TimerWidget(QWidget):
    def __init__(self, main_window=None):
        super().__init__()
        
        self.main_window = main_window  # Reference to Main Window for notifications
        
        # Timer variables
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.total_seconds_left = 0
        self.is_focus_mode = True  # True if Focus, False if Break
        
        # Main layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Cozy status label
        self.status_label = QLabel("Ready to fish... 🏕️")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("font-size: 14px; color: #566573; font-style: italic; font-family: 'Segoe UI', Arial;")
        layout.addWidget(self.status_label)
        
        # Big countdown label (shows minutes:seconds)
        self.timer_label = QLabel("15:00")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 64px; font-weight: bold; color: #1F618D; font-family: 'Segoe UI', Arial;")
        layout.addWidget(self.timer_label)
        
        # --- Settings Selectors (Focus & Break intervals) ---
        settings_layout = QHBoxLayout()
        
        # Focus time selector
        focus_layout = QVBoxLayout()
        focus_title = QLabel("Focus Time:")
        focus_title.setStyleSheet("font-size: 11px; color: #1F618D; font-weight: bold; text-transform: uppercase;")
        self.focus_combo = QComboBox()
        self.focus_combo.addItems(["1 Min", "15 Min", "20 Min", "25 Min", "30 Min"])
        self.focus_combo.setCurrentIndex(1)  # Default: 15 Min
        self.focus_combo.setStyleSheet("""
            QComboBox {
                padding: 6px; 
                border: 2px solid #2E86C1; 
                border-radius: 6px; 
                background-color: white; 
                color: black; 
                font-size: 13px; 
                font-weight: bold;
                min-width: 80px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: black;
                selection-background-color: #2E86C1;
                selection-color: white;
            }
        """)
        focus_layout.addWidget(focus_title)
        focus_layout.addWidget(self.focus_combo)
        settings_layout.addLayout(focus_layout)
        
        # Break time selector
        break_layout = QVBoxLayout()
        break_title = QLabel("Break Time:")
        break_title.setStyleSheet("font-size: 11px; color: #1F618D; font-weight: bold; text-transform: uppercase;")
        self.break_combo = QComboBox()
        # Generates options 1 Min, 3 Min, ..., 20 Min
        break_options = [f"{i} Min" for i in range(1, 21)]
        self.break_combo.addItems(break_options)
        self.break_combo.setCurrentIndex(3)  # Index 3 corresponds to "5 Min"
        self.break_combo.setStyleSheet("""
            QComboBox {
                padding: 6px; 
                border: 2px solid #2E86C1; 
                border-radius: 6px; 
                background-color: white; 
                color: black; 
                font-size: 13px; 
                font-weight: bold;
                min-width: 80px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: black;
                selection-background-color: #2E86C1;
                selection-color: white;
            }
        """)
        break_layout.addWidget(break_title)
        break_layout.addWidget(self.break_combo)
        settings_layout.addLayout(break_layout)
        
        layout.addLayout(settings_layout)
        layout.addSpacing(15)
        
        # --- Action Buttons ---
        buttons_layout = QHBoxLayout()
        
        # Cast Line (Start) Button
        self.start_btn = QPushButton("Cast Line 🎣")
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #2E86C1; color: white; border-radius: 8px; font-size: 14px; font-weight: bold; padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #1F618D;
            }
        """)
        buttons_layout.addWidget(self.start_btn)
        
        # Pull in Line (Transition to break/claim fih) Button
        self.pull_btn = QPushButton("Pull in Line! 🎣💦")
        self.pull_btn.setVisible(False)  # Hidden initially
        self.pull_btn.setStyleSheet("""
            QPushButton {
                background-color: #27AE60; color: white; border-radius: 8px; font-size: 14px; font-weight: bold; padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #1E8449;
            }
        """)
        buttons_layout.addWidget(self.pull_btn)
        
        # Pack up gear (Cancel/Reset) Button
        self.cancel_btn = QPushButton("Pack up gear 🎒")
        self.cancel_btn.setEnabled(False)  # Disabled initially
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #BDC3C7; color: #7F8C8D; border-radius: 8px; font-size: 14px; font-weight: bold; padding: 10px 20px;
            }
            QPushButton:hover:enabled {
                background-color: #95A5A6; color: white;
            }
        """)
        buttons_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(buttons_layout)
        
        # Connecting events
        self.focus_combo.currentIndexChanged.connect(self.update_timer_display_from_settings)
        self.start_btn.clicked.connect(self.start_timer)
        self.pull_btn.clicked.connect(self.claim_fih_and_start_break)
        self.cancel_btn.clicked.connect(self.reset_timer)
        
    def update_timer_display_from_settings(self):
        # Update the clock display text based on the selected focus time dropdown
        selected_text = self.focus_combo.currentText()
        minutes = selected_text.split(" ")[0]
        self.timer_label.setText(f"{minutes}:00")

    def start_timer(self):
        # Read focus minutes from settings and calculate total seconds
        focus_mins = int(self.focus_combo.currentText().split(" ")[0])
        self.total_seconds_left = focus_mins * 60
        self.is_focus_mode = True
        
        # Update UI states
        self.focus_combo.setEnabled(False)
        self.break_combo.setEnabled(False)
        self.start_btn.setEnabled(False)
        self.start_btn.setVisible(True)
        self.pull_btn.setVisible(False)
        self.cancel_btn.setEnabled(True)
        self.status_label.setText("Waiting patiently for a fih... 🤫")
        
        # Update clock display immediately and start QTimer
        self.update_clock_label()
        self.timer.start(1000)  # Fire tick() every 1000ms (1 second)

    def claim_fih_and_start_break(self):
        # Triggered when the user clicks 'Pull in Line! 🎣💦' after a bite
        self.pull_btn.setVisible(False)
        self.start_btn.setVisible(True)
        
        # Start break mode countdown
        self.start_break()

    def start_break(self):
        # Read break minutes from settings and calculate total seconds
        break_mins = int(self.break_combo.currentText().split(" ")[0])
        self.total_seconds_left = break_mins * 60
        self.is_focus_mode = False
        
        # Update UI state
        self.status_label.setText("Taking a sip of tea... 🍵")
        self.update_clock_label()
        self.timer.start(1000)

    def reset_timer(self):
        # Stop timer
        self.timer.stop()
        
        # Enable settings dropdowns and toggle buttons back to idle state
        self.focus_combo.setEnabled(True)
        self.break_combo.setEnabled(True)
        self.start_btn.setEnabled(True)
        self.start_btn.setVisible(True)
        self.pull_btn.setVisible(False)
        self.cancel_btn.setEnabled(False)
        self.status_label.setText("Ready to fish... 🏕️")
        
        # Reset visual clock representation
        self.update_timer_display_from_settings()

    def tick(self):
        if self.total_seconds_left > 0:
            self.total_seconds_left -= 1
            self.update_clock_label()
        else:
            self.timer.stop()
            self.on_timer_complete()

    def update_clock_label(self):
        mins = self.total_seconds_left // 60
        secs = self.total_seconds_left % 60
        self.timer_label.setText(f"{mins:02d}:{secs:02d}")

    def on_timer_complete(self):
        if self.is_focus_mode:
            # FOCUS TIMER FINISHED!
            # Trigger OS notification
            if self.main_window:
                self.main_window.show_notification(
                    "Fishodoro 🐟",
                    "A fih has bit the line! Focus completed. Click 'Pull in Line! 🎣💦' to start break!"
                )
            
            self.status_label.setText("A fih has bit the line! 🎣💦\n(Waiting for you to pull the line...)")
            
            # Switch buttons: hide normal Start button, show Pull in Line!
            self.start_btn.setVisible(False)
            self.pull_btn.setVisible(True)
            
            # (Here we will also generate the random fih in Step 4!)
        else:
            # BREAK TIMER FINISHED!
            # Trigger OS notification
            if self.main_window:
                self.main_window.show_notification(
                    "Fishodoro 🐟",
                    "Break is over! Time to start the next catch. 🏕️"
                )
            
            self.reset_timer()
            self.status_label.setText("Rested and ready for the next catch! 🏕️")

