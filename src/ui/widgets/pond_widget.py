import random
import logging
import math
from datetime import datetime, date, timedelta
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGraphicsView, 
                               QGraphicsScene, QGraphicsTextItem, QLabel, QPushButton)
from PySide6.QtCore import Qt, QTimer, QRectF
from PySide6.QtGui import QBrush, QLinearGradient, QColor, QFont, QPainter, QTransform
from src.database import FihDatabase

logger = logging.getLogger("PondWidget")

class SwimmingFihItem(QGraphicsTextItem):
    """
    Representing a single swimming fih emoji on our 2D canvas with individual velocity and direction.
    """
    def __init__(self, emoji: str, name: str, is_special: bool, catch_time_str: str, bounds: QRectF):
        super().__init__(emoji)
        self.name = name
        self.is_special = is_special
        self.bounds = bounds
        
        # Configure look
        font_size = 28 if is_special else 22
        self.setFont(QFont("Segoe UI Emoji", font_size))
        
        # Set transformation origin to center of bounding rect for smooth rotation & flipping
        self.setTransformOriginPoint(self.boundingRect().width() / 2, self.boundingRect().height() / 2)
        
        # Format hover tooltip
        self.setToolTip(f"🐠 {name}\nCaught at: {catch_time_str}")
        
        # Random initial velocities
        self.vx = random.uniform(-0.8, 0.8)
        self.vy = random.uniform(-0.3, 0.3)
        
        # Ensure velocities aren't zero
        if abs(self.vx) < 0.2:
            self.vx = 0.4 if random.choice([True, False]) else -0.4
        if abs(self.vy) < 0.1:
            self.vy = 0.2 if random.choice([True, False]) else -0.2

        # Gentle bobbing factors
        self.bob_frequency = random.uniform(0.04, 0.08)
        self.bob_amplitude = random.uniform(0.15, 0.3)
        self.time_counter = random.randint(0, 100)
        
        # Dynamic direction change variables (cruising)
        self.change_dir_counter = random.randint(50, 150)

    def update_position(self):
        """Update fih coordinates with steering vectors, natural drift, and direction flips."""
        self.time_counter += 1
        self.change_dir_counter -= 1
        
        # 1. Smooth cruising / direction changes
        if self.change_dir_counter <= 0:
            # Shift velocities slightly to curve their pathways naturally
            self.vx += random.uniform(-0.15, 0.15)
            self.vy += random.uniform(-0.08, 0.08)
            
            # Clamp speeds so they don't sprint or fall asleep
            max_vx = 1.0 if not self.is_special else 0.8
            max_vy = 0.4
            self.vx = max(-max_vx, min(self.vx, max_vx))
            self.vy = max(-max_vy, min(self.vy, max_vy))
            
            # Reset countdown for next steer
            self.change_dir_counter = random.randint(60, 180)
            
        # 2. Physics calculation with trigonometric bobbing
        curr_pos = self.pos()
        bobbing = self.bob_amplitude * math.sin(self.time_counter * self.bob_frequency)
        
        new_x = curr_pos.x() + self.vx
        new_y = curr_pos.y() + self.vy + bobbing
        
        # Scene Boundary Collisions
        item_width = self.boundingRect().width()
        item_height = self.boundingRect().height()
        
        # Bounce off Left/Right edges
        if new_x < self.bounds.left():
            new_x = self.bounds.left()
            self.vx = -self.vx
            self.change_dir_counter = random.randint(20, 60)  # Reset steering delay on bounce
        elif new_x + item_width > self.bounds.right():
            new_x = self.bounds.right() - item_width
            self.vx = -self.vx
            self.change_dir_counter = random.randint(20, 60)
            
        # Bounce off Top/Bottom edges
        if new_y < self.bounds.top():
            new_y = self.bounds.top()
            self.vy = -self.vy
        elif new_y + item_height > self.bounds.bottom():
            new_y = self.bounds.bottom() - item_height
            self.vy = -self.vy
            
        # 3. Apply facing direction (Horizontal Flip) & Rotation (Swaying angle)
        transform = QTransform()
        
        # Flip emoji if swimming to the right (most fish emojis point left by default)
        if self.vx > 0:
            # Scale X by -1 from the origin to flip horizontally
            transform.scale(-1, 1)
            
        # Gentle rotation angle based on vertical movement direction
        # Angle is calculated from velocity arctangent to point head-first
        angle_rad = math.atan2(self.vy + bobbing, abs(self.vx))
        angle_deg = math.degrees(angle_rad)
        
        # Restrict tilting angle slightly (up to 15 degrees) so they don't spin upside down
        clamped_angle = max(-15, min(angle_deg, 15))
        
        # Apply transformation matrices
        self.setTransform(transform)
        self.setRotation(clamped_angle)
        
        # Apply updated position
        self.setPos(new_x, new_y)


class PondWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.db = FihDatabase()
        
        # Default display date (today)
        self.selected_date = date.today()
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(main_layout)
        
        # --- DATE FILTER NAVIGATION BAR ---
        nav_layout = QHBoxLayout()
        nav_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Previous Day Button
        self.prev_btn = QPushButton("◀")
        self.prev_btn.setFixedSize(30, 26)
        self.prev_btn.setStyleSheet("""
            QPushButton {
                background-color: #2E86C1; color: white; border-radius: 4px; font-weight: bold; font-size: 12px;
            }
            QPushButton:hover { background-color: #1F618D; }
        """)
        self.prev_btn.clicked.connect(self.show_prev_day)
        nav_layout.addWidget(self.prev_btn)
        
        # Date Label
        self.date_label = QLabel("")
        self.date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.date_label.setFixedWidth(200)
        self.date_label.setStyleSheet("font-size: 15px; font-weight: bold; color: #1F618D; font-family: 'Segoe UI', Arial;")
        nav_layout.addWidget(self.date_label)
        
        # Next Day Button
        self.next_btn = QPushButton("▶")
        self.next_btn.setFixedSize(30, 26)
        self.next_btn.setStyleSheet("""
            QPushButton {
                background-color: #2E86C1; color: white; border-radius: 4px; font-weight: bold; font-size: 12px;
            }
            QPushButton:hover { background-color: #1F618D; }
        """)
        self.next_btn.clicked.connect(self.show_next_day)
        nav_layout.addWidget(self.next_btn)
        
        main_layout.addLayout(nav_layout)
        main_layout.addSpacing(5)
        
        # Info Label
        self.info_label = QLabel("No fih caught yet on this day.")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setStyleSheet("font-size: 12px; color: #566573; font-style: italic; font-family: 'Segoe UI', Arial;")
        main_layout.addWidget(self.info_label)
        main_layout.addSpacing(5)
        
        # --- THE POND GRAPHICS CANVAS ---
        self.scene = QGraphicsScene()
        # Set absolute boundaries for coordinate space
        self.scene.setSceneRect(0, 0, 480, 280)
        
        # Styling the Scene background with a gorgeous underwater linear gradient
        gradient = QLinearGradient(0, 0, 0, 280)
        gradient.setColorAt(0.0, QColor("#1A5276")) # Calming Teal
        gradient.setColorAt(0.5, QColor("#1F618D")) # Warm Blue
        gradient.setColorAt(1.0, QColor("#113F58")) # Deep Ocean Teal
        self.scene.setBackgroundBrush(QBrush(gradient))
        
        # Visual View container
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.view.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        self.view.setFixedSize(484, 284)
        self.view.setStyleSheet("border: 2px solid #2E86C1; border-radius: 8px; background: transparent;")
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        main_layout.addWidget(self.view, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # --- ANIMATION TIMER ---
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.animate_pond)
        self.animation_timer.start(33) # Smooth ~30 FPS framerate
        
        self.swimming_fih_list = []
        
        # Initial render of today's pond
        self.refresh_pond()

    def show_prev_day(self):
        """Scrolls date filter back by 1 day."""
        self.selected_date -= timedelta(days=1)
        self.refresh_pond()

    def show_next_day(self):
        """Scrolls date filter forward by 1 day."""
        self.selected_date += timedelta(days=1)
        self.refresh_pond()

    def refresh_pond(self):
        """Loads fih caught on the selected date and spawns them into the virtual aquarium."""
        logger.info(f"Refreshing Pond for date: {self.selected_date}")
        
        # 1. Update Navigation Header Labels
        is_today = (self.selected_date == date.today())
        date_display_text = "Today (🌊 My Pond)" if is_today else self.selected_date.strftime("%A, %b %d, %Y")
        self.date_label.setText(date_display_text)
        
        # 2. Clear previous items from the graphics scene
        self.scene.clear()
        self.swimming_fih_list.clear()
        
        # 3. Retrieve fih caught on the selected date from database
        history = self.db.load_data()
        daily_catches = []
        
        for item in history:
            if "focus_end_btn_pressed" in item:
                try:
                    record_date_str = item["focus_end_btn_pressed"].split("T")[0]
                    record_date = datetime.strptime(record_date_str, "%Y-%m-%d").date()
                    if record_date == self.selected_date:
                        daily_catches.append(item)
                except Exception as e:
                    logger.error(f"Error parsing date in pond: {e}")
                    
        # Update Info Label with count
        count = len(daily_catches)
        if count == 0:
            self.info_label.setText("No fih reeled in on this day... Settle down and cast a line! 🏕️")
        else:
            self.info_label.setText(f"Swimming peacefully: {count} fih reeled in on this day! 🐟🫧")
            
        # 4. Spawn fih emojis as swimming graphic items
        scene_bounds = self.scene.sceneRect()
        # Restrict spawn coordinates slightly inward so fih don't get stuck instantly inside edges
        spawn_area = QRectF(20, 20, scene_bounds.width() - 50, scene_bounds.height() - 50)
        
        for item in daily_catches:
            # Parse localized catch time text
            catch_time_text = "Unknown time"
            if "focus_end_btn_pressed" in item:
                try:
                    dt = datetime.fromisoformat(item["focus_end_btn_pressed"])
                    catch_time_text = dt.strftime("%I:%M %p")
                except ValueError:
                    catch_time_text = item["focus_end_btn_pressed"]
            
            # Create graphic swimming item
            fih_item = SwimmingFihItem(
                emoji=item["emoji"],
                name=item["name"],
                is_special=item.get("is_special", False),
                catch_time_str=catch_time_text,
                bounds=scene_bounds
            )
            
            # Position randomly in spawn area
            start_x = random.uniform(spawn_area.left(), spawn_area.right())
            start_y = random.uniform(spawn_area.top(), spawn_area.bottom())
            fih_item.setPos(start_x, start_y)
            
            # Add to canvas and internal tracking list
            self.scene.addItem(fih_item)
            self.swimming_fih_list.append(fih_item)

    def animate_pond(self):
        """Ticks the swimming coordinate frame for all active items on the canvas."""
        for fih in self.swimming_fih_list:
            fih.update_position()
