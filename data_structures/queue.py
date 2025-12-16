from collections import deque
from typing import Any, Optional


class Queue:
    """File (FIFO) pour gérer les requêtes API"""

    def __init__(self):
        self._items = deque()

    def enqueue(self, item: Any):
        """Ajoute un élément à la file"""
        self._items.append(item)

    def dequeue(self) -> Optional[Any]:
        """Retire et retourne le premier élément de la file"""
        if not self.is_empty():
            return self._items.popleft()
        return None

    def peek(self) -> Optional[Any]:
        """Retourne le premier élément sans le retirer"""
        if not self.is_empty():
            return self._items[0]
        return None

    def is_empty(self) -> bool:
        """Vérifie si la file est vide"""
        return len(self._items) == 0

    def size(self) -> int:
        """Retourne la taille de la file"""
        return len(self._items)

    def clear(self):
        """Vide la file"""
        self._items.clear()
