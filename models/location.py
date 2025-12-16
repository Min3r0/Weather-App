from typing import List, Optional


class Pays:
    """Classe de base représentant un pays"""

    def __init__(self, nom: str):
        self.nom = nom
        self.villes: List['Ville'] = []

    def add_ville(self, ville: 'Ville'):
        """Ajoute une ville au pays"""
        self.villes.append(ville)
        ville.pays = self

    def __repr__(self):
        return f"Pays({self.nom}, {len(self.villes)} villes)"


class Ville(Pays):
    """Classe représentant une ville, hérite de Pays"""

    def __init__(self, nom: str, pays: Optional[Pays] = None):
        super().__init__(nom)
        self.pays = pays
        self.stations: List['Station'] = []

    def add_station(self, station: 'Station'):
        """Ajoute une station à la ville"""
        self.stations.append(station)
        station.ville = self

    def __repr__(self):
        return f"Ville({self.nom}, {len(self.stations)} stations)"


class Station(Ville):
    """Classe représentant une station météo, hérite de Ville"""

    def __init__(self, nom: str, ville: Optional[Ville] = None,
                 pays: Optional[Pays] = None, url: str = ""):
        super().__init__(nom, pays)
        self.ville = ville
        self.url = url
        self.measurements: List = []

    def set_measurements(self, measurements: List):
        """Définit les mesures de la station"""
        self.measurements = measurements

    def get_full_name(self) -> str:
        """Retourne le nom complet de la station"""
        parts = []
        if self.ville:
            parts.append(self.ville.nom)
        parts.append(self.nom)
        return " - ".join(parts)

    def __repr__(self):
        return f"Station({self.get_full_name()}, {len(self.measurements)} mesures)"
