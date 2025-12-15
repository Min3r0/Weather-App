"""Modèle pour une station météo."""
from typing import List, Optional, Dict
from collections import defaultdict
from .measurement import Measurement


class Station:
    """Représente une station météo."""

    def __init__(self, name: str, url: str, city: str = "", country: str = ""):
        self.name = name
        self.url = url
        self.city = city
        self.country = country
        self.measurements: List[Measurement] = []

    def add_measurement(self, measurement: Measurement):
        """Ajoute une mesure à la station."""
        self.measurements.append(measurement)

    def clear_measurements(self):
        """Efface toutes les mesures."""
        self.measurements = []

    def get_sorted_measurements(self) -> List[Measurement]:
        """Retourne les mesures triées par date."""
        return sorted(self.measurements, key=lambda m: m.datetime)

    def get_measurements_by_date(self) -> Dict[str, List[Measurement]]:
        """Groupe les mesures par date."""
        grouped = defaultdict(list)
        for measurement in self.get_sorted_measurements():
            date_key = measurement.get_date_key()
            grouped[date_key].append(measurement)
        return dict(grouped)

    def update_url(self, new_url: str):
        """Met à jour l'URL de la station."""
        self.url = new_url

    def __repr__(self):
        return f"Station({self.name}, {len(self.measurements)} mesures)"
