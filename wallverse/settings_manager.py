import json
import os
import platform
import sys
from importlib.resources import files


def resource_path(file_name):
    return files('wallverse').joinpath(file_name)


class SettingsManager:
    def __init__(self):
        with open(resource_path("settings.json"), "r") as file:
            self.settings = json.load(file)
            if platform.system() == "Darwin" or platform.system() == "Linux":
                self.fix_paths()

    def get_value(self, key):
        return self.settings.get(key, None)

    def set_value(self, key, value):
        self.settings[key] = value
        with open(resource_path("settings.json"), 'w') as file:
            file.write(json.dumps(self.settings, indent=2))

    def fix_paths(self):
        paths = ["font_path", "light_mode_image_path", "dark_mode_image_path"]
        for path in paths:
            self.set_value(path, self.get_value(path).replace("\\", "/"))
