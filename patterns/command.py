"""
Pattern Command pour encapsuler les actions utilisateur.
"""
from abc import ABC, abstractmethod
from typing import Any


class Command(ABC):
    """
    Interface pour toutes les commandes.
    Principe SOLID: Interface Segregation - interface simple et claire.
    """

    @abstractmethod
    def execute(self) -> Any:
        """Exécute la commande."""
        pass


class SelectStationCommand(Command):
    """Commande pour sélectionner une station."""

    def __init__(self, station_selector, station):
        self._station_selector = station_selector
        self._station = station

    def execute(self) -> Any:
        """Sélectionne la station."""
        self._station_selector.select_station(self._station)
        return self._station


class RefreshDataCommand(Command):
    """Commande pour rafraîchir les données d'une station."""

    def __init__(self, api_service, station):
        self._api_service = api_service
        self._station = station

    def execute(self) -> Any:
        """Rafraîchit les données de la station."""
        print(f"\n🔄 Rafraîchissement des données pour {self._station.nom}...")
        self._station.clear_measurements()
        self._api_service.fetch_data_for_station(self._station)
        return self._station.get_measurements()


class DisplayMeasurementsCommand(Command):
    """Commande pour afficher les mesures d'une station."""

    def __init__(self, station):
        self._station = station

    def execute(self) -> Any:
        """Affiche les mesures de la station."""
        return self._station.get_measurements()


class AddCountryCommand(Command):
    """Commande pour ajouter un pays."""

    def __init__(self, config, country_id: str, country_name: str):
        self._config = config
        self._country_id = country_id
        self._country_name = country_name

    def execute(self) -> Any:
        """Ajoute un pays."""
        self._config.add_pays(self._country_id, self._country_name)
        print(f"✅ Pays '{self._country_name}' ajouté avec succès.")


class RemoveCountryCommand(Command):
    """Commande pour supprimer un pays."""

    def __init__(self, config, country_id: str):
        self._config = config
        self._country_id = country_id

    def execute(self) -> Any:
        """Supprime un pays."""
        if self._config.remove_pays(self._country_id):
            print(f"✅ Pays supprimé avec succès.")
        else:
            print(f"❌ Pays non trouvé.")


class AddCityCommand(Command):
    """Commande pour ajouter une ville."""

    def __init__(self, config, city_id: str, city_name: str, country_id: str):
        self._config = config
        self._city_id = city_id
        self._city_name = city_name
        self._country_id = country_id

    def execute(self) -> Any:
        """Ajoute une ville."""
        self._config.add_ville(self._city_id, self._city_name, self._country_id)
        print(f"✅ Ville '{self._city_name}' ajoutée avec succès.")


class RemoveCityCommand(Command):
    """Commande pour supprimer une ville."""

    def __init__(self, config, city_id: str):
        self._config = config
        self._city_id = city_id

    def execute(self) -> Any:
        """Supprime une ville."""
        if self._config.remove_ville(self._city_id):
            print(f"✅ Ville supprimée avec succès.")
        else:
            print(f"❌ Ville non trouvée.")


class AddStationCommand(Command):
    """Commande pour ajouter une station."""

    def __init__(self, config, station_id: str, station_name: str,
                 city_id: str, api_url: str):
        self._config = config
        self._station_id = station_id
        self._station_name = station_name
        self._city_id = city_id
        self._api_url = api_url

    def execute(self) -> Any:
        """Ajoute une station."""
        self._config.add_station(self._station_id, self._station_name,
                                self._city_id, self._api_url)
        print(f"✅ Station '{self._station_name}' ajoutée avec succès.")


class RemoveStationCommand(Command):
    """Commande pour supprimer une station."""

    def __init__(self, config, station_id: str):
        self._config = config
        self._station_id = station_id

    def execute(self) -> Any:
        """Supprime une station."""
        if self._config.remove_station(self._station_id):
            print(f"✅ Station supprimée avec succès.")
        else:
            print(f"❌ Station non trouvée.")


class UpdateStationUrlCommand(Command):
    """Commande pour modifier l'URL d'une station."""

    def __init__(self, config, station_id: str, new_url: str):
        self._config = config
        self._station_id = station_id
        self._new_url = new_url

    def execute(self) -> Any:
        """Modifie l'URL de la station."""
        if self._config.update_station_url(self._station_id, self._new_url):
            print(f"✅ URL de la station mise à jour avec succès.")
        else:
            print(f"❌ Station non trouvée.")


class CommandInvoker:
    """
    Invocateur de commandes.
    Gère l'exécution des commandes.
    """

    def __init__(self):
        self._history = []

    def execute_command(self, command: Command) -> Any:
        """Exécute une commande et l'ajoute à l'historique."""
        result = command.execute()
        self._history.append(command)
        return result

    def get_history(self):
        """Retourne l'historique des commandes."""
        return self._history.copy()
