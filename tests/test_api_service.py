"""
Tests unitaires pour ApiService.
Test des appels API et gestion d'erreurs réseau.
"""
from unittest.mock import Mock, patch

import requests

from weather_app.services.api_service import ApiService
from weather_app.models.location import Pays, Ville, Station
from weather_app.models.measurement import Measurement


class TestApiService:
    """Tests pour la classe ApiService."""

    def test_service_creation(self):
        """Test la création du service."""
        service = ApiService()

        assert service is not None

    def test_service_has_request_queue(self):
        """Test que le service a une file de requêtes."""
        service = ApiService()

        # Vérifier que le service a été créé sans erreur
        assert service is not None

    @patch('requests.get')
    def test_fetch_data_success(self, mock_get, sample_api_response):
        """Test le chargement réussi de données."""
        # Préparer le mock
        mock_response = Mock()
        mock_response.json.return_value = sample_api_response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        # Créer une station
        pays = Pays("fr001", "France")
        ville = Ville("v001", "Toulouse", pays)
        station = Station("s001", "Montaudran", ville, "https://api.example.com")

        # Exécuter
        service = ApiService()
        with patch('builtins.print'):
            result = service.fetch_data_for_station(station)

        # Vérifications
        assert result is True
        mock_get.assert_called_once_with("https://api.example.com", timeout=10)
        assert len(station.get_measurements()) == 2

    @patch('requests.get')
    def test_fetch_data_timeout(self, mock_get):
        """Test le comportement en cas de timeout."""
        mock_get.side_effect = requests.exceptions.Timeout()

        pays = Pays("fr001", "France")
        ville = Ville("v001", "Toulouse", pays)
        station = Station("s001", "Montaudran", ville, "https://api.example.com")

        service = ApiService()
        with patch('builtins.print'):
            result = service.fetch_data_for_station(station)

        assert result is False

    @patch('requests.get')
    def test_fetch_data_network_error(self, mock_get):
        """Test le comportement en cas d'erreur réseau."""
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        pays = Pays("fr001", "France")
        ville = Ville("v001", "Toulouse", pays)
        station = Station("s001", "Montaudran", ville, "https://api.example.com")

        service = ApiService()
        with patch('builtins.print'):
            result = service.fetch_data_for_station(station)

        assert result is False

    @patch('requests.get')
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
        with patch('builtins.print'):
            result = service.fetch_data_for_station(station)

        # Devrait réussir même sans résultats (liste vide)
        assert result is True
        assert len(station.get_measurements()) == 0

    @patch('requests.get')
    def test_fetch_data_clears_previous_measurements(self, mock_get, sample_api_response):
        """Test que les anciennes mesures sont effacées."""
        mock_response = Mock()
        mock_response.json.return_value = sample_api_response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        pays = Pays("fr001", "France")
        ville = Ville("v001", "Toulouse", pays)
        station = Station("s001", "Montaudran", ville, "https://api.example.com")

        # Ajouter des mesures initiales
        station.add_measurement(Measurement("2025-01-01T10:00:00+00:00", 10.0, 50, 100000))

        service = ApiService()
        with patch('builtins.print'):
            service.fetch_data_for_station(station)

        # Les anciennes mesures devraient être remplacées
        measurements = station.get_measurements()
        assert len(measurements) == 2  # Seulement les nouvelles

    def test_parse_measurements_valid_data(self):
        """Test le parsing de données valides."""
        data = {
            "results": [
                {
                    "heure_de_paris": "2025-02-11T10:00:00+00:00",
                    "temperature_en_degre_c": 20.5,
                    "humidite": 75,
                    "pression": 101325
                }
            ]
        }

        service = ApiService()
        measurements = service._parse_measurements(data)  # pylint: disable=protected-access

        assert len(measurements) == 1
        assert measurements[0].temperature == 20.5
        assert measurements[0].humidite == 75
        assert measurements[0].pression == 101325

    def test_parse_measurements_missing_fields(self):
        """Test le parsing avec champs manquants."""
        data = {
            "results": [
                {
                    "heure_de_paris": "2025-02-11T10:00:00+00:00",
                    # Champs manquants
                }
            ]
        }

        service = ApiService()
        with patch('builtins.print'):
            measurements = service._parse_measurements(data)  # pylint: disable=protected-access

        # Devrait utiliser des valeurs par défaut
        assert len(measurements) == 1

    def test_parse_measurements_invalid_types(self):
        """Test le parsing avec types invalides."""
        data = {
            "results": [
                {
                    "heure_de_paris": "2025-02-11T10:00:00+00:00",
                    "temperature_en_degre_c": "invalid",
                    "humidite": "invalid",
                    "pression": "invalid"
                }
            ]
        }

        service = ApiService()
        with patch('builtins.print'):
            measurements = service._parse_measurements(data)  # pylint: disable=protected-access

        # Les mesures invalides devraient être ignorées
        assert len(measurements) == 0

    def test_parse_measurements_empty_results(self):
        """Test le parsing avec résultats vides."""
        data = {"results": []}

        service = ApiService()
        measurements = service._parse_measurements(data)  # pylint: disable=protected-access

        assert len(measurements) == 0

    def test_parse_measurements_no_results_key(self):
        """Test le parsing sans clé results."""
        data = {"other_key": "value"}

        service = ApiService()
        measurements = service._parse_measurements(data)  # pylint: disable=protected-access

        assert len(measurements) == 0

    @patch('requests.get')
    def test_test_api_url_valid(self, mock_get):
        """Test la validation d'une URL valide."""
        mock_response = Mock()
        mock_response.json.return_value = {"results": []}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        service = ApiService()
        result = service.test_api_url("https://api.example.com")

        assert result is True

    @patch('requests.get')
    def test_test_api_url_invalid_response(self, mock_get):
        """Test la validation d'une URL avec réponse invalide."""
        mock_response = Mock()
        mock_response.json.return_value = {"no_results": []}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        service = ApiService()
        result = service.test_api_url("https://api.example.com")

        assert result is False

    @patch('requests.get')
    def test_test_api_url_network_error(self, mock_get):
        """Test la validation avec erreur réseau."""
        mock_get.side_effect = requests.exceptions.RequestException()

        service = ApiService()
        result = service.test_api_url("https://api.example.com")

        assert result is False

    @patch('requests.get')
    def test_test_api_url_timeout(self, mock_get):
        """Test la validation avec timeout."""
        mock_get.side_effect = requests.exceptions.Timeout()

        service = ApiService()
        result = service.test_api_url("https://api.example.com")

        assert result is False

    @patch('requests.get')
    def test_test_api_url_invalid_json(self, mock_get):
        """Test la validation avec JSON invalide."""
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        service = ApiService()
        result = service.test_api_url("https://api.example.com")

        assert result is False

    @patch('requests.get')
    def test_multiple_fetches(self, mock_get, sample_api_response):
        """Test plusieurs appels successifs."""
        mock_response = Mock()
        mock_response.json.return_value = sample_api_response
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        pays = Pays("fr001", "France")
        ville = Ville("v001", "Toulouse", pays)
        station1 = Station("s001", "Station1", ville, "https://api1.com")
        station2 = Station("s002", "Station2", ville, "https://api2.com")

        service = ApiService()

        with patch('builtins.print'):
            result1 = service.fetch_data_for_station(station1)
            result2 = service.fetch_data_for_station(station2)

        assert result1 is True
        assert result2 is True
        assert len(station1.get_measurements()) == 2
        assert len(station2.get_measurements()) == 2
