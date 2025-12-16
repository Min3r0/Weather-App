import requests
from typing import List, Optional
from models.measurement import Measurement
from data_structures.queue import Queue


class APIService:
    """Service pour récupérer les données météo depuis l'API"""

    def __init__(self):
        self.request_queue = Queue()

    def fetch_measurements(self, url: str) -> Optional[List[Measurement]]:
        """Récupère les mesures depuis l'API"""
        try:
            # Ajoute la requête à la file
            self.request_queue.enqueue(url)

            # Traite la requête
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            data = response.json()
            measurements = []

            # Parse les résultats
            for result in data.get('results', []):
                # Gère différents formats de clés
                heure = result.get('heure_de_paris') or result.get('date_de_mesure', '')
                temp = result.get('temperature_en_degre_c', 0)
                hum = result.get('humidite', 0)
                press = result.get('pression', 0)

                measurement = Measurement(heure, temp, hum, press)
                measurements.append(measurement)

            # Retire la requête de la file
            self.request_queue.dequeue()

            return measurements

        except requests.RequestException as e:
            print(f"Erreur lors de la récupération des données: {e}")
            self.request_queue.dequeue()
            return None
        except Exception as e:
            print(f"Erreur inattendue: {e}")
            self.request_queue.dequeue()
            return None
