import os
import json
from datetime import datetime

class FihDatabase:
    def __init__(self, filename="database.json"):
        # Resolve the absolute path of the root directory (one level up from src/)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.filename = os.path.join(base_dir, filename)
        
    def load_data(self) -> list:
        """
        Loads the history of caught fih from database.json.
        Returns a list of caught fih dictionaries.
        """
        if not os.path.exists(self.filename):
            return []
            
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            # Fallback if file is corrupted or unreadable
            return []

    def save_fih(self, emoji: str, name: str, is_special: bool, focus_start: str = None, focus_end: str = None) -> dict:
        """
        Appends a newly caught fih to the database.json file with timestamps.
        Returns the logged fih record dictionary.
        """
        history = self.load_data()
        
        # Build the logged item
        new_record = {
            "emoji": emoji,
            "name": name,
            "is_special": is_special,
            "focus_start": focus_start,
            "focus_end": focus_end,
            "focus_end_btn_pressed": datetime.now().isoformat()
        }
        
        history.append(new_record)
        
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Error saving to database: {e}")
            
        return new_record

    def get_total_count(self) -> int:
        """
        Returns the total number of fih caught so far.
        """
        return len(self.load_data())
