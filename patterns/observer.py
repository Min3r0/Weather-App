"""
Pattern Observer pour gérer les événements de sélection de station.
"""
from abc import ABC, abstractmethod
from typing import List, Any


class Observer(ABC):
    """Interface pour les observateurs."""

    @abstractmethod
    def update(self, subject: Any, *args, **kwargs) -> None:
        """Méthode appelée lors d'une notification."""
        pass


class Subject:
    """
    Sujet observable qui notifie les observateurs.
    Principe SOLID: Dependency Inversion - dépend d'abstractions.
    """

    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        """Attache un observateur."""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        """Détache un observateur."""
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, *args, **kwargs) -> None:
        """Notifie tous les observateurs."""
        for observer in self._observers:
            observer.update(self, *args, **kwargs)


class StationSelector(Subject):
    """
    Sélecteur de station qui notifie lors d'une sélection.
    Les observateurs chargeront alors les mesures.
    """

    def __init__(self):
        super().__init__()
        self._selected_station = None

    def select_station(self, station: Any) -> None:
        """Sélectionne une station et notifie les observateurs."""
        self._selected_station = station
        self.notify(station=station)

    @property
    def selected_station(self):
        """Retourne la station sélectionnée."""
        return self._selected_station


class DataLoader(Observer):
    """
    Observateur qui charge les données lorsqu'une station est sélectionnée.
    """

    def __init__(self, api_service):
        self._api_service = api_service

    def update(self, subject: Any, *args, **kwargs) -> None:
        """Charge les données de la station sélectionnée."""
        station = kwargs.get('station')
        if station:
            print(f"\n🔄 Chargement des données pour {station.nom}...")
            self._api_service.fetch_data_for_station(station)