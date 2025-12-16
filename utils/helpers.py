import os

def clear_terminal():
    """Nettoie le terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def validate_url(url: str) -> bool:
    """Valide une URL"""
    return url.startswith('http://') or url.startswith('https://')
