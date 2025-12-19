"""
Pattern Singleton pour la configuration de l'application.
"""
import json
import os
from typing import Dict, List, Optional, Any


class ConfigurationSingleton:
    """
    Singleton pour gérer la configuration de l'application.
    Principe SOLID: Single Responsibility - gère uniquement la configuration.
    """
    _instance: Optional['ConfigurationSingleton'] = None
    _initialized: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._config: Dict = {
                "pays": {},
                "villes": {},
                "stations": {}
            }
            self._config_file = "config.json"
            self._load_configuration()
            ConfigurationSingleton._initialized = True

    def _initialize(self) -> None:
        # Initialisation sûre de la structure attendue
        self._config: Dict[str, Any] = {
            "pays": {},
            "villes": {},
            "stations": {}
        }

    def get_config(self) -> Dict[str, Any]:
        return self._config

    def add_pays(self, pays_id: str, nom: str) -> None:
        # Utilise setdefault pour éviter KeyError si la clé n'existait pas
        self._config.setdefault("pays", {})[pays_id] = {"nom": nom}

    def remove_pays(self, pays_id: str) -> bool:
        return self._config.get("pays", {}).pop(pays_id, None) is not None

    def _load_configuration(self) -> None:
        """Charge la configuration depuis le fichier JSON."""
        if os.path.exists(self._config_file):
            try:
                with open(self._config_file, 'r', encoding='utf-8') as f:
                    self._config = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Erreur lors du chargement de la configuration: {e}")
                self._config = {"pays": {}, "villes": {}, "stations": {}}

    def _save_configuration(self) -> None:
        """Sauvegarde la configuration dans le fichier JSON."""
        try:
            with open(self._config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
        except IOError as e:
            print(f"Erreur lors de la sauvegarde: {e}")

    def get_pays(self) -> Dict:
        """Retourne tous les pays."""
        return self._config.get("pays", {})

    def get_villes(self, pays_id: Optional[str] = None) -> Dict:
        """Retourne toutes les villes ou celles d'un pays spécifique."""
        villes = self._config.get("villes", {})
        if pays_id:
            return {k: v for k, v in villes.items() if v.get("pays_id") == pays_id}
        return villes

    def get_stations(self, ville_id: Optional[str] = None) -> Dict:
        """Retourne toutes les stations ou celles d'une ville spécifique."""
        stations = self._config.get("stations", {})
        if ville_id:
            return {k: v for k, v in stations.items() if v.get("ville_id") == ville_id}
        return stations

    def add_pays(self, pays_id: str, nom: str) -> None:
        """Ajoute un nouveau pays."""
        self._config["pays"][pays_id] = {"nom": nom}
        self._save_configuration()

    def remove_pays(self, pays_id: str) -> bool:
        """Supprime un pays et ses villes/stations associées."""
        if pays_id in self._config["pays"]:
            # Supprimer les villes et stations liées
            villes_to_remove = [v_id for v_id, v in self._config["villes"].items()
                               if v.get("pays_id") == pays_id]
            for v_id in villes_to_remove:
                self.remove_ville(v_id)

            del self._config["pays"][pays_id]
            self._save_configuration()
            return True
        return False

    def add_ville(self, ville_id: str, nom: str, pays_id: str) -> None:
        """Ajoute une nouvelle ville."""
        self._config["villes"][ville_id] = {
            "nom": nom,
            "pays_id": pays_id
        }
        self._save_configuration()

    def remove_ville(self, ville_id: str) -> bool:
        """Supprime une ville et ses stations associées."""
        if ville_id in self._config["villes"]:
            # Supprimer les stations liées
            stations_to_remove = [s_id for s_id, s in self._config["stations"].items()
                                 if s.get("ville_id") == ville_id]
            for s_id in stations_to_remove:
                self.remove_station(s_id)

            del self._config["villes"][ville_id]
            self._save_configuration()
            return True
        return False

    def add_station(self, station_id: str, nom: str, ville_id: str, api_url: str) -> None:
        """Ajoute une nouvelle station météo."""
        self._config["stations"][station_id] = {
            "nom": nom,
            "ville_id": ville_id,
            "api_url": api_url
        }
        self._save_configuration()

    def update_station_url(self, station_id: str, new_url: str) -> bool:
        """Met à jour l'URL API d'une station."""
        if station_id in self._config["stations"]:
            self._config["stations"][station_id]["api_url"] = new_url
            self._save_configuration()
            return True
        return False

    def remove_station(self, station_id: str) -> bool:
        """Supprime une station météo."""
        if station_id in self._config["stations"]:
            del self._config["stations"][station_id]
            self._save_configuration()
            return True
        return False

    def get_station_by_id(self, station_id: str) -> Optional[Dict]:
        """Récupère une station par son ID."""
        return self._config["stations"].get(station_id)

    def get_all_stations_list(self) -> List[tuple]:
        """Retourne la liste de toutes les stations (id, nom, url)."""
        return [(s_id, s["nom"], s["api_url"])
                for s_id, s in self._config["stations"].items()]