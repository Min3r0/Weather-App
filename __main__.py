"""
Point d'entrée de l'application météo.
"""
from weather_app.ui.menu import MainMenu


def main():
    """Lance l'application météo."""
    menu = MainMenu()
    menu.run()


if __name__ == "__main__":
    main()
