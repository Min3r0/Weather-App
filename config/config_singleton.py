"""Singleton pour la configuration de l'application."""
import json
import os
from typing import Dict, List, Any, Optional


class ConfigSingleton:
    """Singleton pour gérer la configuration de l'application."""

    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not ConfigSingleton._initialized:
            self._config: Dict[str, Any] = {}
            self._config_file = "config.json"
            self.load_config()
            ConfigSingleton._initialized = True

    def load_config(self):
        """Charge la configuration depuis le fichier."""
        if os.path.exists(self._config_file):
            with open(self._config_file, 'r', encoding='utf-8') as f:
                self._config = json.load(f)
        else:
            # Configuration par défaut
            self._config = {
                "countries": {
                    "France": {
                        "Toulouse": {
                            "stations": [
                                {
                                    "name": "Toulouse - Montaudran",
                                    "url": "https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets/12-station-meteo-toulouse-montaudran/records?select=heure_de_paris%2C%20humidite%2C%20temperature_en_degre_c%2C%20pression&order_by=heure_de_paris%20DESC&limit=100"
                                },
                                {
                                    "name": "Toulouse - Compans-Caffarelli",
                                    "url": "https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets/stations-meteo-en-temps-reel-compans-caffarelli/records?select=heure_de_paris%2C%20humidite%2C%20temperature_en_degre_c%2C%20pression&order_by=heure_de_paris%20DESC&limit=100"
                                }
                            ]
                        }
                    }
                }
            }
            self.save_config()

    def save_config(self):
        """Sauvegarde la configuration dans le fichier."""
        with open(self._config_file, 'w', encoding='utf-8') as f:
            json.dump(self._config, f, indent=2, ensure_ascii=False)

    def get_all_stations(self) -> List[Dict[str, str]]:
        """Retourne toutes les stations disponibles."""
        stations = []
        for country, cities in self._config.get("countries", {}).items():
            for city, data in cities.items():
                for station in data.get("stations", []):
                    stations.append({
                        "name": station["name"],
                        "url": station["url"],
                        "city": city,
                        "country": country
                    })
        return stations

    def add_station(self, country: str, city: str, name: str, url: str):
        """Ajoute une nouvelle station à la configuration."""
        if country not in self._config["countries"]:
            self._config["countries"][country] = {}
        if city not in self._config["countries"][country]:
            self._config["countries"][country][city] = {"stations": []}

        self._config["countries"][country][city]["stations"].append({
            "name": name,
            "url": url
        })
        self.save_config()

    def update_station_url(self, station_name: str, new_url: str) -> bool:
        """Met à jour l'URL d'une station."""
        for country, cities in self._config.get("countries", {}).items():
            for city, data in cities.items():
                for station in data.get("stations", []):
                    if station["name"] == station_name:
                        station["url"] = new_url
                        self.save_config()
                        return True
        return False