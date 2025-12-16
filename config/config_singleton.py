import json
import os
from typing import Dict, Optional


class ConfigSingleton:
    """Singleton pour stocker la configuration globale"""
    _instance = None
    _config_file = "config.json"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._data = {
            "pays": {},
            "default_api_base": "https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets/"
        }
        self.load_config()

    def load_config(self):
        """Charge la configuration depuis le fichier"""
        if os.path.exists(self._config_file):
            try:
                with open(self._config_file, 'r', encoding='utf-8') as f:
                    self._data = json.load(f)
            except Exception as e:
                print(f"Erreur lors du chargement de la config: {e}")
                self._init_default_config()
        else:
            self._init_default_config()

    def _init_default_config(self):
        """Initialise une configuration par défaut"""
        self._data = {
            "pays": {
                "France": {
                    "villes": {
                        "Toulouse": {
                            "stations": {
                                "Compans-Caffarelli": {
                                    "url": "https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets/toulouse-metropole-station-meteo-compans-caffarelli/records?select=date_de_mesure%2C%20humidite%2C%20temperature_en_degre_c%2C%20pression&order_by=date_de_mesure%20DESC&limit=100"
                                },
                                "Université Paul Sabatier": {
                                    "url": "https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets/12-station-meteo-toulouse-montaudran/records?select=heure_de_paris%2C%20humidite%2C%20temperature_en_degre_c%2C%20pression&order_by=heure_de_paris%20DESC&limit=100"
                                }
                            }
                        }
                    }
                }
            },
            "default_api_base": "https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets/"
        }
        self.save_config()

    def save_config(self):
        """Sauvegarde la configuration dans le fichier"""
        try:
            with open(self._config_file, 'w', encoding='utf-8') as f:
                json.dump(self._data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de la config: {e}")

    def get_pays(self) -> Dict:
        """Retourne tous les pays"""
        return self._data.get("pays", {})

    def add_pays(self, nom: str):
        """Ajoute un nouveau pays"""
        if nom not in self._data["pays"]:
            self._data["pays"][nom] = {"villes": {}}
            self.save_config()
            return True
        return False

    def remove_pays(self, nom: str):
        """Supprime un pays"""
        if nom in self._data["pays"]:
            del self._data["pays"][nom]
            self.save_config()
            return True
        return False

    def add_ville(self, pays: str, ville: str):
        """Ajoute une ville à un pays"""
        if pays in self._data["pays"]:
            if ville not in self._data["pays"][pays]["villes"]:
                self._data["pays"][pays]["villes"][ville] = {"stations": {}}
                self.save_config()
                return True
        return False

    def remove_ville(self, pays: str, ville: str):
        """Supprime une ville"""
        if pays in self._data["pays"] and ville in self._data["pays"][pays]["villes"]:
            del self._data["pays"][pays]["villes"][ville]
            self.save_config()
            return True
        return False

    def add_station(self, pays: str, ville: str, station: str, url: str):
        """Ajoute une station à une ville"""
        if pays in self._data["pays"] and ville in self._data["pays"][pays]["villes"]:
            self._data["pays"][pays]["villes"][ville]["stations"][station] = {"url": url}
            self.save_config()
            return True
        return False

    def remove_station(self, pays: str, ville: str, station: str):
        """Supprime une station"""
        if (pays in self._data["pays"] and
                ville in self._data["pays"][pays]["villes"] and
                station in self._data["pays"][pays]["villes"][ville]["stations"]):
            del self._data["pays"][pays]["villes"][ville]["stations"][station]
            self.save_config()
            return True
        return False

    def get_station_url(self, pays: str, ville: str, station: str) -> Optional[str]:
        """Récupère l'URL d'une station"""
        try:
            return self._data["pays"][pays]["villes"][ville]["stations"][station]["url"]
        except KeyError:
            return None

    def update_station_url(self, pays: str, ville: str, station: str, url: str):
        """Met à jour l'URL d'une station"""
        if (pays in self._data["pays"] and
                ville in self._data["pays"][pays]["villes"] and
                station in self._data["pays"][pays]["villes"][ville]["stations"]):
            self._data["pays"][pays]["villes"][ville]["stations"][station]["url"] = url
            self.save_config()
            return True
        return False
