from datetime import datetime, timedelta
import calendar
import logging
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QScrollArea, QFrame, QPushButton
from PySide6.QtCore import Qt
from src.database import FihDatabase

logger = logging.getLogger("StatsWidget")

class StatsWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.db = FihDatabase()
        
        # Keep track of which month/year the calendar is currently displaying (defaults to current date)
        self.current_display_date = datetime.now()
        
        # Main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # Title/Overview label
        self.overview_label = QLabel("Loading your fishing logs... 🎣")
        self.overview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.overview_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #1F618D; font-family: 'Segoe UI', Arial;")
        main_layout.addWidget(self.overview_label)
        main_layout.addSpacing(10)
        
        # --- MONTH NAVIGATION HEADER ---
        nav_layout = QHBoxLayout()
        nav_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.prev_btn = QPushButton("◀")
        self.prev_btn.setFixedSize(30, 26)
        self.prev_btn.setStyleSheet("""
            QPushButton {
                background-color: #2E86C1; color: white; border-radius: 4px; font-weight: bold; font-size: 12px;
            }
            QPushButton:hover { background-color: #1F618D; }
        """)
        self.prev_btn.clicked.connect(self.show_prev_month)
        nav_layout.addWidget(self.prev_btn)
        
        self.month_year_label = QLabel("August 2026")
        self.month_year_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.month_year_label.setFixedWidth(160)
        self.month_year_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #1F618D; font-family: 'Segoe UI', Arial;")
        nav_layout.addWidget(self.month_year_label)
        
        self.next_btn = QPushButton("▶")
        self.next_btn.setFixedSize(30, 26)
        self.next_btn.setStyleSheet("""
            QPushButton {
                background-color: #2E86C1; color: white; border-radius: 4px; font-weight: bold; font-size: 12px;
            }
            QPushButton:hover { background-color: #1F618D; }
        """)
        self.next_btn.clicked.connect(self.show_next_month)
        nav_layout.addWidget(self.next_btn)
        
        main_layout.addLayout(nav_layout)
        main_layout.addSpacing(5)
        
        # --- CALENDAR GRID CONTAINER ---
        self.heatmap_frame = QFrame()
        self.heatmap_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px solid #AED6F1;
                border-radius: 8px;
            }
        """)
        heatmap_outer_layout = QVBoxLayout(self.heatmap_frame)
        heatmap_outer_layout.setContentsMargins(15, 10, 15, 15)
        
        # Grid layout for calendar
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(6)
        heatmap_outer_layout.addLayout(self.grid_layout)
        
        main_layout.addWidget(self.heatmap_frame)
        main_layout.addSpacing(15)
        
        # --- HISTORY LOGS LIST ---
        history_title = QLabel("Recent Catches Logbook 📖")
        history_title.setStyleSheet("font-size: 12px; font-weight: bold; color: #1F618D; text-transform: uppercase;")
        main_layout.addWidget(history_title)
        
        # Scrollable area for history lines
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: 1px solid #BDC3C7;
                border-radius: 6px;
                background-color: #F8F9F9;
            }
        """)
        
        self.history_content = QWidget()
        self.history_layout = QVBoxLayout(self.history_content)
        self.history_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll.setWidget(self.history_content)
        
        main_layout.addWidget(scroll)
        
        # Initial render/load of stats
        self.refresh_stats()

    def show_prev_month(self):
        """Scrolls calendar to the previous month."""
        # Subtract one month
        first_of_current = self.current_display_date.replace(day=1)
        self.current_display_date = first_of_current - timedelta(days=1)
        self.refresh_stats()

    def show_next_month(self):
        """Scrolls calendar to the next month."""
        # Add 32 days from the 1st of current month to ensure we enter the next month, then reset day to 1st
        first_of_current = self.current_display_date.replace(day=1)
        next_month_approx = first_of_current + timedelta(days=32)
        self.current_display_date = next_month_approx.replace(day=1)
        self.refresh_stats()

    def refresh_stats(self):
        """Loads data from the database and redraws both the heatmap and history logs."""
        logger.info("Refreshing StatsWidget...")
        history = self.db.load_data()
        
        # 1. Update Overview Label
        total_caught = len(history)
        unique_species = len(set(item["name"] for item in history))
        self.overview_label.setText(
            f"You have caught a total of {total_caught} fih! 🎣\n"
            f"Discovered {unique_species} unique species in your logbook."
        )
        
        # Update Month/Year Header text
        self.month_year_label.setText(self.current_display_date.strftime("%B %Y"))
        
        # 2. Populate History Logs list
        # Clear existing logs in the list
        while self.history_layout.count():
            child = self.history_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
        if not history:
            no_fih_label = QLabel("Your logbook is empty. Cast some lines to catch your first fih! 🏕️")
            no_fih_label.setStyleSheet("color: #7F8C8D; font-style: italic; padding: 10px;")
            self.history_layout.addWidget(no_fih_label)
        else:
            # Show in reverse order (most recent first)
            for item in reversed(history):
                time_str = "Unknown"
                if "focus_end_btn_pressed" in item:
                    try:
                        dt = datetime.fromisoformat(item["focus_end_btn_pressed"])
                        time_str = dt.strftime("%b %d, %Y at %I:%M %p")
                    except ValueError:
                        time_str = item["focus_end_btn_pressed"]
                
                log_text = f"{item['emoji']} {item['name']} - reeled in on {time_str}"
                log_label = QLabel(log_text)
                log_label.setStyleSheet("""
                    QLabel {
                        font-size: 12px;
                        color: #2C3E50;
                        padding: 6px;
                        border-bottom: 1px solid #E5E7E9;
                        font-family: 'Segoe UI', Arial;
                    }
                """)
                self.history_layout.addWidget(log_label)
                
        # 3. Render the Monthly Calendar Heatmap
        self.render_monthly_calendar(history)

    def render_monthly_calendar(self, history):
        """Draws a beautiful standard monthly calendar grid, colored based on daily fish counts."""
        # Clear existing widgets in grid layout
        while self.grid_layout.count():
            child = self.grid_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
        # Group fih caught on each date ("YYYY-MM-DD")
        daily_catches = {}
        for item in history:
            if "focus_end_btn_pressed" in item:
                try:
                    date_str = item["focus_end_btn_pressed"].split("T")[0]
                    if date_str not in daily_catches:
                        daily_catches[date_str] = []
                    daily_catches[date_str].append(item)
                except Exception:
                    continue
                    
        # Add Day-of-Week headers (Sun, Mon, Tue, Wed, Thu, Fri, Sat)
        day_headers = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        for col, day_name in enumerate(day_headers):
            lbl = QLabel(day_name)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("font-size: 11px; font-weight: bold; color: #1F618D; font-family: 'Segoe UI', Arial; padding-bottom: 5px;")
            self.grid_layout.addWidget(lbl, 0, col)
            
        # Determine the calendar structure for self.current_display_date
        year = self.current_display_date.year
        month = self.current_display_date.month
        
        # calendar.monthcalendar returns a list of weeks of days. Days outside the month are represented as 0.
        # It defaults to Monday=0. We can configure calendar to start weeks on Sunday.
        cal = calendar.Calendar(firstweekday=6)  # 6 corresponds to Sunday
        month_weeks = cal.monthdayscalendar(year, month)
        
        # Draw the squares for each cell in each week
        for row_idx, week in enumerate(month_weeks):
            for col_idx, day_num in enumerate(week):
                # Row index shifts down by 1 because Row 0 is our Day Headers (Sun-Sat)
                grid_row = row_idx + 1
                
                # If day_num is 0, it belongs to the adjacent month. We draw an empty, semi-transparent square
                if day_num == 0:
                    empty_cell = QLabel()
                    empty_cell.setFixedSize(36, 36)
                    empty_cell.setStyleSheet("background-color: #F2F4F4; border-radius: 6px; border: 1px dashed #E5E7E9;")
                    self.grid_layout.addWidget(empty_cell, grid_row, col_idx)
                    continue
                
                # Build exact ISO date string for this cell
                cell_date = datetime(year, month, day_num)
                date_str = cell_date.strftime("%Y-%m-%d")
                
                # Get the caught fish on this day
                catches = daily_catches.get(date_str, [])
                count = len(catches)
                
                # Determine background color based on count
                if count == 0:
                    bg_color = "#EBEDF0"      # Light neutral gray-blue
                    text_color = "#7F8C8D"    # Gray text
                elif count <= 2:
                    bg_color = "#A9CCE3"      # Soft sky blue
                    text_color = "#1B4F72"    # Dark contrast text
                elif count <= 4:
                    bg_color = "#5499C7"      # Wave blue
                    text_color = "white"
                elif count <= 6:
                    bg_color = "#2471A3"      # Deep lake blue
                    text_color = "white"
                else:
                    bg_color = "#1B4F72"      # Deep ocean blue
                    text_color = "white"
                    
                # Highlight today's calendar square with a golden/yellow border!
                is_today = (cell_date.date() == datetime.now().date())
                border_style = "border: 2px solid #F39C12;" if is_today else "border: 1px solid #D5F5E3;" if count > 0 else "border: none;"
                
                # Build custom hover tooltip showing exactly what fish were caught!
                if count == 0:
                    tooltip_text = f"{cell_date.strftime('%B %d, %Y')}\nNo fih caught yet. 🏕️"
                else:
                    fish_list = "\n".join([f"• {f['emoji']} {f['name']}" for f in catches])
                    tooltip_text = f"{cell_date.strftime('%B %d, %Y')}\nCaught {count} fih:\n{fish_list}"
                
                # Create a beautiful, labeled calendar cell
                cell = QLabel(str(day_num))
                cell.setFixedSize(36, 36)
                cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
                cell.setToolTip(tooltip_text)
                
                cell_font_weight = "bold" if (count > 0 or is_today) else "normal"
                
                cell.setStyleSheet(f"""
                    QLabel {{
                        background-color: {bg_color};
                        color: {text_color};
                        font-family: 'Segoe UI', Arial;
                        font-weight: {cell_font_weight};
                        font-size: 13px;
                        border-radius: 6px;
                        {border_style}
                    }}
                    QLabel:hover {{
                        color: black;
                        background-color: #F8F9F9; /* Cozy hover background light-tint */
                        border: 2px solid #3498DB;
                    }}
                """)
                
                self.grid_layout.addWidget(cell, grid_row, col_idx)
