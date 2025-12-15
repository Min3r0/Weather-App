"""Point d'entrée principal de l'application météo."""
import sys
import os

# Ajouter le dossier parent au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.display import WeatherApp

def main():
    """Lance l'application météo."""
    app = WeatherApp()
    app.run()

if __name__ == "__main__":
    main()