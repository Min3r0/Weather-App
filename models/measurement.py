from datetime import datetime


class Measurement:
    """Représente une mesure météo à un instant donné"""

    def __init__(self, heure: str, temperature: float,
                 humidite: int, pression: int):
        self.heure = heure
        self.temperature = temperature
        self.humidite = humidite
        self.pression = pression
        self._parse_datetime()

    def _parse_datetime(self):
        """Parse la date/heure au format ISO"""
        try:
            self.datetime = datetime.fromisoformat(self.heure.replace('+00:00', ''))
        except:
            self.datetime = datetime.now()

    def get_date_str(self) -> str:
        """Retourne la date formatée"""
        return self.datetime.strftime("%d/%m/%Y")

    def get_time_str(self) -> str:
        """Retourne l'heure formatée"""
        return self.datetime.strftime("%H:%M")

    def __repr__(self):
        return f"Measurement({self.get_time_str()}, {self.temperature}°C, {self.humidite}%, {self.pression}hPa)"
