"""
Tests unitaires pour le Singleton Configuration.
Test du pattern Singleton et de la persistance.
"""
import os
from unittest.mock import patch

from weather_app.config.singleton_config import ConfigurationSingleton


class TestConfigurationSingleton:
    """Tests pour la classe ConfigurationSingleton."""

    def test_singleton_instance(self, temp_data_dir):
        """Test que le singleton retourne toujours la même instance."""
        with patch('weather_app.config.singleton_config.os.path.dirname') as mock_dirname:
            mock_dirname.return_value = temp_data_dir

            # Réinitialiser le singleton pour les tests
            # pylint: disable=protected-access
            ConfigurationSingleton._instance = None
            ConfigurationSingleton._initialized = False
            # pylint: enable=protected-access

            instance1 = ConfigurationSingleton()
            instance2 = ConfigurationSingleton()

            assert instance1 is instance2

    def test_singleton_initialized_once(self, temp_data_dir):
        """Test que le singleton n'est initialisé qu'une fois."""
        with patch('weather_app.config.singleton_config.os.path.dirname') as mock_dirname:
            mock_dirname.return_value = temp_data_dir

            # pylint: disable=protected-access
            ConfigurationSingleton._instance = None
            ConfigurationSingleton._initialized = False
            # pylint: enable=protected-access

            config1 = ConfigurationSingleton()

            # Modifier la config
            config1.add_pays("test_id", "Test")

            # Créer une "nouvelle" instance
            config2 = ConfigurationSingleton()

            # Devrait avoir la même config
            assert config2.get_pays() == config1.get_pays()

    def test_initialization_creates_data_dir(self, temp_data_dir):
        """Test que l'initialisation crée le répertoire data."""
        with patch('weather_app.config.singleton_config.os.path.dirname') as mock_dirname:
            mock_dirname.return_value = temp_data_dir

            # pylint: disable=protected-access
            ConfigurationSingleton._instance = None
            ConfigurationSingleton._initialized = False
            # pylint: enable=protected-access

            ConfigurationSingleton()

            expected_data_dir = os.path.join(temp_data_dir, 'data')
            assert os.path.exists(expected_data_dir)

    def test_default_config_structure(self, temp_data_dir):
        """Test la structure par défaut de la configuration."""
        with patch('weather_app.config.singleton_config.os.path.dirname') as mock_dirname:
            mock_dirname.return_value = temp_data_dir

            # pylint: disable=protected-access
            ConfigurationSingleton._instance = None
            ConfigurationSingleton._initialized = False
            # pylint: enable=protected-access

            config = ConfigurationSingleton()

            # Vérifier la structure via les méthodes publiques
            assert isinstance(config.get_pays(), dict)
            assert isinstance(config.get_villes(), dict)
            assert isinstance(config.get_stations(), dict)

    def test_add_pays(self, temp_data_dir):
        """Test l'ajout d'un pays."""
        with patch('weather_app.config.singleton_config.os.path.dirname') as mock_dirname:
            mock_dirname.return_value = temp_data_dir

            # pylint: disable=protected-access
            ConfigurationSingleton._instance = None
            ConfigurationSingleton._initialized = False
            # pylint: enable=protected-access

            config = ConfigurationSingleton()
            config.add_pays("fr001", "France")

            pays = config.get_pays()
            assert "fr001" in pays
            assert pays["fr001"]["nom"] == "France"

    def test_add_multiple_pays(self, temp_data_dir):
        """Test l'ajout de plusieurs pays."""
        with patch('weather_app.config.singleton_config.os.path.dirname') as mock_dirname:
            mock_dirname.return_value = temp_data_dir

            # pylint: disable=protected-access
            ConfigurationSingleton._instance = None
            ConfigurationSingleton._initialized = False
            # pylint: enable=protected-access

            config = ConfigurationSingleton()
            config.add_pays("fr001", "France")
            config.add_pays("es001", "Espagne")
            config.add_pays("de001", "Allemagne")

            pays = config.get_pays()
            assert len(pays) == 3
            assert "fr001" in pays
            assert "es001" in pays
            assert "de001" in pays

    def test_remove_pays(self, temp_data_dir):
        """Test la suppression d'un pays."""
        with patch('weather_app.config.singleton_config.os.path.dirname') as mock_dirname:
            mock_dirname.return_value = temp_data_dir

            # pylint: disable=protected-access
            ConfigurationSingleton._instance = None
            ConfigurationSingleton._initialized = False
            # pylint: enable=protected-access

            config = ConfigurationSingleton()
            config.add_pays("fr001", "France")

            result = config.remove_pays("fr001")

            assert result is True
            assert "fr001" not in config.get_pays()

    def test_remove_nonexistent_pays(self, temp_data_dir):
        """Test la suppression d'un pays inexistant."""
        with patch('weather_app.config.singleton_config.os.path.dirname') as mock_dirname:
            mock_dirname.return_value = temp_data_dir

            # pylint: disable=protected-access
            ConfigurationSingleton._instance = None
            ConfigurationSingleton._initialized = False
            # pylint: enable=protected-access

            config = ConfigurationSingleton()

            result = config.remove_pays("nonexistent")

            assert result is False

    def test_add_ville(self, temp_data_dir):
        """Test l'ajout d'une ville."""
        with patch('weather_app.config.singleton_config.os.path.dirname') as mock_dirname:
            mock_dirname.return_value = temp_data_dir

            # pylint: disable=protected-access
            ConfigurationSingleton._instance = None
            ConfigurationSingleton._initialized = False
            # pylint: enable=protected-access

            config = ConfigurationSingleton()
            config.add_pays("fr001", "France")
            config.add_ville("v001", "Toulouse", "fr001")

            villes = config.get_villes()
            assert "v001" in villes
            assert villes["v001"]["nom"] == "Toulouse"
            assert villes["v001"]["pays_id"] == "fr001"

    def test_get_villes_by_pays(self, temp_data_dir):
        """Test la récupération des villes d'un pays."""
        with patch('weather_app.config.singleton_config.os.path.dirname') as mock_dirname:
            mock_dirname.return_value = temp_data_dir

            # pylint: disable=protected-access
            ConfigurationSingleton._instance = None
            ConfigurationSingleton._initialized = False
            # pylint: enable=protected-access

            config = ConfigurationSingleton()
            config.add_pays("fr001", "France")
            config.add_pays("es001", "Espagne")
            config.add_ville("v001", "Toulouse", "fr001")
            config.add_ville("v002", "Paris", "fr001")
            config.add_ville("v003", "Madrid", "es001")

            villes_france = config.get_villes("fr001")

            assert len(villes_france) == 2
            assert "v001" in villes_france
            assert "v002" in villes_france
            assert "v003" not in villes_france

    def test_remove_ville(self, temp_data_dir):
        """Test la suppression d'une ville."""
        with patch('weather_app.config.singleton_config.os.path.dirname') as mock_dirname:
            mock_dirname.return_value = temp_data_dir

            # pylint: disable=protected-access
            ConfigurationSingleton._instance = None
            ConfigurationSingleton._initialized = False
            # pylint: enable=protected-access

            config = ConfigurationSingleton()
            config.add_pays("fr001", "France")
            config.add_ville("v001", "Toulouse", "fr001")

            result = config.remove_ville("v001")

            assert result is True
            assert "v001" not in config.get_villes()

    def test_remove_pays_cascades_to_villes(self, temp_data_dir):
        """Test que supprimer un pays supprime ses villes."""
        with patch('weather_app.config.singleton_config.os.path.dirname') as mock_dirname:
            mock_dirname.return_value = temp_data_dir

            # pylint: disable=protected-access
            ConfigurationSingleton._instance = None
            ConfigurationSingleton._initialized = False
            # pylint: enable=protected-access

            config = ConfigurationSingleton()
            config.add_pays("fr001", "France")
            config.add_ville("v001", "Toulouse", "fr001")
            config.add_ville("v002", "Paris", "fr001")

            config.remove_pays("fr001")

            villes = config.get_villes()
            assert "v001" not in villes
            assert "v002" not in villes

    def test_add_station(self, temp_data_dir):
        """Test l'ajout d'une station."""
        with patch('weather_app.config.singleton_config.os.path.dirname') as mock_dirname:
            mock_dirname.return_value = temp_data_dir

            # pylint: disable=protected-access
            ConfigurationSingleton._instance = None
            ConfigurationSingleton._initialized = False
            # pylint: enable=protected-access

            config = ConfigurationSingleton()
            config.add_pays("fr001", "France")
            config.add_ville("v001", "Toulouse", "fr001")
            config.add_station("s001", "Montaudran", "v001", "https://api.com")

            stations = config.get_stations()
            assert "s001" in stations
            assert stations["s001"]["nom"] == "Montaudran"
            assert stations["s001"]["ville_id"] == "v001"
            assert stations["s001"]["api_url"] == "https://api.com"

    def test_get_stations_by_ville(self, temp_data_dir):
        """Test la récupération des stations d'une ville."""
        with patch('weather_app.config.singleton_config.os.path.dirname') as mock_dirname:
            mock_dirname.return_value = temp_data_dir

            # pylint: disable=protected-access
            ConfigurationSingleton._instance = None
            ConfigurationSingleton._initialized = False
            # pylint: enable=protected-access

            config = ConfigurationSingleton()
            config.add_pays("fr001", "France")
            config.add_ville("v001", "Toulouse", "fr001")
            config.add_ville("v002", "Paris", "fr001")
            config.add_station("s001", "Montaudran", "v001", "https://api1.com")
            config.add_station("s002", "Blagnac", "v001", "https://api2.com")
            config.add_station("s003", "Orly", "v002", "https://api3.com")

            stations_toulouse = config.get_stations("v001")

            assert len(stations_toulouse) == 2
            assert "s001" in stations_toulouse
            assert "s002" in stations_toulouse
            assert "s003" not in stations_toulouse

    def test_update_station_url(self, temp_data_dir):
        """Test la mise à jour de l'URL d'une station."""
        with patch('weather_app.config.singleton_config.os.path.dirname') as mock_dirname:
            mock_dirname.return_value = temp_data_dir

            # pylint: disable=protected-access
            ConfigurationSingleton._instance = None
            ConfigurationSingleton._initialized = False
            # pylint: enable=protected-access

            config = ConfigurationSingleton()
            config.add_pays("fr001", "France")
            config.add_ville("v001", "Toulouse", "fr001")
            config.add_station("s001", "Montaudran", "v001", "https://old-api.com")

            result = config.update_station_url("s001", "https://new-api.com")

            assert result is True
            stations = config.get_stations()
            assert stations["s001"]["api_url"] == "https://new-api.com"

    def test_remove_station(self, temp_data_dir):
        """Test la suppression d'une station."""
        with patch('weather_app.config.singleton_config.os.path.dirname') as mock_dirname:
            mock_dirname.return_value = temp_data_dir

            # pylint: disable=protected-access
            ConfigurationSingleton._instance = None
            ConfigurationSingleton._initialized = False
            # pylint: enable=protected-access

            config = ConfigurationSingleton()
            config.add_pays("fr001", "France")
            config.add_ville("v001", "Toulouse", "fr001")
            config.add_station("s001", "Montaudran", "v001", "https://api.com")

            result = config.remove_station("s001")

            assert result is True
            assert "s001" not in config.get_stations()

    def test_remove_ville_cascades_to_stations(self, temp_data_dir):
        """Test que supprimer une ville supprime ses stations."""
        with patch('weather_app.config.singleton_config.os.path.dirname') as mock_dirname:
            mock_dirname.return_value = temp_data_dir

            # pylint: disable=protected-access
            ConfigurationSingleton._instance = None
            ConfigurationSingleton._initialized = False
            # pylint: enable=protected-access

            config = ConfigurationSingleton()
            config.add_pays("fr001", "France")
            config.add_ville("v001", "Toulouse", "fr001")
            config.add_station("s001", "Montaudran", "v001", "https://api1.com")
            config.add_station("s002", "Blagnac", "v001", "https://api2.com")

            config.remove_ville("v001")

            stations = config.get_stations()
            assert "s001" not in stations
            assert "s002" not in stations

    def test_get_station_by_id(self, temp_data_dir):
        """Test la récupération d'une station par ID."""
        with patch('weather_app.config.singleton_config.os.path.dirname') as mock_dirname:
            mock_dirname.return_value = temp_data_dir

            # pylint: disable=protected-access
            ConfigurationSingleton._instance = None
            ConfigurationSingleton._initialized = False
            # pylint: enable=protected-access

            config = ConfigurationSingleton()
            config.add_pays("fr001", "France")
            config.add_ville("v001", "Toulouse", "fr001")
            config.add_station("s001", "Montaudran", "v001", "https://api.com")

            station = config.get_station_by_id("s001")

            assert station is not None
            assert station["nom"] == "Montaudran"
            assert station["api_url"] == "https://api.com"

    def test_get_all_stations_list(self, temp_data_dir):
        """Test la récupération de toutes les stations sous forme de liste."""
        with patch('weather_app.config.singleton_config.os.path.dirname') as mock_dirname:
            mock_dirname.return_value = temp_data_dir

            # pylint: disable=protected-access
            ConfigurationSingleton._instance = None
            ConfigurationSingleton._initialized = False
            # pylint: enable=protected-access

            config = ConfigurationSingleton()
            config.add_pays("fr001", "France")
            config.add_ville("v001", "Toulouse", "fr001")
            config.add_station("s001", "Station1", "v001", "https://api1.com")
            config.add_station("s002", "Station2", "v001", "https://api2.com")

            stations_list = config.get_all_stations_list()

            assert len(stations_list) == 2
            assert isinstance(stations_list[0], tuple)
            assert len(stations_list[0]) == 3  # (id, nom, url)

    def test_persistence(self, temp_data_dir):
        """Test la persistance de la configuration."""
        with patch('weather_app.config.singleton_config.os.path.dirname') as mock_dirname:
            mock_dirname.return_value = temp_data_dir

            # Créer et configurer
            # pylint: disable=protected-access
            ConfigurationSingleton._instance = None
            ConfigurationSingleton._initialized = False
            # pylint: enable=protected-access
            config1 = ConfigurationSingleton()
            config1.add_pays("fr001", "France")

            # Réinitialiser et recharger
            # pylint: disable=protected-access
            ConfigurationSingleton._instance = None
            ConfigurationSingleton._initialized = False
            # pylint: enable=protected-access
            config2 = ConfigurationSingleton()

            # Devrait avoir chargé la config sauvegardée
            pays = config2.get_pays()
            assert "fr001" in pays
            assert pays["fr001"]["nom"] == "France"
