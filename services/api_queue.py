"""File (Queue) pour gérer les extractions API."""
from collections import deque
from typing import Any, Optional


class APIQueue:
    """File pour gérer les requêtes API."""

    def __init__(self):
        self._queue = deque()

    def enqueue(self, item: Any):
        """Ajoute un élément à la file."""
        self._queue.append(item)

    def dequeue(self) -> Optional[Any]:
        """Retire et retourne le premier élément de la file."""
        if not self.is_empty():
            return self._queue.popleft()
        return None

    def is_empty(self) -> bool:
        """Vérifie si la file est vide."""
        return len(self._queue) == 0

    def size(self) -> int:
        """Retourne la taille de la file."""
        return len(self._queue)

    def clear(self):
        """Vide la file."""
        self._queue.clear()