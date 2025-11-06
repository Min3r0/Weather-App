# app/config_manager.py
import json
import os

DEFAULT_CONFIG = {
    "default_country": "France",
    "default_city": "Toulouse",
    "stations_file": "data/stations.json",
    "config_file": "data/config.json"
}

class ConfigManager:
    def __init__(self, config_path: str = "data/config.json"):
        self.config_path = config_path
        self.config = DEFAULT_CONFIG.copy()
        self._ensure_data_folder()
        self.load_config()

    def _ensure_data_folder(self):
        folder = os.path.dirname(self.config_path)
        if folder and not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.config.update(data)
            except Exception as e:
                print(f"Warning: failed to load config: {e}. Using defaults.")
        else:
            self.save_config()  # create default config file

    def save_config(self):
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error saving config: {e}")

    def get_default_city(self) -> str:
        return self.config.get("default_city", DEFAULT_CONFIG["default_city"])

    def set_default_city(self, city: str):
        self.config["default_city"] = city
        self.save_config()
