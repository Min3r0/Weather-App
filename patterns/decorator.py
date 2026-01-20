"""
Pattern Decorator pour l'affichage des mesures.
"""
import shutil
import time
from functools import wraps
from typing import Callable, Any
from datetime import datetime


def display_measurements_decorator(func: Callable) -> Callable:
    """
    Décorateur qui formate l'affichage des mesures météorologiques en colonnes.
    Principe DRY: centralise la logique d'affichage.
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        result = func(*args, **kwargs)

        if result and isinstance(result, list):
            _display_measurements_table(result)

        return result

    return wrapper


def _display_measurements_table(measurements: list) -> None:
    """Affiche les mesures sous forme de tableau en colonnes."""

    # Obtenir la taille du terminal
    terminal_width = shutil.get_terminal_size().columns

    # Largeur d'une colonne (ajustable)
    col_width = 18

    # Calculer le nombre de colonnes possibles
    # -2 pour les bordures, -1 pour l'espace entre colonnes
    available_width = terminal_width - 2
    num_columns = max(1, available_width // (col_width + 1))

    print("\n" + "=" * terminal_width)
    print("📊 MESURES MÉTÉOROLOGIQUES".center(terminal_width))
    print("=" * terminal_width)

    if not measurements:
        print("\n⚠️  Aucune mesure disponible.\n")
        return

    print(f"\n📍 Nombre total de mesures: {len(measurements)}\n")

    # Grouper les mesures par date
    measurements_by_date = {}
    for m in measurements:
        try:
            dt = datetime.fromisoformat(m.heure.replace('Z', '+00:00'))
            date_key = dt.strftime("%d/%m/%Y")
            if date_key not in measurements_by_date:
                measurements_by_date[date_key] = []
            measurements_by_date[date_key].append(m)
        except (ValueError, AttributeError):
            continue

    # Afficher chaque journée
    for date, day_measurements in sorted(measurements_by_date.items(), reverse=True):
        print("─" * terminal_width)
        print(f"📅 {date}".center(terminal_width))
        print("─" * terminal_width)

        # Afficher les mesures par groupes de colonnes
        total = len(day_measurements)
        for start_idx in range(0, total, num_columns):
            end_idx = min(start_idx + num_columns, total)
            chunk = day_measurements[start_idx:end_idx]

            _print_measurement_row(chunk, col_width, terminal_width)

            # Séparateur entre les groupes (sauf le dernier)
            if end_idx < total:
                print()

    print("=" * terminal_width)
    print()


def _print_measurement_row(measurements: list, col_width: int, terminal_width: int) -> None:
    """Affiche une ligne de mesures en colonnes."""

    # Préparer les données
    headers = []
    temps = []
    hums = []
    press = []

    for m in measurements:
        try:
            dt = datetime.fromisoformat(m.heure.replace('Z', '+00:00'))
            heure = dt.strftime("%Hh%M")
            headers.append(heure)
            temps.append(f"{m.temperature}°C")
            hums.append(f"{m.humidite}%")
            press.append(f"{m.pression} Pa")
        except (ValueError, AttributeError):
            headers.append("--:--")
            temps.append("--°C")
            hums.append("--%")
            press.append("-- Pa")

    # Afficher les lignes
    _print_line("Heure", headers, col_width, terminal_width)
    _print_line("Temp", temps, col_width, terminal_width)
    _print_line("Hum", hums, col_width, terminal_width)
    _print_line("Press", press, col_width, terminal_width)


def _print_line(label: str, values: list, col_width: int, terminal_width: int) -> None:
    """Affiche une ligne du tableau."""

    # Formater le label (8 caractères)
    formatted_label = f"{label:<8}"

    # Formater les valeurs
    formatted_values = []
    for val in values:
        # Centrer la valeur dans la colonne
        formatted_values.append(f"{val:^{col_width}}")

    # Construire la ligne
    line = formatted_label + " │ ".join(formatted_values)

    # Tronquer si nécessaire
    if len(line) > terminal_width:
        line = line[:terminal_width - 3] + "..."

    print(line)


def execution_time_decorator(func: Callable) -> Callable:
    """
    Décorateur qui mesure le temps d'exécution d'une fonction.
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()

        execution_time = end_time - start_time
        print(f"⏱️  Temps d'exécution: {execution_time:.3f}s")

        return result

    return wrapper


def error_handler_decorator(func: Callable) -> Callable:
    """
    Décorateur qui gère les erreurs de manière élégante.
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except (ValueError, TypeError, KeyError, AttributeError) as e:
            print(f"\n❌ Erreur lors de l'exécution: {str(e)}")
            return None

    return wrapper
