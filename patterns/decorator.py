"""Pattern Decorator pour l'affichage des mesures."""
import os
import shutil
from typing import List, Dict
from models.measurement import Measurement


class MeasurementDisplayDecorator:
    """Décorateur pour afficher les mesures météo."""

    def __init__(self, station):
        self.station = station

    def display(self):
        """Affiche les mesures de la station groupées par date."""
        measurements_by_date = self.station.get_measurements_by_date()

        if not measurements_by_date:
            print("\nAucune mesure disponible pour cette station.")
            return

        # Obtenir la taille du terminal
        terminal_width = shutil.get_terminal_size().columns

        # Afficher chaque date séparément
        for date_key, measurements in measurements_by_date.items():
            self._display_date_section(measurements, terminal_width)
            print()  # Ligne vide entre les dates

    def _display_date_section(self, measurements: List[Measurement], terminal_width: int):
        """Affiche une section pour une date."""
        if not measurements:
            return

        # Largeur minimale par colonne (environ 13 caractères)
        col_width = 13
        max_cols = max(1, (terminal_width - 20) // col_width)

        # Date de référence (première mesure)
        date_str = measurements[0].get_date_str()

        print("=" * terminal_width)
        print(f"DATE: {date_str}".center(terminal_width))
        print("=" * terminal_width)

        # Afficher les mesures par groupes
        for i in range(0, len(measurements), max_cols):
            chunk = measurements[i:i + max_cols]
            self._display_chunk(chunk, col_width)
            print()  # Ligne vide entre les groupes

    def _display_chunk(self, measurements: List[Measurement], col_width: int):
        """Affiche un groupe de mesures."""
        # Ligne des heures
        times = [m.get_time_str() for m in measurements]
        print(f"{'Heure':<20}", end="")
        for time in times:
            print(f"{time:>{col_width}}", end="")
        print()

        # Ligne des températures
        temps = [f"{m.temperature}°C" for m in measurements]
        print(f"{'Température':<20}", end="")
        for temp in temps:
            print(f"{temp:>{col_width}}", end="")
        print()

        # Ligne des pressions (conversion en hPa)
        pressures = [f"{m.pressure/100:.1f}hPa" for m in measurements]
        print(f"{'Pression':<20}", end="")
        for pressure in pressures:
            print(f"{pressure:>{col_width}}", end="")
        print()

        # Ligne de l'humidité
        humidities = [f"{m.humidity}%" for m in measurements]
        print(f"{'Humidité':<20}", end="")
        for humidity in humidities:
            print(f"{humidity:>{col_width}}", end="")
        print()
