import os
import shutil
from typing import Optional
from collections import defaultdict

from config.config_singleton import ConfigSingleton
from models.location import Pays, Ville, Station
from data_structures.linked_list import LinkedList
from services.api_service import APIService
from patterns.observer import Observer, StationSubject
from patterns.builder import StationBuilder
from patterns.command import (
    SelectStationCommand, RefreshDataCommand, AddStationCommand,
    BackToMenuCommand, QuitCommand, ConfigMenuCommand
)
from patterns.decorator import display_measurements, clear_screen


class MeasurementObserver(Observer):
    """Observateur qui charge les mesures quand une station est sélectionnée"""
    
    def __init__(self, api_service: APIService):
        self.api_service = api_service
    
    def update(self, subject: StationSubject):
        """Charge les mesures de la station sélectionnée"""
        if subject.selected_station:
            measurements = self.api_service.fetch_measurements(
                subject.selected_station.url
            )
            if measurements:
                subject.selected_station.set_measurements(measurements)


class WeatherApp:
    """Application principale de météo"""
    
    def __init__(self):
        self.config = ConfigSingleton()
        self.api_service = APIService()
        self.stations_list = LinkedList()
        self.station_subject = StationSubject()
        self.running = True
        self.current_station: Optional[Station] = None
        
        # Attache l'observateur
        observer = MeasurementObserver(self.api_service)
        self.station_subject.attach(observer)
        
        # Charge les stations
        self._load_stations()
    
    def _load_stations(self):
        """Charge les stations depuis la configuration"""
        self.stations_list.clear()
        pays_data = self.config.get_pays()
        
        for pays_nom, pays_info in pays_data.items():
            pays = Pays(pays_nom)
            
            for ville_nom, ville_info in pays_info.get("villes", {}).items():
                ville = Ville(ville_nom, pays)
                pays.add_ville(ville)
                
                for station_nom, station_info in ville_info.get("stations", {}).items():
                    station = Station(station_nom, ville, pays, station_info.get("url", ""))
                    ville.add_station(station)
                    self.stations_list.append(station)
    
    def run(self):
        """Boucle principale de l'application"""
        while self.running:
            self.show_main_menu()
    
    def show_main_menu(self):
        """Affiche le menu principal"""
        clear_screen()
        print("=== Sélection de la station météo ===\n")
        print("0. Quitter le programme")
        print("r. Rafraîchir les données")
        print("a. Ajouter une nouvelle station")
        print("c. Configuration (pays/villes/stations)\n")
        
        # Affiche les stations avec la liste chaînée
        for i, station in enumerate(self.stations_list, 1):
            print(f"{i}. {station.get_full_name()}")
        
        choice = input("\nEntrez un numéro : ").strip()
        
        if choice == '0':
            QuitCommand(self).execute()
        elif choice.lower() == 'r':
            RefreshDataCommand(self).execute()
        elif choice.lower() == 'a':
            AddStationCommand(self).execute()
        elif choice.lower() == 'c':
            ConfigMenuCommand(self).execute()
        elif choice.isdigit():
            index = int(choice) - 1
            station = self.stations_list.get(index)
            if station:
                SelectStationCommand(self, station).execute()
            else:
                input("Station invalide. Appuyez sur Entrée...")
        else:
            input("Choix invalide. Appuyez sur Entrée...")
    
    @display_measurements
    def select_station(self, station: Station) -> Station:
        """Sélectionne une station et charge ses données"""
        self.current_station = station
        self.station_subject.select_station(station)
        return station
    
    def _display_station_measurements(self, station: Station):
        """Affiche les mesures d'une station de manière formatée"""
        if not station.measurements:
            print("Aucune mesure disponible.")
            return
        
        # Obtient la largeur du terminal
        term_width = shutil.get_terminal_size().columns
        col_width = 12
        max_cols = max(1, (term_width - 20) // col_width)
        
        # Groupe les mesures par date
        measurements_by_date = defaultdict(list)
        for m in station.measurements:
            measurements_by_date[m.get_date_str()].append(m)
        
        print(f"\n{'='*80}")
        print(f"STATION: {station.get_full_name()}")
        print(f"{'='*80}\n")
        
        # Affiche chaque date
        for date_str in sorted(measurements_by_date.keys(), reverse=True):
            measures = measurements_by_date[date_str]
            
            print(f"{'='*80}")
            print(f"DATE: {date_str}")
            print(f"{'='*80}")
            
            # Affiche par groupe de colonnes
            for i in range(0, len(measures), max_cols):
                chunk = measures[i:i+max_cols]
                
                # Ligne des heures
                print(f"{'Heure':<20}", end='')
                for m in chunk:
                    print(f"{m.get_time_str():>12}", end='')
                print()
                
                # Ligne des températures
                print(f"{'Température':<20}", end='')
                for m in chunk:
                    print(f"{m.temperature:>10.1f}°C", end='')
                print()
                
                # Ligne des pressions
                print(f"{'Pression':<20}", end='')
                for m in chunk:
                    print(f"{m.pression/100:>9.1f}hPa", end='')
                print()
                
                # Ligne des humidités
                print(f"{'Humidité':<20}", end='')
                for m in chunk:
                    print(f"{m.humidite:>11}%", end='')
                print("\n")
    
    def refresh_station_data(self, station: Station):
        """Rafraîchit les données d'une station"""
        clear_screen()
        print(f"Rafraîchissement des données de {station.get_full_name()}...")
        measurements = self.api_service.fetch_measurements(station.url)
        if measurements:
            station.set_measurements(measurements)
            print("Données rafraîchies avec succès!")
        else:
            print("Échec du rafraîchissement des données.")
        input("\nAppuyez sur Entrée...")
    
    def refresh_all_stations(self):
        """Rafraîchit les données de toutes les stations"""
        clear_screen()
        print("Rafraîchissement de toutes les stations...")
        for station in self.stations_list:
            measurements = self.api_service.fetch_measurements(station.url)
            if measurements:
                station.set_measurements(measurements)
        print("Toutes les stations ont été rafraîchies!")
        input("\nAppuyez sur Entrée...")
    
    def add_new_station(self):
        """Ajoute une nouvelle station avec le Builder"""
        clear_screen()
        print("=== Ajout d'une nouvelle station ===\n")
        
        # Sélection du pays
        pays_data = self.config.get_pays()
        pays_list = list(pays_data.keys())
        
        print("Pays disponibles:")
        for i, pays_nom in enumerate(pays_list, 1):
            print(f"{i}. {pays_nom}")
        print("0. Créer un nouveau pays")
        
        choix = input("\nChoisissez un pays : ").strip()
        
        if choix == '0':
            pays_nom = input("Nom du nouveau pays : ").strip()
            if pays_nom:
                self.config.add_pays(pays_nom)
                pays = Pays(pays_nom)
            else:
                input("Nom invalide. Appuyez sur Entrée...")
                return
        elif choix.isdigit() and 0 < int(choix) <= len(pays_list):
            pays_nom = pays_list[int(choix) - 1]
            pays = Pays(pays_nom)
        else:
            input("Choix invalide. Appuyez sur Entrée...")
            return
        
        # Sélection de la ville
        villes_data = pays_data.get(pays_nom, {}).get("villes", {})
        villes_list = list(villes_data.keys())
        
        print("\nVilles disponibles:")
        for i, ville_nom in enumerate(villes_list, 1):
            print(f"{i}. {ville_nom}")
        print("0. Créer une nouvelle ville")
        
        choix = input("\nChoisissez une ville : ").strip()
        
        if choix == '0':
            ville_nom = input("Nom de la nouvelle ville : ").strip()
            if ville_nom:
                self.config.add_ville(pays_nom, ville_nom)
                ville = Ville(ville_nom, pays)
            else:
                input("Nom invalide. Appuyez sur Entrée...")
                return
        elif choix.isdigit() and 0 < int(choix) <= len(villes_list):
            ville_nom = villes_list[int(choix) - 1]
            ville = Ville(ville_nom, pays)
        else:
            input("Choix invalide. Appuyez sur Entrée...")
            return
        
        # Informations de la station
        station_nom = input("\nNom de la station : ").strip()
        if not station_nom:
            input("Nom invalide. Appuyez sur Entrée...")
            return
        
        url = input("URL de l'API : ").strip()
        if not url:
            input("URL invalide. Appuyez sur Entrée...")
            return
        
        # Utilise le Builder pour créer la station
        builder = StationBuilder()
        station = (builder
                  .set_nom(station_nom)
                  .set_pays(pays)
                  .set_ville(ville)
                  .set_url(url)
                  .build())
        
        # Recharge les stations
        self._load_stations()
        
        print(f"\nStation '{station.get_full_name()}' ajoutée avec succès!")
        input("\nAppuyez sur Entrée...")
    
    def show_config_menu(self):
        """Affiche le menu de configuration"""
        while True:
            clear_screen()
            print("=== Menu de Configuration ===\n")
            print("1. Ajouter un pays")
            print("2. Ajouter une ville")
            print("3. Supprimer un pays")
            print("4. Supprimer une ville")
            print("5. Supprimer une station")
            print("6. Modifier l'URL d'une station")
            print("0. Retour au menu principal\n")
            
            choice = input("Votre choix : ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                self._config_add_pays()
            elif choice == '2':
                self._config_add_ville()
            elif choice == '3':
                self._config_remove_pays()
            elif choice == '4':
                self._config_remove_ville()
            elif choice == '5':
                self._config_remove_station()
            elif choice == '6':
                self._config_update_url()
            else:
                input("Choix invalide. Appuyez sur Entrée...")
    
    def _config_add_pays(self):
        """Ajoute un pays"""
        clear_screen()
        nom = input("Nom du pays : ").strip()
        if nom:
            if self.config.add_pays(nom):
                print(f"Pays '{nom}' ajouté!")
            else:
                print("Le pays existe déjà.")
        input("\nAppuyez sur Entrée...")
    
    def _config_add_ville(self):
        """Ajoute une ville"""
        clear_screen()
        pays_list = list(self.config.get_pays().keys())
        if not pays_list:
            print("Aucun pays disponible.")
            input("\nAppuyez sur Entrée...")
            return
        
        for i, pays in enumerate(pays_list, 1):
            print(f"{i}. {pays}")
        
        choix = input("\nChoisissez un pays : ").strip()
        if choix.isdigit() and 0 < int(choix) <= len(pays_list):
            pays = pays_list[int(choix) - 1]
            ville = input("Nom de la ville : ").strip()
            if ville:
                if self.config.add_ville(pays, ville):
                    print(f"Ville '{ville}' ajoutée à '{pays}'!")
                else:
                    print("La ville existe déjà.")
        input("\nAppuyez sur Entrée...")
    
    def _config_remove_pays(self):
        """Supprime un pays"""
        clear_screen()
        pays_list = list(self.config.get_pays().keys())
        if not pays_list:
            print("Aucun pays disponible.")
            input("\nAppuyez sur Entrée...")
            return
        
        for i, pays in enumerate(pays_list, 1):
            print(f"{i}. {pays}")
        
        choix = input("\nChoisissez un pays à supprimer : ").strip()
        if choix.isdigit() and 0 < int(choix) <= len(pays_list):
            pays = pays_list[int(choix) - 1]
            confirm = input(f"Confirmer la suppression de '{pays}' ? (o/n) : ").strip().lower()
            if confirm == 'o':
                if self.config.remove_pays(pays):
                    self._load_stations()
                    print(f"Pays '{pays}' supprimé!")
        input("\nAppuyez sur Entrée...")
    
    def _config_remove_ville(self):
        """Supprime une ville"""
        clear_screen()
        pays_list = list(self.config.get_pays().keys())
        if not pays_list:
            print("Aucun pays disponible.")
            input("\nAppuyez sur Entrée...")
            return
        
        for i, pays in enumerate(pays_list, 1):
            print(f"{i}. {pays}")
        
        choix_pays = input("\nChoisissez un pays : ").strip()
        if choix_pays.isdigit() and 0 < int(choix_pays) <= len(pays_list):
            pays = pays_list[int(choix_pays) - 1]
            villes = list(self.config.get_pays()[pays].get("villes", {}).keys())
            
            if not villes:
                print("Aucune ville dans ce pays.")
                input("\nAppuyez sur Entrée...")
                return
            
            print(f"\nVilles de {pays}:")
            for i, ville in enumerate(villes, 1):
                print(f"{i}. {ville}")
            
            choix_ville = input("\nChoisissez une ville à supprimer : ").strip()
            if choix_ville.isdigit() and 0 < int(choix_ville) <= len(villes):
                ville = villes[int(choix_ville) - 1]
                confirm = input(f"Confirmer la suppression de '{ville}' ? (o/n) : ").strip().lower()
                if confirm == 'o':
                    if self.config.remove_ville(pays, ville):
                        self._load_stations()
                        print(f"Ville '{ville}' supprimée!")
        input("\nAppuyez sur Entrée...")
    
    def _config_remove_station(self):
        """Supprime une station"""
        clear_screen()
        if self.stations_list.size() == 0:
            print("Aucune station disponible.")
            input("\nAppuyez sur Entrée...")
            return
        
        for i, station in enumerate(self.stations_list, 1):
            print(f"{i}. {station.get_full_name()}")
        
        choix = input("\nChoisissez une station à supprimer : ").strip()
        if choix.isdigit():
            index = int(choix) - 1
            station = self.stations_list.get(index)
            if station:
                confirm = input(f"Confirmer la suppression de '{station.get_full_name()}' ? (o/n) : ").strip().lower()
                if confirm == 'o':
                    if self.config.remove_station(station.pays.nom, station.ville.nom, station.nom):
                        self._load_stations()
                        print(f"Station '{station.get_full_name()}' supprimée!")
        input("\nAppuyez sur Entrée...")
    
    def _config_update_url(self):
        """Modifie l'URL d'une station"""
        clear_screen()
        if self.stations_list.size() == 0:
            print("Aucune station disponible.")
            input("\nAppuyez sur Entrée...")
            return
        
        for i, station in enumerate(self.stations_list, 1):
            print(f"{i}. {station.get_full_name()}")
        
        choix = input("\nChoisissez une station : ").strip()
        if choix.isdigit():
            index = int(choix) - 1
            station = self.stations_list.get(index)
            if station:
                print(f"\nURL actuelle: {station.url}")
                new_url = input("Nouvelle URL : ").strip()
                if new_url:
                    if self.config.update_station_url(station.pays.nom, station.ville.nom, station.nom, new_url):
                        station.url = new_url
                        print("URL mise à jour!")
        input("\nAppuyez sur Entrée...")
    
    def quit(self):
        """Quitte l'application"""
        self.running = False
        clear_screen()
        print("Au revoir!")
