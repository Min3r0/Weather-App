from typing import Optional, Any


class Node:
    """Nœud d'une liste chaînée"""

    def __init__(self, data: Any):
        self.data = data
        self.next: Optional['Node'] = None


class LinkedList:
    """Liste chaînée pour stocker les stations"""

    def __init__(self):
        self.head: Optional[Node] = None
        self._size = 0

    def append(self, data: Any):
        """Ajoute un élément à la fin de la liste"""
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self._size += 1

    def get(self, index: int) -> Optional[Any]:
        """Récupère un élément par index"""
        if index < 0 or index >= self._size:
            return None
        current = self.head
        for _ in range(index):
            current = current.next
        return current.data if current else None

    def size(self) -> int:
        """Retourne la taille de la liste"""
        return self._size

    def clear(self):
        """Vide la liste"""
        self.head = None
        self._size = 0

    def __iter__(self):
        """Permet l'itération sur la liste"""
        current = self.head
        while current:
            yield current.data
            current = current.next

    def __len__(self):
        return self._size
