from models.location import Pays, Ville, Station
from config.config_singleton import ConfigSingleton


class StationBuilder:
    """Builder pour construire des objets Station"""

    def __init__(self):
        self.reset()

    def reset(self):
        """Réinitialise le builder"""
        self._station = None
        self._nom = ""
        self._ville = None
        self._pays = None
        self._url = ""

    def set_nom(self, nom: str) -> 'StationBuilder':
        """Définit le nom de la station"""
        self._nom = nom
        return self

    def set_ville(self, ville: Ville) -> 'StationBuilder':
        """Définit la ville"""
        self._ville = ville
        return self

    def set_pays(self, pays: Pays) -> 'StationBuilder':
        """Définit le pays"""
        self._pays = pays
        return self

    def set_url(self, url: str) -> 'StationBuilder':
        """Définit l'URL de l'API"""
        self._url = url
        return self

    def build(self) -> Station:
        """Construit et retourne la station"""
        station = Station(self._nom, self._ville, self._pays, self._url)

        # Sauvegarde dans le config singleton
        config = ConfigSingleton()
        if self._pays and self._ville:
            config.add_station(self._pays.nom, self._ville.nom, self._nom, self._url)

        self.reset()
        return station
