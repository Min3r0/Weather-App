"""Pattern Observer pour les notifications."""
from abc import ABC, abstractmethod
from typing import List


class Observer(ABC):
    """Interface pour le pattern Observer."""

    @abstractmethod
    def update(self, subject, *args, **kwargs):
        """Méthode appelée lors d'une notification."""
        pass


class Subject:
    """Sujet observable."""

    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer):
        """Attache un observateur."""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer):
        """Détache un observateur."""
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, *args, **kwargs):
        """Notifie tous les observateurs."""
        for observer in self._observers:
            observer.update(self, *args, **kwargs)


class StationObserver(Observer):
    """Observateur pour charger les mesures d'une station."""

    def __init__(self, api_service):
        self.api_service = api_service

    def update(self, subject, *args, **kwargs):
        """Charge les mesures lorsqu'une station est sélectionnée."""
        station = kwargs.get('station')
        if station:
            print(f"\nChargement des mesures pour {station.name}...")
            self.api_service.fetch_measurements(station)