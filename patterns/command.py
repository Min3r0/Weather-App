"""
Pattern Command pour encapsuler les actions utilisateur.

Note: Les classes Command ont intentionnellement une seule méthode (pattern design).
Les warnings pylint R0903, R0913, R0917 sont désactivés pour ce fichier.
"""

# pylint: disable=too-few-public-methods
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments

from abc import ABC, abstractmethod
from typing import Any


class Command(ABC):
    """
    Interface pour toutes les commandes.
    """

    @abstractmethod
    def execute(self) -> Any:
        """Exécute la commande."""
        raise NotImplementedError


class SelectStationCommand(Command):
    """Commande pour sélectionner une station."""

    def __init__(self, station_selector, station):
        """
        Args:
            station_selector: Le sélecteur de station
            station: La station à sélectionner
        """
        self._station_selector = station_selector
        self._station = station

    def execute(self) -> Any:
        """Sélectionne la station."""
        self._station_selector.select_station(self._station)
        return self._station


class RefreshDataCommand(Command):
    """Commande pour rafraîchir les données d'une station."""

    def __init__(self, api_service, station):
        """
        Args:
            api_service: Le service API
            station: La station à rafraîchir
        """
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
        """
        Args:
            station: La station dont afficher les mesures
        """
        self._station = station

    def execute(self) -> Any:
        """Affiche les mesures de la station."""
        return self._station.get_measurements()


class AddCountryCommand(Command):
    """Commande pour ajouter un pays."""

    def __init__(self, config, country_id: str, country_name: str):
        """
        Args:
            config: La configuration
            country_id: L'identifiant du pays
            country_name: Le nom du pays
        """
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
        """
        Args:
            config: La configuration
            country_id: L'identifiant du pays à supprimer
        """
        self._config = config
        self._country_id = country_id

    def execute(self) -> Any:
        """Supprime un pays."""
        if self._config.remove_pays(self._country_id):
            print("✅ Pays supprimé avec succès.")
        else:
            print("❌ Pays non trouvé.")


class AddCityCommand(Command):
    """Commande pour ajouter une ville."""

    def __init__(self, config, city_id: str, city_name: str, country_id: str):
        """
        Args:
            config: La configuration
            city_id: L'identifiant de la ville
            city_name: Le nom de la ville
            country_id: L'identifiant du pays
        """
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
        """
        Args:
            config: La configuration
            city_id: L'identifiant de la ville à supprimer
        """
        self._config = config
        self._city_id = city_id

    def execute(self) -> Any:
        """Supprime une ville."""
        if self._config.remove_ville(self._city_id):
            print("✅ Ville supprimée avec succès.")
        else:
            print("❌ Ville non trouvée.")


class AddStationCommand(Command):
    """Commande pour ajouter une station."""

    def __init__(
            self,
            config,
            station_id: str,
            station_name: str,
            city_id: str,
            api_url: str
    ):
        """
        Args:
            config: La configuration
            station_id: L'identifiant de la station
            station_name: Le nom de la station
            city_id: L'identifiant de la ville
            api_url: L'URL de l'API
        """
        self._config = config
        self._station_id = station_id
        self._station_name = station_name
        self._city_id = city_id
        self._api_url = api_url

    def execute(self) -> Any:
        """Ajoute une station."""
        self._config.add_station(
            self._station_id,
            self._station_name,
            self._city_id,
            self._api_url
        )
        print(f"✅ Station '{self._station_name}' ajoutée avec succès.")


class RemoveStationCommand(Command):
    """Commande pour supprimer une station."""

    def __init__(self, config, station_id: str):
        """
        Args:
            config: La configuration
            station_id: L'identifiant de la station à supprimer
        """
        self._config = config
        self._station_id = station_id

    def execute(self) -> Any:
        """Supprime une station."""
        if self._config.remove_station(self._station_id):
            print("✅ Station supprimée avec succès.")
        else:
            print("❌ Station non trouvée.")


class UpdateStationUrlCommand(Command):
    """Commande pour modifier l'URL d'une station."""

    def __init__(self, config, station_id: str, new_url: str):
        """
        Args:
            config: La configuration
            station_id: L'identifiant de la station
            new_url: La nouvelle URL
        """
        self._config = config
        self._station_id = station_id
        self._new_url = new_url

    def execute(self) -> Any:
        """Modifie l'URL de la station."""
        if self._config.update_station_url(self._station_id, self._new_url):
            print("✅ URL de la station mise à jour avec succès.")
        else:
            print("❌ Station non trouvée.")


class CommandInvoker:
    """
    Invocateur de commandes.
    Gère l'exécution des commandes.
    """

    def __init__(self):
        """Initialise l'invocateur avec un historique vide."""
        self._history = []

    def execute_command(self, command: Command) -> Any:
        """
        Args:
            command: La commande à exécuter

        Returns:
            Le résultat de l'exécution de la commande
        """
        result = command.execute()
        self._history.append(command)
        return result

    def get_history(self):
        """
        Returns:
            Liste des commandes exécutées
        """
        return self._history.copy()
