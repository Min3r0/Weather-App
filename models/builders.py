"""
Pattern Builder pour la construction des stations météo.
"""
from typing import Optional
from weather_app.models.location import Station, Ville, Pays


class StationBuilder:
    """
    Builder pour construire progressivement une Station.
    Principe KISS: construction simple et étape par étape.
    """

    def __init__(self):
        self._id: Optional[str] = None
        self._nom: Optional[str] = None
        self._ville: Optional[Ville] = None
        self._api_url: Optional[str] = None

    def set_id(self, station_id: str) -> 'StationBuilder':
        """Définit l'ID de la station."""
        self._id = station_id
        return self

    def set_nom(self, nom: str) -> 'StationBuilder':
        """Définit le nom de la station."""
        self._nom = nom
        return self

    def set_ville(self, ville: Ville) -> 'StationBuilder':
        """Définit la ville de la station."""
        self._ville = ville
        return self

    def set_api_url(self, api_url: str) -> 'StationBuilder':
        """Définit l'URL de l'API."""
        self._api_url = api_url
        return self

    def build(self) -> Station:
        """
        Construit et retourne la station.
        Lève une exception si des informations sont manquantes.
        """
        if not all([self._id, self._nom, self._ville, self._api_url]):
            missing = []
            if not self._id:
                missing.append("ID")
            if not self._nom:
                missing.append("nom")
            if not self._ville:
                missing.append("ville")
            if not self._api_url:
                missing.append("API URL")
            raise ValueError(f"Informations manquantes pour créer la station: {', '.join(missing)}")

        return Station(self._id, self._nom, self._ville, self._api_url)

    def reset(self) -> 'StationBuilder':
        """Réinitialise le builder."""
        self._id = None
        self._nom = None
        self._ville = None
        self._api_url = None
        return self


class VilleBuilder:
    """Builder pour construire une Ville."""

    def __init__(self):
        self._id: Optional[str] = None
        self._nom: Optional[str] = None
        self._pays: Optional[Pays] = None

    def set_id(self, ville_id: str) -> 'VilleBuilder':
        """Définit l'ID de la ville."""
        self._id = ville_id
        return self

    def set_nom(self, nom: str) -> 'VilleBuilder':
        """Définit le nom de la ville."""
        self._nom = nom
        return self

    def set_pays(self, pays: Pays) -> 'VilleBuilder':
        """Définit le pays de la ville."""
        self._pays = pays
        return self

    def build(self) -> Ville:
        """Construit et retourne la ville."""
        if not all([self._id, self._nom, self._pays]):
            raise ValueError("Informations manquantes pour créer la ville")

        return Ville(self._id, self._nom, self._pays)

    def reset(self) -> 'VilleBuilder':
        """Réinitialise le builder."""
        self._id = None
        self._nom = None
        self._pays = None
        return self
