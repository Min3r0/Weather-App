"""
Implémentation d'une Liste Chaînée pour l'affichage des stations.
"""
from typing import Optional, Any, Iterator


class Node:
    """
    Nœud d'une liste chaînée.

    Cette classe est une simple structure de données sans méthodes.
    """

    # pylint: disable=too-few-public-methods

    def __init__(self, data: Any):
        """
        Initialise un nœud.

        Args:
            data: Données stockées dans le nœud
        """
        self.data = data
        self.next: Optional['Node'] = None


class LinkedList:
    """
    Liste Chaînée pour stocker et afficher les stations.
    Principe YAGNI: implémente uniquement ce qui est nécessaire.
    """

    def __init__(self):
        """Initialise une liste chaînée vide."""
        self._head: Optional[Node] = None
        self._size: int = 0

    def append(self, data: Any) -> None:
        """
        Ajoute un élément à la fin de la liste.

        Args:
            data: Élément à ajouter
        """
        new_node = Node(data)

        if not self._head:
            self._head = new_node
        else:
            current = self._head
            while current.next:
                current = current.next
            current.next = new_node

        self._size += 1

    def get(self, index: int) -> Any:
        """
        Récupère un élément par son index.

        Args:
            index: Position de l'élément (commence à 0)

        Returns:
            L'élément à la position spécifiée

        Raises:
            IndexError: Si l'index est hors limites
        """
        if index < 0 or index >= self._size:
            raise IndexError("Index hors limites")

        current = self._head
        for _ in range(index):
            current = current.next

        return current.data

    def remove(self, index: int) -> None:
        """
        Supprime un élément par son index.

        Args:
            index: Position de l'élément à supprimer

        Raises:
            IndexError: Si l'index est hors limites
        """
        if index < 0 or index >= self._size:
            raise IndexError("Index hors limites")

        if index == 0:
            self._head = self._head.next
        else:
            current = self._head
            for _ in range(index - 1):
                current = current.next
            current.next = current.next.next

        self._size -= 1

    def is_empty(self) -> bool:
        """
        Vérifie si la liste est vide.

        Returns:
            True si la liste est vide, False sinon
        """
        return self._head is None

    def size(self) -> int:
        """
        Retourne la taille de la liste.

        Returns:
            Nombre d'éléments dans la liste
        """
        return self._size

    def clear(self) -> None:
        """Vide la liste."""
        self._head = None
        self._size = 0

    def __iter__(self) -> Iterator:
        """
        Permet l'itération sur la liste.

        Yields:
            Les données de chaque nœud
        """
        current = self._head
        while current:
            yield current.data
            current = current.next

    def __len__(self) -> int:
        """
        Retourne la longueur de la liste.

        Returns:
            Nombre d'éléments
        """
        return self._size

    def __str__(self) -> str:
        """
        Représentation textuelle de la liste.

        Returns:
            Chaîne représentant la liste
        """
        elements = [str(data) for data in self]
        return f"LinkedList([{', '.join(elements)}])"
