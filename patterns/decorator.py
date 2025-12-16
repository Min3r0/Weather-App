from functools import wraps
from typing import Callable
import os


def clear_screen():
    """Nettoie l'écran du terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')


def display_measurements(func: Callable) -> Callable:
    """Décorateur pour afficher les mesures d'une station"""

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)

        # Récupère la station depuis le résultat
        station = result if result else kwargs.get('station')

        if station and station.measurements:
            clear_screen()
            self._display_station_measurements(station)
            input("\nAppuyez sur Entrée pour revenir au menu...")

        return result

    return wrapper
