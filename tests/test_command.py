"""
Tests unitaires pour le pattern Command.
"""

# pylint: disable=too-few-public-methods

from unittest.mock import Mock, patch

from weather_app.patterns.command import (
    CommandInvoker, SelectStationCommand, RefreshDataCommand,
    DisplayMeasurementsCommand, AddCountryCommand, RemoveCountryCommand,
    AddCityCommand, RemoveCityCommand, AddStationCommand,
    RemoveStationCommand, UpdateStationUrlCommand
)


class TestCommandInvoker:
    """Tests pour la classe CommandInvoker."""

    def test_invoker_creation(self):
        """Test la création d'un invocateur."""
        invoker = CommandInvoker()

        history = invoker.get_history()
        assert not history

    def test_execute_command(self):
        """Test l'exécution d'une commande."""
        invoker = CommandInvoker()
        mock_command = Mock()
        mock_command.execute.return_value = "result"

        result = invoker.execute_command(mock_command)

        assert result == "result"
        mock_command.execute.assert_called_once()

    def test_command_added_to_history(self):
        """Test que la commande est ajoutée à l'historique."""
        invoker = CommandInvoker()
        mock_command = Mock()

        invoker.execute_command(mock_command)

        history = invoker.get_history()
        assert mock_command in history
        assert len(history) == 1

    def test_get_history(self):
        """Test la récupération de l'historique."""
        invoker = CommandInvoker()
        cmd1 = Mock()
        cmd2 = Mock()
        cmd3 = Mock()

        invoker.execute_command(cmd1)
        invoker.execute_command(cmd2)
        invoker.execute_command(cmd3)

        history = invoker.get_history()

        assert len(history) == 3
        assert cmd1 in history
        assert cmd2 in history
        assert cmd3 in history

    def test_get_history_returns_copy(self):
        """Test que get_history retourne une copie."""
        invoker = CommandInvoker()
        cmd = Mock()
        invoker.execute_command(cmd)

        history1 = invoker.get_history()
        history2 = invoker.get_history()

        assert history1 == history2
        assert history1 is not history2


class TestSelectStationCommand:
    """Tests pour SelectStationCommand."""

    def test_command_creation(self):
        """Test la création de la commande."""
        mock_selector = Mock()
        mock_station = Mock()

        cmd = SelectStationCommand(mock_selector, mock_station)

        # Vérifier que la commande a été créée
        assert cmd is not None

    def test_execute(self):
        """Test l'exécution de la commande."""
        mock_selector = Mock()
        mock_station = Mock()
        cmd = SelectStationCommand(mock_selector, mock_station)

        result = cmd.execute()

        mock_selector.select_station.assert_called_once_with(mock_station)
        assert result == mock_station


class TestRefreshDataCommand:
    """Tests pour RefreshDataCommand."""

    def test_command_creation(self):
        """Test la création de la commande."""
        mock_api = Mock()
        mock_station = Mock()

        cmd = RefreshDataCommand(mock_api, mock_station)

        # Vérifier que la commande a été créée
        assert cmd is not None

    @patch('builtins.print')
    def test_execute(self, _mock_print):
        """Test l'exécution de la commande."""
        mock_api = Mock()
        mock_station = Mock()
        mock_station.nom = "Montaudran"
        mock_station.get_measurements.return_value = ["m1", "m2"]
        cmd = RefreshDataCommand(mock_api, mock_station)

        result = cmd.execute()

        mock_station.clear_measurements.assert_called_once()
        mock_api.fetch_data_for_station.assert_called_once_with(mock_station)
        assert result == ["m1", "m2"]


class TestDisplayMeasurementsCommand:
    """Tests pour DisplayMeasurementsCommand."""

    def test_command_creation(self):
        """Test la création de la commande."""
        mock_station = Mock()

        cmd = DisplayMeasurementsCommand(mock_station)

        # Vérifier que la commande a été créée
        assert cmd is not None

    def test_execute(self):
        """Test l'exécution de la commande."""
        mock_station = Mock()
        mock_station.get_measurements.return_value = ["m1", "m2", "m3"]
        cmd = DisplayMeasurementsCommand(mock_station)

        result = cmd.execute()

        mock_station.get_measurements.assert_called_once()
        assert result == ["m1", "m2", "m3"]


class TestAddCountryCommand:
    """Tests pour AddCountryCommand."""

    def test_command_creation(self):
        """Test la création de la commande."""
        mock_config = Mock()

        cmd = AddCountryCommand(mock_config, "fr001", "France")

        # Vérifier que la commande a été créée
        assert cmd is not None

    @patch('builtins.print')
    def test_execute(self, _mock_print):
        """Test l'exécution de la commande."""
        mock_config = Mock()
        cmd = AddCountryCommand(mock_config, "fr001", "France")

        cmd.execute()

        mock_config.add_pays.assert_called_once_with("fr001", "France")


class TestRemoveCountryCommand:
    """Tests pour RemoveCountryCommand."""

    def test_command_creation(self):
        """Test la création de la commande."""
        mock_config = Mock()

        cmd = RemoveCountryCommand(mock_config, "fr001")

        # Vérifier que la commande a été créée
        assert cmd is not None

    @patch('builtins.print')
    def test_execute_success(self, _mock_print):
        """Test l'exécution réussie de la commande."""
        mock_config = Mock()
        mock_config.remove_pays.return_value = True
        cmd = RemoveCountryCommand(mock_config, "fr001")

        cmd.execute()

        mock_config.remove_pays.assert_called_once_with("fr001")

    @patch('builtins.print')
    def test_execute_failure(self, _mock_print):
        """Test l'exécution échouée de la commande."""
        mock_config = Mock()
        mock_config.remove_pays.return_value = False
        cmd = RemoveCountryCommand(mock_config, "fr001")

        cmd.execute()

        mock_config.remove_pays.assert_called_once_with("fr001")


class TestAddCityCommand:
    """Tests pour AddCityCommand."""

    def test_command_creation(self):
        """Test la création de la commande."""
        mock_config = Mock()

        cmd = AddCityCommand(mock_config, "v001", "Toulouse", "fr001")

        # Vérifier que la commande a été créée
        assert cmd is not None

    @patch('builtins.print')
    def test_execute(self, _mock_print):
        """Test l'exécution de la commande."""
        mock_config = Mock()
        cmd = AddCityCommand(mock_config, "v001", "Toulouse", "fr001")

        cmd.execute()

        mock_config.add_ville.assert_called_once_with("v001", "Toulouse", "fr001")


class TestRemoveCityCommand:
    """Tests pour RemoveCityCommand."""

    def test_command_creation(self):
        """Test la création de la commande."""
        mock_config = Mock()

        cmd = RemoveCityCommand(mock_config, "v001")

        # Vérifier que la commande a été créée
        assert cmd is not None

    @patch('builtins.print')
    def test_execute_success(self, _mock_print):
        """Test l'exécution réussie de la commande."""
        mock_config = Mock()
        mock_config.remove_ville.return_value = True
        cmd = RemoveCityCommand(mock_config, "v001")

        cmd.execute()

        mock_config.remove_ville.assert_called_once_with("v001")

    @patch('builtins.print')
    def test_execute_failure(self, _mock_print):
        """Test l'exécution échouée de la commande."""
        mock_config = Mock()
        mock_config.remove_ville.return_value = False
        cmd = RemoveCityCommand(mock_config, "v001")

        cmd.execute()

        mock_config.remove_ville.assert_called_once_with("v001")


class TestAddStationCommand:
    """Tests pour AddStationCommand."""

    def test_command_creation(self):
        """Test la création de la commande."""
        mock_config = Mock()

        cmd = AddStationCommand(
            mock_config,
            "s001",
            "Montaudran",
            "v001",
            "https://api.com"
        )

        # Vérifier que la commande a été créée
        assert cmd is not None

    @patch('builtins.print')
    def test_execute(self, _mock_print):
        """Test l'exécution de la commande."""
        mock_config = Mock()
        cmd = AddStationCommand(
            mock_config,
            "s001",
            "Montaudran",
            "v001",
            "https://api.com"
        )

        cmd.execute()

        mock_config.add_station.assert_called_once_with(
            "s001",
            "Montaudran",
            "v001",
            "https://api.com"
        )


class TestRemoveStationCommand:
    """Tests pour RemoveStationCommand."""

    def test_command_creation(self):
        """Test la création de la commande."""
        mock_config = Mock()

        cmd = RemoveStationCommand(mock_config, "s001")

        # Vérifier que la commande a été créée
        assert cmd is not None

    @patch('builtins.print')
    def test_execute_success(self, _mock_print):
        """Test l'exécution réussie de la commande."""
        mock_config = Mock()
        mock_config.remove_station.return_value = True
        cmd = RemoveStationCommand(mock_config, "s001")

        cmd.execute()

        mock_config.remove_station.assert_called_once_with("s001")

    @patch('builtins.print')
    def test_execute_failure(self, _mock_print):
        """Test l'exécution échouée de la commande."""
        mock_config = Mock()
        mock_config.remove_station.return_value = False
        cmd = RemoveStationCommand(mock_config, "s001")

        cmd.execute()

        mock_config.remove_station.assert_called_once_with("s001")


class TestUpdateStationUrlCommand:
    """Tests pour UpdateStationUrlCommand."""

    def test_command_creation(self):
        """Test la création de la commande."""
        mock_config = Mock()

        cmd = UpdateStationUrlCommand(mock_config, "s001", "https://new-api.com")

        # Vérifier que la commande a été créée
        assert cmd is not None

    @patch('builtins.print')
    def test_execute_success(self, _mock_print):
        """Test l'exécution réussie de la commande."""
        mock_config = Mock()
        mock_config.update_station_url.return_value = True
        cmd = UpdateStationUrlCommand(mock_config, "s001", "https://new-api.com")

        cmd.execute()

        mock_config.update_station_url.assert_called_once_with("s001", "https://new-api.com")

    @patch('builtins.print')
    def test_execute_failure(self, _mock_print):
        """Test l'exécution échouée de la commande."""
        mock_config = Mock()
        mock_config.update_station_url.return_value = False
        cmd = UpdateStationUrlCommand(mock_config, "s001", "https://new-api.com")

        cmd.execute()

        mock_config.update_station_url.assert_called_once_with("s001", "https://new-api.com")


class TestCommandIntegration:
    """Tests d'intégration des commandes."""

    def test_command_sequence_with_invoker(self):
        """Test une séquence de commandes avec l'invocateur."""
        invoker = CommandInvoker()
        mock_config = Mock()

        # Exécuter plusieurs commandes
        cmd1 = AddCountryCommand(mock_config, "fr001", "France")
        cmd2 = AddCityCommand(mock_config, "v001", "Toulouse", "fr001")
        cmd3 = AddStationCommand(mock_config, "s001", "Montaudran", "v001", "https://api.com")

        with patch('builtins.print'):
            invoker.execute_command(cmd1)
            invoker.execute_command(cmd2)
            invoker.execute_command(cmd3)

        # Vérifier l'historique
        history = invoker.get_history()
        assert len(history) == 3
        assert cmd1 in history
        assert cmd2 in history
        assert cmd3 in history
