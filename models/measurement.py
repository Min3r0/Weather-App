"""
Modèle pour les mesures météorologiques.
"""
from datetime import datetime


class Measurement:
    """
    Représente une mesure météorologique à un instant donné.

    Attributes:
        heure: Horodatage de la mesure (format ISO 8601)
        temperature: Température en degrés Celsius
        humidite: Taux d'humidité en pourcentage
        pression: Pression atmosphérique en Pascals
    """

    def __init__(self,
                 heure: str,
                 temperature: float,
                 humidite: int,
                 pression: int):
        """
        Initialise une mesure météorologique.

        Args:
            heure: Horodatage de la mesure (ISO 8601)
            temperature: Température en °C
            humidite: Humidité en %
            pression: Pression en Pa
        """
        self._heure = heure
        self._temperature = temperature
        self._humidite = humidite
        self._pression = pression

    @property
    def heure(self) -> str:
        """Retourne l'horodatage de la mesure."""
        return self._heure

    @property
    def temperature(self) -> float:
        """Retourne la température en degrés Celsius."""
        return self._temperature

    @property
    def humidite(self) -> int:
        """Retourne le taux d'humidité en pourcentage."""
        return self._humidite

    @property
    def pression(self) -> int:
        """Retourne la pression atmosphérique en Pascals."""
        return self._pression

    def format_heure(self) -> str:
        """
        Formate l'heure de manière lisible.

        Returns:
            str: Date et heure formatées (JJ/MM/AAAA HH:MM)
        """
        try:
            dt = datetime.fromisoformat(self._heure.replace('Z', '+00:00'))
            return dt.strftime("%d/%m/%Y %H:%M")
        except (ValueError, AttributeError):
            return self._heure

    def __str__(self) -> str:
        """Représentation textuelle de la mesure."""
        return (
            f"{self.format_heure()} - "
            f"Temp: {self._temperature}°C, "
            f"Hum: {self._humidite}%, "
            f"Press: {self._pression} Pa"
        )

    def __repr__(self) -> str:
        """Représentation technique de la mesure."""
        return (
            f"Measurement({self._heure}, {self._temperature}°C, "
            f"{self._humidite}%, {self._pression}Pa)"
        )
