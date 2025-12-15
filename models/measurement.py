"""Modèle pour une mesure météo."""
from datetime import datetime
from typing import Optional


class Measurement:
    """Représente une mesure météo."""

    def __init__(self, timestamp: str, temperature: float,
                 humidity: int, pressure: int):
        self.timestamp = timestamp
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        self.datetime = self._parse_datetime(timestamp)

    def _parse_datetime(self, timestamp: str) -> datetime:
        """Parse le timestamp en objet datetime."""
        try:
            return datetime.fromisoformat(timestamp.replace('+00:00', ''))
        except:
            return datetime.now()

    def get_time_str(self) -> str:
        """Retourne l'heure formatée."""
        return self.datetime.strftime("%H:%M")

    def get_date_str(self) -> str:
        """Retourne la date formatée."""
        return self.datetime.strftime("%d/%m/%Y")

    def get_date_key(self) -> str:
        """Retourne une clé de date pour le groupement."""
        return self.datetime.strftime("%Y-%m-%d")

    def __repr__(self):
        return f"Measurement({self.get_time_str()}, {self.temperature}°C)"
