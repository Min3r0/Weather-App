"""
Pattern Observer pour gérer les événements de sélection de station.

Note: Les classes Observer ont intentionnellement peu de méthodes (pattern design).
"""
# pylint: disable=too-few-public-methods

from abc import ABC, abstractmethod
from typing import List, Any


class Observer(ABC):
    """Interface pour les observateurs."""

    @abstractmethod
    def update(self, subject: Any, *args, **kwargs) -> None:
        """
        Args:
            subject: Le sujet qui notifie
            *args: Arguments positionnels
            **kwargs: Arguments nommés
        """


class Subject:
    """
    Sujet observable qui notifie les observateurs.
    """

    def __init__(self):
        """Initialise le sujet avec une liste vide d'observateurs."""
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        """
        Args:
            observer: L'observateur à attacher
        """
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        """
        Args:
            observer: L'observateur à détacher
        """
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, *args, **kwargs) -> None:
        """
        Args:
            *args: Arguments positionnels à transmettre
            **kwargs: Arguments nommés à transmettre
        """
        for observer in self._observers:
            observer.update(self, *args, **kwargs)


class StationSelector(Subject):
    """
    Sélecteur de station qui notifie lors d'une sélection.
    Les observateurs chargeront alors les mesures.
    """

    def __init__(self):
        """Initialise le sélecteur sans station sélectionnée."""
        super().__init__()
        self._selected_station = None

    def select_station(self, station: Any) -> None:
        """
        Args:
            station: La station à sélectionner
        """
        self._selected_station = station
        self.notify(station=station)

    @property
    def selected_station(self):
        """
        Returns:
            La station actuellement sélectionnée
        """
        return self._selected_station


class DataLoader(Observer):
    """
    Observateur qui charge les données lorsqu'une station est sélectionnée.
    """

    def __init__(self, api_service):
        """
        Args:
            api_service: Le service API pour charger les données
        """
        self._api_service = api_service

    def update(self, subject: Any, *args, **kwargs) -> None:
        """
        Args:
            subject: Le sujet qui notifie (non utilisé)
            *args: Arguments positionnels (non utilisés)
            **kwargs: Arguments nommés contenant 'station'
        """
        station = kwargs.get('station')
        if station:
            print(f"\n🔄 Chargement des données pour {station.nom}...")
            self._api_service.fetch_data_for_station(station)
