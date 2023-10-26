import json


class SettingsManager:
    def __init__(self):
        with open("settings.json", "r") as file:
            self.settings = json.load(file)

    def get_value(self, key):
        return self.settings.get(key, None)

    def set_value(self, key, value):
        self.settings[key] = value
        with open("settings.json", 'w') as file:
            file.write(json.dumps(self.settings, indent=2))
