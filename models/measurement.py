"""
Modèle pour les mesures météorologiques.
"""
from datetime import datetime


class Measurement:

    def __init__(self,
                 heure: str,
                 temperature: float,
                 humidite: int,
                 pression: int):
        self._heure = heure
        self._temperature = temperature
        self._humidite = humidite
        self._pression = pression

    @property
    def heure(self) -> str:
        return self._heure

    @property
    def temperature(self) -> float:
        return self._temperature

    @property
    def humidite(self) -> int:
        return self._humidite

    @property
    def pression(self) -> int:
        return self._pression

    def format_heure(self) -> str:
        """Formate l'heure de manière lisible."""
        try:
            dt = datetime.fromisoformat(self._heure.replace('Z', '+00:00'))
            return dt.strftime("%d/%m/%Y %H:%M")
        except (ValueError, AttributeError):
            return self._heure

    def __str__(self) -> str:
        """Représentation textuelle de la mesure."""
        return (f"{self.format_heure()} - "
                f"Temp: {self._temperature}°C, "
                f"Hum: {self._humidite}%, "
                f"Press: {self._pression} Pa")

    def __repr__(self) -> str:
        return f"Measurement({self._heure}, {self._temperature}°C, {self._humidite}%, {self._pression}Pa)"
