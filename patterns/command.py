from abc import ABC, abstractmethod


class Command(ABC):
    """Interface pour les commandes"""

    @abstractmethod
    def execute(self):
        """Exécute la commande"""
        pass


class SelectStationCommand(Command):
    """Commande pour sélectionner une station"""

    def __init__(self, app, station):
        self.app = app
        self.station = station

    def execute(self):
        """Sélectionne la station"""
        self.app.select_station(self.station)


class RefreshDataCommand(Command):
    """Commande pour rafraîchir les données"""

    def __init__(self, app, station=None):
        self.app = app
        self.station = station

    def execute(self):
        """Rafraîchit les données"""
        if self.station:
            self.app.refresh_station_data(self.station)
        else:
            self.app.refresh_all_stations()


class AddStationCommand(Command):
    """Commande pour ajouter une station"""

    def __init__(self, app):
        self.app = app

    def execute(self):
        """Ajoute une nouvelle station"""
        self.app.add_new_station()


class BackToMenuCommand(Command):
    """Commande pour revenir au menu"""

    def __init__(self, app):
        self.app = app

    def execute(self):
        """Retourne au menu principal"""
        self.app.show_main_menu()


class QuitCommand(Command):
    """Commande pour quitter l'application"""

    def __init__(self, app):
        self.app = app

    def execute(self):
        """Quitte l'application"""
        self.app.quit()


class ConfigMenuCommand(Command):
    """Commande pour ouvrir le menu de configuration"""

    def __init__(self, app):
        self.app = app

    def execute(self):
        """Ouvre le menu de configuration"""
        self.app.show_config_menu()
