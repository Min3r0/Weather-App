"""Interface utilisateur de l'application."""
import os
import sys
from config.config_singleton import ConfigSingleton
from models.linked_list import LinkedList
from models.station import Station
from patterns.builder import StationBuilder
from patterns.command import (SelectStationCommand, RefreshDataCommand,
                              QuitCommand, BackToMenuCommand, UpdateStationURLCommand)
from patterns.decorator import MeasurementDisplayDecorator
from patterns.observer import Subject, StationObserver
from services.api_service import APIService


class WeatherApp:
    """Application principale de météo."""

    def __init__(self):
        self.config = ConfigSingleton()
        self.stations = LinkedList()
        self.api_service = APIService()
        self.builder = StationBuilder()
        self.subject = Subject()
        self.running = True
        self.current_station = None

        # Attacher l'observateur
        station_observer = StationObserver(self.api_service)
        self.subject.attach(station_observer)

        # Charger les stations
        self._load_stations()

    def _load_stations(self):
        """Charge les stations depuis la configuration."""
        self.stations.clear()
        stations_data = self.config.get_all_stations()

        for station_data in stations_data:
            station = self.builder.reset() \
                .set_name(station_data['name']) \
                .set_url(station_data['url']) \
                .set_city(station_data['city']) \
                .set_country(station_data['country']) \
                .build()
            self.stations.append(station)

    def clear_screen(self):
        """Nettoie l'écran du terminal."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_menu(self):
        """Affiche le menu principal."""
        self.clear_screen()
        print("=== Sélection de la station météo ===\n")
        print("0. Quitter le programme")
        print("r. Rafraîchir toutes les données")
        print("a. Ajouter une nouvelle station")
        print("u. Modifier l'URL d'une station\n")

        stations_list = self.stations.to_list()
        for i, station in enumerate(stations_list, 1):
            print(f"{i}. {station.name}")
        print()

    def select_station(self, index: int):
        """Sélectionne une station et affiche ses mesures."""
        station = self.stations.get(index)
        if station:
            self.current_station = station
            # Notifier les observateurs (charge les mesures)
            self.subject.notify(station=station)
            self.display_station_data(station)

    def display_station_data(self, station: Station):
        """Affiche les données d'une station."""
        self.clear_screen()

        print(f"=== {station.name} ===")
        print(f"URL: {station.url}\n")

        # Utiliser le décorateur pour afficher
        decorator = MeasurementDisplayDecorator(station)
        decorator.display()

        print("\nOptions:")
        print("r - Rafraîchir les données")
        print("u - Modifier l'URL de cette station")
        print("m - Retour au menu")
        print("q - Quitter")

        choice = input("\nVotre choix: ").strip().lower()

        if choice == 'r':
            RefreshDataCommand(self, station).execute()
            self.display_station_data(station)
        elif choice == 'u':
            UpdateStationURLCommand(self, station).execute()
            self.display_station_data(station)
        elif choice == 'm':
            BackToMenuCommand(self).execute()
        elif choice == 'q':
            QuitCommand(self).execute()
        else:
            self.display_station_data(station)

    def refresh_station_data(self, station: Station):
        """Rafraîchit les données d'une station."""
        print(f"\nRafraîchissement de {station.name}...")
        self.api_service.fetch_measurements(station)
        print("Données rafraîchies!")

    def refresh_all_stations(self):
        """Rafraîchit les données de toutes les stations."""
        print("\nRafraîchissement de toutes les stations...")
        stations_list = self.stations.to_list()
        for station in stations_list:
            self.api_service.add_to_queue(station)
        self.api_service.process_queue()
        print("Toutes les données ont été rafraîchies!")
        input("\nAppuyez sur Entrée pour continuer...")

    def add_new_station(self):
        """Ajoute une nouvelle station."""
        self.clear_screen()
        print("=== Ajouter une nouvelle station ===\n")

        country = input("Pays: ").strip()
        city = input("Ville: ").strip()
        name = input("Nom de la station: ").strip()
        url = input("URL de l'API: ").strip()

        if all([country, city, name, url]):
            try:
                # Utiliser le builder
                station = self.builder.reset() \
                    .set_country(country) \
                    .set_city(city) \
                    .set_name(name) \
                    .set_url(url) \
                    .build()

                # Ajouter à la configuration
                self.config.add_station(country, city, name, url)

                # Recharger les stations
                self._load_stations()

                print("\nStation ajoutée avec succès!")
            except Exception as e:
                print(f"\nErreur: {e}")
        else:
            print("\nTous les champs sont obligatoires!")

        input("\nAppuyez sur Entrée pour continuer...")

    def update_station_url(self, station: Station):
        """Modifie l'URL d'une station."""
        self.clear_screen()
        print(f"=== Modifier l'URL de {station.name} ===\n")
        print(f"URL actuelle: {station.url}\n")

        new_url = input("Nouvelle URL (laissez vide pour annuler): ").strip()

        if new_url:
            # Mettre à jour dans la configuration
            if self.config.update_station_url(station.name, new_url):
                # Mettre à jour dans l'objet station
                station.update_url(new_url)
                # Recharger les stations pour synchroniser
                self._load_stations()
                # Trouver la station mise à jour
                updated_station = self.stations.find_by_name(station.name)
                if updated_station:
                    self.current_station = updated_station

                print("\nURL mise à jour avec succès!")
                print("Les données seront rechargées automatiquement.")
            else:
                print("\nErreur lors de la mise à jour de l'URL.")
        else:
            print("\nMise à jour annulée.")

        input("\nAppuyez sur Entrée pour continuer...")

    def back_to_menu(self):
        """Retourne au menu principal."""
        self.current_station = None

    def quit(self):
        """Quitte l'application."""
        self.running = False
        self.clear_screen()
        print("Au revoir!")
        sys.exit(0)

    def run(self):
        """Lance la boucle principale de l'application."""
        while self.running:
            self.display_menu()
            choice = input("Entrez un numéro: ").strip().lower()

            if choice == '0':
                QuitCommand(self).execute()
            elif choice == 'r':
                RefreshDataCommand(self).execute()
            elif choice == 'a':
                self.add_new_station()
            elif choice == 'u':
                self.update_station_url_menu()
            elif choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < self.stations.size():
                    SelectStationCommand(self, index).execute()
                else:
                    print("Numéro invalide!")
                    input("\nAppuyez sur Entrée pour continuer...")
            else:
                print("Choix invalide!")
                input("\nAppuyez sur Entrée pour continuer...")

    def update_station_url_menu(self):
        """Menu pour sélectionner une station à modifier."""
        self.clear_screen()
        print("=== Modifier l'URL d'une station ===\n")
        print("0. Annuler\n")

        stations_list = self.stations.to_list()
        for i, station in enumerate(stations_list, 1):
            print(f"{i}. {station.name}")

        choice = input("\nSélectionnez une station: ").strip()

        if choice.isdigit():
            if choice == '0':
                return

            index = int(choice) - 1
            if 0 <= index < self.stations.size():
                station = self.stations.get(index)
                if station:
                    self.update_station_url(station)
            else:
                print("Numéro invalide!")
                input("\nAppuyez sur Entrée pour continuer...")
        else:
            print("Choix invalide!")
            input("\nAppuyez sur Entrée pour continuer...")