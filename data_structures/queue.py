"""
Implémentation d'une File (Queue) pour les extractions API.
"""
from typing import Any, Optional
from collections import deque


class Queue:
    """
    File FIFO pour gérer les requêtes API.
    Principe KISS: implémentation simple avec deque.
    """

    def __init__(self):
        self._items = deque()

    def enqueue(self, item: Any) -> None:
        """Ajoute un élément à la fin de la file."""
        self._items.append(item)

    def dequeue(self) -> Any:
        """Retire et retourne le premier élément de la file."""
        if self.is_empty():
            raise IndexError("Impossible de retirer un élément d'une file vide")
        return self._items.popleft()

    def peek(self) -> Any:
        """Retourne le premier élément sans le retirer."""
        if self.is_empty():
            raise IndexError("La file est vide")
        return self._items[0]

    def is_empty(self) -> bool:
        """Vérifie si la file est vide."""
        return len(self._items) == 0

    def size(self) -> int:
        """Retourne la taille de la file."""
        return len(self._items)

    def clear(self) -> None:
        """Vide la file."""
        self._items.clear()

    def __len__(self) -> int:
        """Retourne la longueur de la file."""
        return len(self._items)

    def __str__(self) -> str:
        """Représentation textuelle de la file."""
        return f"Queue({list(self._items)})"

    def __repr__(self) -> str:
        return self.__str__()
