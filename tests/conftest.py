"""
Fixtures communes pour les tests.
Principe DRY: centralisation des fixtures réutilisables.
"""
import os
import shutil
import tempfile
from unittest.mock import Mock

import pytest


@pytest.fixture
def temp_config_file():
    """
    Fixture qui crée un fichier de configuration temporaire.

    Yields:
        str: Chemin vers le fichier temporaire
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        temp_path = f.name

    yield temp_path

    # Nettoyage
    if os.path.exists(temp_path):
        os.remove(temp_path)


@pytest.fixture
def temp_data_dir():
    """
    Fixture qui crée un répertoire temporaire pour les données.

    Yields:
        str: Chemin vers le répertoire temporaire
    """
    temp_dir = tempfile.mkdtemp()
    yield temp_dir

    # Nettoyage
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


@pytest.fixture
def mock_pays():
    """
    Fixture qui crée un mock de Pays.

    Returns:
        Mock: Mock configuré d'un Pays
    """
    pays = Mock()
    pays.id = "pays123"
    pays.nom = "France"
    pays.get_info.return_value = "Pays: France (ID: pays123) - 0 ville(s)"

    # pylint: disable=protected-access
    pays._villes = []

    return pays


@pytest.fixture
def mock_ville():
    """
    Fixture qui crée un mock de Ville.

    Returns:
        Mock: Mock configuré d'une Ville
    """
    ville = Mock()
    ville.id = "ville123"
    ville.nom = "Toulouse"
    ville.pays = Mock()
    ville.pays.nom = "France"
    ville.get_info.return_value = (
        "Ville: Toulouse (Pays: France) - 0 station(s)"
    )

    # pylint: disable=protected-access
    ville._stations = []

    return ville


@pytest.fixture
def mock_station():
    """
    Fixture qui crée un mock de Station.

    Returns:
        Mock: Mock configuré d'une Station
    """
    station = Mock()
    station.id = "station123"
    station.nom = "Montaudran"
    station.api_url = "https://api.example.com/data"
    station.ville = Mock()
    station.ville.nom = "Toulouse"
    station.ville.pays = Mock()
    station.ville.pays.nom = "France"

    # pylint: disable=protected-access
    station._measurements = []

    station.get_measurements.return_value = []
    station.clear_measurements = Mock()
    station.add_measurement = Mock()
    return station


@pytest.fixture
def mock_measurement():
    """
    Fixture qui crée un mock de Measurement.

    Returns:
        Mock: Mock configuré d'une Measurement
    """
    measurement = Mock()
    measurement.heure = "2025-02-11T10:00:00+00:00"
    measurement.temperature = 15.5
    measurement.humidite = 75
    measurement.pression = 101325
    measurement.format_heure.return_value = "11/02/2025 10:00"
    return measurement


@pytest.fixture
def sample_api_response():
    """
    Fixture qui retourne un exemple de réponse API.

    Returns:
        dict: Exemple de réponse API
    """
    return {
        "total_count": 100,
        "results": [
            {
                "heure_de_paris": "2025-02-11T10:00:00+00:00",
                "temperature_en_degre_c": 15.5,
                "humidite": 75,
                "pression": 101325,
            },
            {
                "heure_de_paris": "2025-02-11T09:00:00+00:00",
                "temperature_en_degre_c": 14.2,
                "humidite": 80,
                "pression": 101300,
            },
        ],
    }


@pytest.fixture
def mock_api_service():
    """
    Fixture qui crée un mock d'ApiService.

    Returns:
        Mock: Mock configuré d'ApiService
    """
    service = Mock()
    service.fetch_data_for_station.return_value = True
    service.test_api_url.return_value = True
    return service


@pytest.fixture
def mock_config():
    """
    Fixture qui crée un mock de ConfigurationSingleton.

    Returns:
        Mock: Mock configuré de ConfigurationSingleton
    """
    config = Mock()
    config.get_pays.return_value = {}
    config.get_villes.return_value = {}
    config.get_stations.return_value = {}
    config.add_pays = Mock()
    config.add_ville = Mock()
    config.add_station = Mock()
    config.remove_pays = Mock(return_value=True)
    config.remove_ville = Mock(return_value=True)
    config.remove_station = Mock(return_value=True)
    config.update_station_url = Mock(return_value=True)
    return config
