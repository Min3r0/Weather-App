# app/menu_manager.py
class MenuManager:
    def __init__(self):
        pass

    def show_main_menu(self, default_city: str = "Toulouse") -> str:
        """
        Affiche le menu principal et retourne le choix de l'utilisateur (string).
        On garde une API simple: retourne la chaîne entrée par l'utilisateur.
        """
        print("\n=== Weather Station App ===")
        print(f"Welcome to Weather Station for \"{default_city}\" (default)")
        print("1 - Show Stations")
        print("2 - Show Weather")
        print("3 - Change location")
        print("4 - Quit")
        return input("> ").strip()

    # plus tard on ajoutera d'autres méthodes: show_stations_menu(), show_add_station(), etc.
