"""Pattern Builder pour construire des stations."""
from models.station import Station


class StationBuilder:
    """Builder pour construire une station météo."""

    def __init__(self):
        self._station: Station = None
        self._name: str = ""
        self._url: str = ""
        self._city: str = ""
        self._country: str = ""

    def reset(self):
        """Réinitialise le builder."""
        self._station = None
        self._name = ""
        self._url = ""
        self._city = ""
        self._country = ""
        return self

    def set_name(self, name: str):
        """Définit le nom de la station."""
        self._name = name
        return self

    def set_url(self, url: str):
        """Définit l'URL de la station."""
        self._url = url
        return self

    def set_city(self, city: str):
        """Définit la ville de la station."""
        self._city = city
        return self

    def set_country(self, country: str):
        """Définit le pays de la station."""
        self._country = country
        return self

    def build(self) -> Station:
        """Construit et retourne la station."""
        if not self._name or not self._url:
            raise ValueError("Le nom et l'URL sont obligatoires")

        self._station = Station(
            name=self._name,
            url=self._url,
            city=self._city,
            country=self._country
        )
        return self._station