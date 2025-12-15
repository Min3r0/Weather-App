"""Service pour récupérer les données API."""
import requests
from typing import List, Dict, Any
from models.station import Station
from models.measurement import Measurement
from .api_queue import APIQueue


class APIService:
    """Service pour interagir avec l'API météo."""

    def __init__(self):
        self.queue = APIQueue()

    def fetch_measurements(self, station: Station) -> bool:
        """Récupère les mesures d'une station."""
        try:
            response = requests.get(station.url, timeout=10)
            response.raise_for_status()
            data = response.json()

            station.clear_measurements()

            results = data.get('results', [])
            for record in results:
                measurement = Measurement(
                    timestamp=record.get('heure_de_paris', ''),
                    temperature=float(record.get('temperature_en_degre_c', 0)),
                    humidity=int(record.get('humidite', 0)),
                    pressure=int(record.get('pression', 0))
                )
                station.add_measurement(measurement)

            return True
        except Exception as e:
            print(f"Erreur lors de la récupération des données: {e}")
            return False

    def add_to_queue(self, station: Station):
        """Ajoute une station à la file d'attente."""
        self.queue.enqueue(station)

    def process_queue(self):
        """Traite toutes les stations de la file."""
        while not self.queue.is_empty():
            station = self.queue.dequeue()
            if station:
                self.fetch_measurements(station)