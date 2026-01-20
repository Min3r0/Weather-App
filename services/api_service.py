"""
Service pour gérer les appels à l'API météo.
"""
from typing import List, Dict

import requests

from weather_app.data_structures.queue import Queue
from weather_app.models.measurement import Measurement
from weather_app.models.location import Station


class ApiService:
    """
    Service pour gérer les requêtes API.
    """

    def __init__(self):
        """Initialise le service API avec une file de requêtes."""
        self._request_queue = Queue()
        self._timeout = 10  # Timeout en secondes

    def fetch_data_for_station(self, station: Station) -> bool:
        """
        Args:
            station: La station pour laquelle récupérer les données

        Returns:
            True si les données ont été chargées avec succès, False sinon
        """
        try:
            self._request_queue.enqueue(station.api_url)
            url = self._request_queue.dequeue()

            response = requests.get(url, timeout=self._timeout)
            response.raise_for_status()

            data = response.json()
            measurements = self._parse_measurements(data)

            station.clear_measurements()
            for measurement in measurements:
                station.add_measurement(measurement)

            print(f"✅ {len(measurements)} mesure(s) chargée(s) pour {station.nom}")
            return True

        except requests.exceptions.Timeout:
            print(f"❌ Timeout lors de la récupération des données pour {station.nom}")
            return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Erreur réseau: {str(e)}")
            return False
        except (KeyError, ValueError) as e:
            print(f"❌ Erreur lors du parsing des données: {str(e)}")
            return False

    def _parse_measurements(self, data: Dict) -> List[Measurement]:
        """
       Args:
            data: Les données JSON de l'API

        Returns:
            Liste d'objets Measurement
        """
        measurements = []

        results = data.get('results', [])
        for result in results:
            try:
                measurement = Measurement(
                    heure=result.get('heure_de_paris', ''),
                    temperature=float(result.get('temperature_en_degre_c', 0)),
                    humidite=int(result.get('humidite', 0)),
                    pression=int(result.get('pression', 0))
                )
                measurements.append(measurement)
            except (ValueError, TypeError) as e:
                print(f"⚠️  Erreur lors du parsing d'une mesure: {e}")
                continue

        return measurements

    def test_api_url(self, url: str) -> bool:
        """
        rgs:
            url: L'URL à tester

        Returns:
            True si l'URL est valide, False sinon
        """
        try:
            response = requests.get(url, timeout=self._timeout)
            response.raise_for_status()
            data = response.json()
            return 'results' in data
        except (requests.exceptions.RequestException, ValueError, KeyError):
            return False
