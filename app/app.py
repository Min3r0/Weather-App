# app/app.py
from .menu_manager import MenuManager
from .config_manager import ConfigManager

class App:
    def __init__(self):
        self.config = ConfigManager()
        self.menu = MenuManager()
        # pour l'instant pas de domain/core chargés, on ajoutera plus tard
        self.running = True

    def run(self):
        # boucle principale simple
        while self.running:
            choice = self.menu.show_main_menu(default_city=self.config.get_default_city())
            if choice == "1":
                # afficher stations (sera implémenté plus tard)
                print("\n[Feature] List stations — coming soon.")
                input("Press Enter to continue...")
            elif choice == "2":
                print("\n[Feature] Show weather — coming soon.")
                input("Press Enter to continue...")
            elif choice == "3":
                # changer localisation (sera implémenté plus tard)
                print("\n[Feature] Change location — coming soon.")
                input("Press Enter to continue...")
            elif choice == "4":
                print("Bye 👋")
                self.running = False
            else:
                print("Invalid choice, try again.")
