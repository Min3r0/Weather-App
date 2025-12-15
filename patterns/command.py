"""Pattern Command pour les actions utilisateur."""
from abc import ABC, abstractmethod
from typing import Any


class Command(ABC):
    """Interface pour le pattern Command."""

    @abstractmethod
    def execute(self) -> Any:
        """Exécute la commande."""
        pass


class SelectStationCommand(Command):
    """Commande pour sélectionner une station."""

    def __init__(self, app, station_index: int):
        self.app = app
        self.station_index = station_index

    def execute(self):
        """Sélectionne la station."""
        return self.app.select_station(self.station_index)


class RefreshDataCommand(Command):
    """Commande pour rafraîchir les données."""

    def __init__(self, app, station=None):
        self.app = app
        self.station = station

    def execute(self):
        """Rafraîchit les données."""
        if self.station:
            return self.app.refresh_station_data(self.station)
        else:
            return self.app.refresh_all_stations()


class QuitCommand(Command):
    """Commande pour quitter l'application."""

    def __init__(self, app):
        self.app = app

    def execute(self):
        """Quitte l'application."""
        self.app.quit()


class BackToMenuCommand(Command):
    """Commande pour revenir au menu."""

    def __init__(self, app):
        self.app = app

    def execute(self):
        """Retourne au menu principal."""
        self.app.back_to_menu()


class UpdateStationURLCommand(Command):
    """Commande pour modifier l'URL d'une station."""

    def __init__(self, app, station):
        self.app = app
        self.station = station

    def execute(self):
        """Modifie l'URL de la station."""
        return self.app.update_station_url(self.station)