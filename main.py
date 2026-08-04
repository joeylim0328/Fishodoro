import sys
import os
import logging
from PySide6.QtWidgets import QApplication
from src.ui.main_window import FishodoroApp

# Configure logging
base_dir = os.path.dirname(os.path.abspath(__file__))
log_file = os.path.join(base_dir, "fishodoro.log")

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.FileHandler(log_file, encoding="utf-8"),
        logging.StreamHandler(sys.stdout)  # Keep printing to terminal too
    ]
)

logger = logging.getLogger("main")
logger.info("Fishodoro Application Starting Up...")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FishodoroApp()
    window.show()
    sys.exit(app.exec())

