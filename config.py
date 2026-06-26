import os
import json

SETTINGS_FILE = "settings.json"
LEGACY_THEME_FILE = "theme.txt"

# Default state
CURRENT_THEME = "Naruto"
COINS = 500
UNLOCKED_THEMES = ["Arsene_Lupin", "Astro_Boy"]

def _load_settings():
    global CURRENT_THEME, COINS, UNLOCKED_THEMES
    
    # Migrate legacy theme.txt if it exists and settings.json doesn't
    if os.path.exists(LEGACY_THEME_FILE) and not os.path.exists(SETTINGS_FILE):
        with open(LEGACY_THEME_FILE, "r") as f:
            t = f.read().strip()
            if t: CURRENT_THEME = t
        save_state()
        try:
            os.remove(LEGACY_THEME_FILE)
        except:
            pass
        return

    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                data = json.load(f)
                CURRENT_THEME = data.get("theme", CURRENT_THEME)
                COINS = data.get("coins", COINS)
                
                # Ensure the default free themes are always unlocked
                saved_unlocked = data.get("unlocked_themes", UNLOCKED_THEMES)
                for default_theme in ["Arsene_Lupin", "Astro_Boy"]:
                    if default_theme not in saved_unlocked:
                        saved_unlocked.append(default_theme)
                        
                # Ensure the current theme is always considered unlocked
                if CURRENT_THEME not in saved_unlocked:
                    saved_unlocked.append(CURRENT_THEME)
                    
                UNLOCKED_THEMES = saved_unlocked
        except:
            pass

def save_state():
    data = {
        "theme": CURRENT_THEME,
        "coins": COINS,
        "unlocked_themes": UNLOCKED_THEMES
    }
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def save_theme(theme_name):
    global CURRENT_THEME
    CURRENT_THEME = theme_name
    save_state()

def unlock_theme(theme_name, cost=100):
    global COINS, UNLOCKED_THEMES
    if theme_name not in UNLOCKED_THEMES and COINS >= cost:
        COINS -= cost
        UNLOCKED_THEMES.append(theme_name)
        save_state()
        return True
    return False

# Initialize
_load_settings()