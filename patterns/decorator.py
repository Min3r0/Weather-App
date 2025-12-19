"""
Pattern Decorator pour l'affichage des mesures.
"""
from functools import wraps
from typing import Callable, Any


def display_measurements_decorator(func: Callable) -> Callable:
    """
    Décorateur qui formate l'affichage des mesures météorologiques.
    Principe DRY: centralise la logique d'affichage.
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        result = func(*args, **kwargs)

        if result and isinstance(result, list):
            print("\n" + "=" * 80)
            print("📊 MESURES MÉTÉOROLOGIQUES".center(80))
            print("=" * 80)

            if not result:
                print("\n⚠️  Aucune mesure disponible.\n")
            else:
                print(f"\n📍 Nombre de mesures: {len(result)}\n")
                print("-" * 80)

                for i, measurement in enumerate(result[:20], 1):  # Limite à 20 pour la lisibilité
                    print(f"{i:2d}. {measurement}")

                if len(result) > 20:
                    print(f"\n... et {len(result) - 20} mesure(s) supplémentaire(s)")

                print("-" * 80)

            print()

        return result

    return wrapper


def execution_time_decorator(func: Callable) -> Callable:
    """
    Décorateur qui mesure le temps d'exécution d'une fonction.
    """
    import time

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
        except Exception as e:
            print(f"\n❌ Erreur lors de l'exécution: {str(e)}")
            return None

    return wrapper