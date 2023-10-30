import json
import os, sys
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class SettingsManager:
    def __init__(self):
        with open(resource_path("settings.json"), "r") as file:
            self.settings = json.load(file)

    def get_value(self, key):
        return self.settings.get(key, None)

    def set_value(self, key, value):
        self.settings[key] = value
        with open(resource_path("settings.json"), 'w') as file:
            file.write(json.dumps(self.settings, indent=2))
