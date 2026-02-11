"""
Tests unitaires pour ApiService.
Test des appels API et gestion d'erreurs réseau.
"""
from unittest.mock import Mock, patch

import requests

from weather_app.data_structures.queue import Queue
from weather_app.models.location import Pays, Ville, Station
from weather_app.models.measurement import Measurement
from weather_app.services.api_service import ApiService


class TestApiService:
    """Tests pour la classe ApiService."""

    def test_service_creation(self):
        """Test la création du service."""
        service = ApiService()

        # pylint: disable=protected-access
        assert service._request_queue is not None
        assert service._timeout == 10

    def test_service_has_request_queue(self):
        """Test que le service a une file de requêtes."""
        service = ApiService()

        # pylint: disable=protected-access
        assert hasattr(service, "_request_queue")
        assert isinstance(service._request_queue, Queue)

    @patch("requests.get")
    def test_fetch_data_success(self, mock_get, sample_api_response):
        """Test le chargement réussi de données."""
        mock_response = Mock()
        mock_response.json.return_value = sample_api_response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        pays = Pays("fr001", "France")
        ville = Ville("v001", "Toulouse", pays)
        station = Station("s001", "Montaudran", ville, "https://api.example.com")

        service = ApiService()
        with patch("builtins.print"):
            result = service.fetch_data_for_station(station)

        assert result is True
        mock_get.assert_called_once_with(
            "https://api.example.com", timeout=10
        )
        assert len(station.get_measurements()) == 2

    @patch("requests.get")
    def test_fetch_data_timeout(self, mock_get):
        """Test le comportement en cas de timeout."""
        mock_get.side_effect = requests.exceptions.Timeout()

        pays = Pays("fr001", "France")
        ville = Ville("v001", "Toulouse", pays)
        station = Station("s001", "Montaudran", ville, "https://api.example.com")

        service = ApiService()
        with patch("builtins.print"):
            result = service.fetch_data_for_station(station)

        assert result is False

    @patch("requests.get")
    def test_fetch_data_network_error(self, mock_get):
        """Test le comportement en cas d'erreur réseau."""
        mock_get.side_effect = requests.exceptions.RequestException(
            "Network error"
        )

        pays = Pays("fr001", "France")
        ville = Ville("v001", "Toulouse", pays)
        station = Station("s001", "Montaudran", ville, "https://api.example.com")

        service = ApiService()
        with patch("builtins.print"):
            result = service.fetch_data_for_station(station)

        assert result is False

    @patch("requests.get")
    def test_fetch_data_parsing_error(self, mock_get):
        """Test le comportement en cas d'erreur de parsing."""
        mock_response = Mock()
        mock_response.json.return_value = {"invalid": "data"}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        pays = Pays("fr001", "France")
        ville = Ville("v001", "Toulouse", pays)
        station = Station("s001", "Montaudran", ville, "https://api.example.com")

        service = ApiService()
        with patch("builtins.print"):
            result = service.fetch_data_for_station(station)

        assert result is True
        assert len(station.get_measurements()) == 0

    @patch("requests.get")
    def test_fetch_data_clears_previous_measurements(
        self, mock_get, sample_api_response
    ):
        """Test que les anciennes mesures sont effacées."""
        mock_response = Mock()
        mock_response.json.return_value = sample_api_response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        pays = Pays("fr001", "France")
        ville = Ville("v001", "Toulouse", pays)
        station = Station("s001", "Montaudran", ville, "https://api.example.com")

        station.add_measurement(
            Measurement("2025-01-01T10:00:00+00:00", 10.0, 50, 100000)
        )

        service = ApiService()
        with patch("builtins.print"):
            service.fetch_data_for_station(station)

        measurements = station.get_measurements()
        assert len(measurements) == 2

    @patch("requests.get")
    def test_parse_measurements_valid_data(self, _mock_get):
        """Test le parsing de données valides."""
        data = {
            "results": [
                {
                    "heure_de_paris": "2025-02-11T10:00:00+00:00",
                    "temperature_en_degre_c": 20.5,
                    "humidite": 75,
                    "pression": 101325,
                }
            ]
        }

        service = ApiService()

        # pylint: disable=protected-access
        measurements = service._parse_measurements(data)

        assert len(measurements) == 1
        assert measurements[0].temperature == 20.5
        assert measurements[0].humidite == 75
        assert measurements[0].pression == 101325

    @patch("requests.get")
    def test_parse_measurements_missing_fields(self, _mock_get):
        """Test le parsing avec champs manquants."""
        data = {"results": [{"heure_de_paris": "2025-02-11T10:00:00+00:00"}]}

        service = ApiService()
        with patch("builtins.print"):
            # pylint: disable=protected-access
            measurements = service._parse_measurements(data)

        assert len(measurements) == 1

    @patch("requests.get")
    def test_parse_measurements_invalid_types(self, _mock_get):
        """Test le parsing avec types invalides."""
        data = {
            "results": [
                {
                    "heure_de_paris": "2025-02-11T10:00:00+00:00",
                    "temperature_en_degre_c": "invalid",
                    "humidite": "invalid",
                    "pression": "invalid",
                }
            ]
        }

        service = ApiService()
        with patch("builtins.print"):
            # pylint: disable=protected-access
            measurements = service._parse_measurements(data)

        assert len(measurements) == 0

    @patch("requests.get")
    def test_parse_measurements_empty_results(self, _mock_get):
        """Test le parsing avec une liste de résultats vide."""
        service = ApiService()

        # pylint: disable=protected-access
        measurements = service._parse_measurements({"results": []})

        assert len(measurements) == 0

    @patch("requests.get")
    def test_parse_measurements_no_results_key(self, _mock_get):
        """Test le parsing lorsque la clé 'results' est absente."""
        service = ApiService()

        # pylint: disable=protected-access
        measurements = service._parse_measurements({"other_key": "value"})

        assert len(measurements) == 0

    @patch("requests.get")
    def test_queue_usage(self, mock_get, sample_api_response):
        mock_response = Mock()
        mock_response.json.return_value = sample_api_response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        pays = Pays("fr001", "France")
        ville = Ville("v001", "Toulouse", pays)
        station = Station("s001", "Montaudran", ville, "https://api.example.com")

        service = ApiService()

        # pylint: disable=protected-access
        assert service._request_queue.is_empty()

        with patch("builtins.print"):
            service.fetch_data_for_station(station)

        # pylint: disable=protected-access
        assert service._request_queue.is_empty()
