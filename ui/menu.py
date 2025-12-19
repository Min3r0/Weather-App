"""
Interface utilisateur avec menus de navigation.
"""
import os
from typing import Optional
from config.singleton_config import ConfigurationSingleton
from services.api_service import ApiService
from patterns.observer import StationSelector, DataLoader
from patterns.command import (
    CommandInvoker, SelectStationCommand, RefreshDataCommand,
    DisplayMeasurementsCommand, AddCountryCommand, RemoveCountryCommand,
    AddCityCommand, RemoveCityCommand, AddStationCommand,
    RemoveStationCommand, UpdateStationUrlCommand
)
from patterns.decorator import display_measurements_decorator
from data_structures.linked_list import LinkedList
from models.location import Pays, Ville, Station
from models.builders import StationBuilder, VilleBuilder
import uuid


class MainMenu:
    """
    Menu principal de l'application.
    Principe KISS: interface simple et intuitive.
    """

    def __init__(self):
        self._config = ConfigurationSingleton()
        self._api_service = ApiService()
        self._station_selector = StationSelector()
        self._data_loader = DataLoader(self._api_service)
        self._station_selector.attach(self._data_loader)
        self._command_invoker = CommandInvoker()
        self._running = True

    def clear_screen(self) -> None:
        """Nettoie le terminal."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_header(self, title: str) -> None:
        """Affiche un en-tête formaté."""
        self.clear_screen()
        print("\n" + "=" * 80)
        print(f"🌤️  {title}".center(80))
        print("=" * 80 + "\n")

    def get_user_choice(self, prompt: str = "Entrez votre choix: ") -> str:
        """Récupère le choix de l'utilisateur."""
        return input(prompt).strip()

    def pause(self) -> None:
        """Met en pause pour que l'utilisateur puisse lire."""
        input("\nAppuyez sur Entrée pour continuer...")

    def run(self) -> None:
        """Lance l'application."""
        while self._running:
            self._show_main_menu()

    def _show_main_menu(self) -> None:
        """Affiche le menu principal."""
        self.display_header("MENU PRINCIPAL")
        print("1. Voir la météo")
        print("2. Configuration")
        print("0. Quitter le programme")

        choice = self.get_user_choice()

        if choice == "1":
            self._show_weather_menu()
        elif choice == "2":
            self._show_config_menu()
        elif choice == "0":
            self._running = False
            print("\n👋 Au revoir !")
        else:
            print("\n❌ Choix invalide.")
            self.pause()

    def _show_weather_menu(self) -> None:
        """Affiche le menu de sélection des stations météo."""
        self.display_header("SÉLECTION DE LA STATION MÉTÉO")

        # Charger les stations depuis la configuration
        stations_list = self._load_stations_to_linked_list()

        if stations_list.is_empty():
            print("⚠️  Aucune station configurée.")
            print("\n💡 Veuillez d'abord ajouter des stations dans la configuration.")
            self.pause()
            return

        print("0. Revenir au menu principal")

        for i, station in enumerate(stations_list, 1):
            ville_name = self._get_ville_name(station)
            print(f"{i}. {ville_name} - {station.nom}")

        choice = self.get_user_choice("\nEntrez un numéro: ")

        if choice == "0":
            return

        try:
            index = int(choice) - 1
            if 0 <= index < len(stations_list):
                station = stations_list.get(index)
                self._show_station_details(station)
            else:
                print("\n❌ Numéro invalide.")
                self.pause()
        except ValueError:
            print("\n❌ Veuillez entrer un numéro valide.")
            self.pause()

    def _show_station_details(self, station: Station) -> None:
        """Affiche les détails et mesures d'une station."""
        # Utiliser le pattern Command pour sélectionner la station
        command = SelectStationCommand(self._station_selector, station)
        self._command_invoker.execute_command(command)

        while True:
            self.display_header(f"STATION: {station.nom}")
            print(f"📍 Ville: {self._get_ville_name(station)}")
            print(f"🌍 Pays: {self._get_pays_name(station)}")
            print(f"📊 Mesures: {len(station.get_measurements())}\n")

            print("1. Afficher les mesures")
            print("2. Rafraîchir les données")
            print("0. Retour")

            choice = self.get_user_choice()

            if choice == "1":
                self._display_station_measurements(station)
            elif choice == "2":
                self._refresh_station_data(station)
            elif choice == "0":
                break
            else:
                print("\n❌ Choix invalide.")
                self.pause()

    @display_measurements_decorator
    def _display_station_measurements(self, station: Station):
        """Affiche les mesures avec le décorateur."""
        command = DisplayMeasurementsCommand(station)
        measurements = self._command_invoker.execute_command(command)
        self.pause()
        return measurements

    def _refresh_station_data(self, station: Station) -> None:
        """Rafraîchit les données d'une station."""
        command = RefreshDataCommand(self._api_service, station)
        self._command_invoker.execute_command(command)
        self.pause()

    def _show_config_menu(self) -> None:
        """Affiche le menu de configuration."""
        while True:
            self.display_header("CONFIGURATION")
            print("1. Gérer les pays")
            print("2. Gérer les villes")
            print("3. Gérer les stations")
            print("0. Revenir au menu principal")

            choice = self.get_user_choice()

            if choice == "1":
                self._show_countries_menu()
            elif choice == "2":
                self._show_cities_menu()
            elif choice == "3":
                self._show_stations_menu()
            elif choice == "0":
                break
            else:
                print("\n❌ Choix invalide.")
                self.pause()

    def _show_countries_menu(self) -> None:
        """Menu de gestion des pays."""
        while True:
            self.display_header("GESTION DES PAYS")
            print("1. Lister les pays")
            print("2. Ajouter un pays")
            print("3. Supprimer un pays")
            print("0. Retour")

            choice = self.get_user_choice()

            if choice == "1":
                self._list_countries()
            elif choice == "2":
                self._add_country()
            elif choice == "3":
                self._remove_country()
            elif choice == "0":
                break
            else:
                print("\n❌ Choix invalide.")
                self.pause()

    def _list_countries(self) -> None:
        """Liste tous les pays."""
        self.display_header("LISTE DES PAYS")
        pays = self._config.get_pays()

        if not pays:
            print("⚠️  Aucun pays configuré.")
        else:
            for pays_id, pays_data in pays.items():
                villes_count = len(self._config.get_villes(pays_id))
                print(f"• {pays_data['nom']} (ID: {pays_id}) - {villes_count} ville(s)")

        self.pause()

    def _add_country(self) -> None:
        """Ajoute un nouveau pays."""
        self.display_header("AJOUTER UN PAYS")
        nom = input("Nom du pays: ").strip()

        if nom:
            pays_id = str(uuid.uuid4())[:8]
            command = AddCountryCommand(self._config, pays_id, nom)
            self._command_invoker.execute_command(command)
        else:
            print("\n❌ Le nom ne peut pas être vide.")

        self.pause()

    def _remove_country(self) -> None:
        """Supprime un pays."""
        self.display_header("SUPPRIMER UN PAYS")
        self._list_countries()

        pays_id = input("\nID du pays à supprimer: ").strip()

        if pays_id:
            confirmation = input(f"⚠️  Confirmer la suppression (o/n)? ").lower()
            if confirmation == 'o':
                command = RemoveCountryCommand(self._config, pays_id)
                self._command_invoker.execute_command(command)

        self.pause()

    def _show_cities_menu(self) -> None:
        """Menu de gestion des villes."""
        while True:
            self.display_header("GESTION DES VILLES")
            print("1. Lister les villes")
            print("2. Ajouter une ville")
            print("3. Supprimer une ville")
            print("0. Retour")

            choice = self.get_user_choice()

            if choice == "1":
                self._list_cities()
            elif choice == "2":
                self._add_city()
            elif choice == "3":
                self._remove_city()
            elif choice == "0":
                break
            else:
                print("\n❌ Choix invalide.")
                self.pause()

    def _list_cities(self) -> None:
        """Liste toutes les villes."""
        self.display_header("LISTE DES VILLES")
        villes = self._config.get_villes()
        pays_dict = self._config.get_pays()

        if not villes:
            print("⚠️  Aucune ville configurée.")
        else:
            for ville_id, ville_data in villes.items():
                pays_name = pays_dict.get(ville_data['pays_id'], {}).get('nom', 'Inconnu')
                stations_count = len(self._config.get_stations(ville_id))
                print(f"• {ville_data['nom']} ({pays_name}) "
                      f"(ID: {ville_id}) - {stations_count} station(s)")

        self.pause()

    def _add_city(self) -> None:
        """Ajoute une nouvelle ville."""
        self.display_header("AJOUTER UNE VILLE")

        pays_dict = self._config.get_pays()
        if not pays_dict:
            print("⚠️  Aucun pays configuré. Veuillez d'abord ajouter un pays.")
            self.pause()
            return

        print("Pays disponibles:")
        for pays_id, pays_data in pays_dict.items():
            print(f"  {pays_id}: {pays_data['nom']}")

        pays_id = input("\nID du pays: ").strip()
        if pays_id not in pays_dict:
            print("\n❌ Pays non trouvé.")
            self.pause()
            return

        nom = input("Nom de la ville: ").strip()

        if nom:
            ville_id = str(uuid.uuid4())[:8]
            command = AddCityCommand(self._config, ville_id, nom, pays_id)
            self._command_invoker.execute_command(command)
        else:
            print("\n❌ Le nom ne peut pas être vide.")

        self.pause()

    def _remove_city(self) -> None:
        """Supprime une ville."""
        self.display_header("SUPPRIMER UNE VILLE")
        self._list_cities()

        ville_id = input("\nID de la ville à supprimer: ").strip()

        if ville_id:
            confirmation = input(f"⚠️  Confirmer la suppression (o/n)? ").lower()
            if confirmation == 'o':
                command = RemoveCityCommand(self._config, ville_id)
                self._command_invoker.execute_command(command)

        self.pause()

    def _show_stations_menu(self) -> None:
        """Menu de gestion des stations."""
        while True:
            self.display_header("GESTION DES STATIONS")
            print("1. Lister les stations")
            print("2. Ajouter une station")
            print("3. Modifier l'URL d'une station")
            print("4. Supprimer une station")
            print("0. Retour")

            choice = self.get_user_choice()

            if choice == "1":
                self._list_stations()
            elif choice == "2":
                self._add_station()
            elif choice == "3":
                self._update_station_url()
            elif choice == "4":
                self._remove_station()
            elif choice == "0":
                break
            else:
                print("\n❌ Choix invalide.")
                self.pause()

    def _list_stations(self) -> None:
        """Liste toutes les stations."""
        self.display_header("LISTE DES STATIONS")
        stations = self._config.get_stations()

        if not stations:
            print("⚠️  Aucune station configurée.")
        else:
            villes_dict = self._config.get_villes()
            pays_dict = self._config.get_pays()

            for station_id, station_data in stations.items():
                ville = villes_dict.get(station_data['ville_id'], {})
                ville_nom = ville.get('nom', 'Inconnu')
                pays_nom = pays_dict.get(ville.get('pays_id', ''), {}).get('nom', 'Inconnu')

                print(f"\n• {station_data['nom']}")
                print(f"  ID: {station_id}")
                print(f"  Ville: {ville_nom} ({pays_nom})")
                print(f"  URL: {station_data['api_url'][:60]}...")

        self.pause()

    def _add_station(self) -> None:
        """Ajoute une nouvelle station avec le Builder pattern."""
        self.display_header("AJOUTER UNE STATION")

        villes_dict = self._config.get_villes()
        if not villes_dict:
            print("⚠️  Aucune ville configurée. Veuillez d'abord ajouter une ville.")
            self.pause()
            return

        print("Villes disponibles:")
        pays_dict = self._config.get_pays()
        for ville_id, ville_data in villes_dict.items():
            pays_nom = pays_dict.get(ville_data['pays_id'], {}).get('nom', 'Inconnu')
            print(f"  {ville_id}: {ville_data['nom']} ({pays_nom})")

        ville_id = input("\nID de la ville: ").strip()
        if ville_id not in villes_dict:
            print("\n❌ Ville non trouvée.")
            self.pause()
            return

        nom = input("Nom de la station: ").strip()
        api_url = input("URL de l'API: ").strip()

        if nom and api_url:
            # Test de l'URL
            print("\n🔍 Test de l'URL...")
            if self._api_service.test_api_url(api_url):
                station_id = str(uuid.uuid4())[:8]
                command = AddStationCommand(self._config, station_id, nom, ville_id, api_url)
                self._command_invoker.execute_command(command)
            else:
                print("⚠️  L'URL ne semble pas valide, mais la station sera ajoutée quand même.")
                station_id = str(uuid.uuid4())[:8]
                command = AddStationCommand(self._config, station_id, nom, ville_id, api_url)
                self._command_invoker.execute_command(command)
        else:
            print("\n❌ Tous les champs sont obligatoires.")

        self.pause()

    def _update_station_url(self) -> None:
        """Modifie l'URL d'une station."""
        self.display_header("MODIFIER L'URL D'UNE STATION")
        self._list_stations()

        station_id = input("\nID de la station: ").strip()

        if station_id in self._config.get_stations():
            new_url = input("Nouvelle URL de l'API: ").strip()

            if new_url:
                command = UpdateStationUrlCommand(self._config, station_id, new_url)
                self._command_invoker.execute_command(command)
            else:
                print("\n❌ L'URL ne peut pas être vide.")
        else:
            print("\n❌ Station non trouvée.")

        self.pause()

    def _remove_station(self) -> None:
        """Supprime une station."""
        self.display_header("SUPPRIMER UNE STATION")
        self._list_stations()

        station_id = input("\nID de la station à supprimer: ").strip()

        if station_id:
            confirmation = input(f"⚠️  Confirmer la suppression (o/n)? ").lower()
            if confirmation == 'o':
                command = RemoveStationCommand(self._config, station_id)
                self._command_invoker.execute_command(command)

        self.pause()

    def _load_stations_to_linked_list(self) -> LinkedList:
        """Charge les stations dans une liste chaînée depuis la configuration."""
        stations_list = LinkedList()

        # Caches locaux pour cette session de chargement
        pays_cache = {}
        villes_cache = {}

        # Charger depuis la configuration
        pays_dict = self._config.get_pays()
        villes_dict = self._config.get_villes()
        stations_dict = self._config.get_stations()

        # Créer les objets Pays
        for pays_id, pays_data in pays_dict.items():
            pays_cache[pays_id] = Pays(pays_id, pays_data['nom'])

        # Créer les objets Ville
        for ville_id, ville_data in villes_dict.items():
            pays = pays_cache.get(ville_data['pays_id'])
            if pays:
                villes_cache[ville_id] = Ville(ville_id, ville_data['nom'], pays)

        # Créer les objets Station avec le Builder
        for station_id, station_data in stations_dict.items():
            ville = villes_cache.get(station_data['ville_id'])
            if ville:
                try:
                    builder = StationBuilder()
                    station = (builder
                             .set_id(station_id)
                             .set_nom(station_data['nom'])
                             .set_ville(ville)
                             .set_api_url(station_data['api_url'])
                             .build())
                    stations_list.append(station)
                except ValueError as e:
                    print(f"⚠️  Erreur lors de la création de la station: {e}")

        return stations_list

    def _get_ville_name(self, station: Station) -> str:
        """Récupère le nom de la ville d'une station."""
        return station.ville.nom if station.ville else "Inconnu"

    def _get_pays_name(self, station: Station) -> str:
        """Récupère le nom du pays d'une station."""
        return station.ville.pays.nom if station.ville and station.ville.pays else "Inconnu"