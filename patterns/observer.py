from abc import ABC, abstractmethod
from typing import List


class Observer(ABC):
    """Interface pour les observateurs"""

    @abstractmethod
    def update(self, subject: 'Subject'):
        """Méthode appelée lors d'une notification"""
        pass


class Subject:
    """Sujet observable"""

    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer):
        """Attache un observateur"""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer):
        """Détache un observateur"""
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self):
        """Notifie tous les observateurs"""
        for observer in self._observers:
            observer.update(self)


class StationSubject(Subject):
    """Sujet pour les stations - notifie lors de la sélection"""

    def __init__(self):
        super().__init__()
        self.selected_station = None

    def select_station(self, station):
        """Sélectionne une station et notifie les observateurs"""
        self.selected_station = station
        self.notify()
