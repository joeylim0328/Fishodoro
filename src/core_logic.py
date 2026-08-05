import random

# Common Fih (Standard Sea Life - caught on Focus sessions 1, 2, 3)
COMMON_FIH = [
    {"emoji": "🐟", "base_name": "Plain Old Blue"},
    {"emoji": "🐠", "base_name": "Goody Jane"},
    {"emoji": "🐡", "base_name": "Angy Porcupino"},
    {"emoji": "🦀", "base_name": "Small Kiap Kiap"},
    {"emoji": "🦐", "base_name": "Grandpa Shrimp"},
    {"emoji": "🐙", "base_name": "Takoyaki"},
    {"emoji": "🦞", "base_name": "Big Kiap Kiap"},
    {"emoji": "🐚", "base_name": "Jolly Shelly"},
    
]

# Special Fih (Rare/Legendary Sea Life - caught on every 4th focus completion)
SPECIAL_FIH = [
    {"emoji": "🦑", "base_name": "Le Kraken"},
    {"emoji": "🐋", "base_name": "Majestic Willy"},
    {"emoji": "🐬", "base_name": "Elegant Daphne"},
    {"emoji": "🦈", "base_name": "Mr Vegan Sunshine"},
    {"emoji": "🐳", "base_name": "Aqua Willy"},
    {"emoji": "🧜‍♂️", "base_name": "King Poseidon"},
    {"emoji": "🧜‍♀️", "base_name": "Queen Amphitrite"},
    {"emoji": "🦕", "base_name": "Loch Ness Monster"},
]

def generate_random_fih(total_caught_count: int) -> dict:
    """
    Generates a random fih based on the 4th fih rule.
    Returns a dictionary with 'emoji', 'name', and 'is_special'.
    """
    # Rule: Every 4th fih has a small chance to reward a rare special fih!
    current_fih_number = total_caught_count + 1
    is_special = (current_fih_number % 4 == 0 and random.random() < 0.15)
    
    if is_special:
        fih_template = random.choice(SPECIAL_FIH)
    else:
        fih_template = random.choice(COMMON_FIH)
        
    return {
        "emoji": fih_template["emoji"],
        "name": fih_template["base_name"],
        "is_special": is_special
    }
