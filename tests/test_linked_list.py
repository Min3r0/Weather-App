"""
Tests unitaires pour la Liste Chaînée.
Principe FIRST: Fast, Independent, Repeatable, Self-validating, Timely.
"""
import pytest
from weather_app.data_structures.linked_list import LinkedList, Node


class TestNode:
    """Tests pour la classe Node."""

    def test_node_creation(self):
        """Test la création d'un nœud."""
        node = Node("test_data")

        assert node.data == "test_data"
        assert node.next is None

    def test_node_with_different_data_types(self):
        """Test la création de nœuds avec différents types de données."""
        node_str = Node("string")
        node_int = Node(42)
        node_dict = Node({"key": "value"})

        assert node_str.data == "string"
        assert node_int.data == 42
        assert node_dict.data == {"key": "value"}


class TestLinkedList:
    """Tests pour la classe LinkedList."""

    def test_empty_list_creation(self):
        """Test la création d'une liste vide."""
        ll = LinkedList()

        assert ll.is_empty() is True
        assert ll.size() == 0
        assert len(ll) == 0

    def test_append_single_element(self):
        """Test l'ajout d'un seul élément."""
        ll = LinkedList()
        ll.append("first")

        assert ll.is_empty() is False
        assert ll.size() == 1
        assert ll.get(0) == "first"

    def test_append_multiple_elements(self):
        """Test l'ajout de plusieurs éléments."""
        ll = LinkedList()
        ll.append("first")
        ll.append("second")
        ll.append("third")

        assert ll.size() == 3
        assert ll.get(0) == "first"
        assert ll.get(1) == "second"
        assert ll.get(2) == "third"

    def test_get_valid_index(self):
        """Test la récupération d'un élément à un index valide."""
        ll = LinkedList()
        ll.append("a")
        ll.append("b")
        ll.append("c")

        assert ll.get(0) == "a"
        assert ll.get(1) == "b"
        assert ll.get(2) == "c"

    def test_get_invalid_index_raises_error(self):
        """Test que get lève une erreur pour un index invalide."""
        ll = LinkedList()
        ll.append("test")

        with pytest.raises(IndexError):
            ll.get(-1)

        with pytest.raises(IndexError):
            ll.get(5)

    def test_remove_first_element(self):
        """Test la suppression du premier élément."""
        ll = LinkedList()
        ll.append("first")
        ll.append("second")
        ll.append("third")

        ll.remove(0)

        assert ll.size() == 2
        assert ll.get(0) == "second"
        assert ll.get(1) == "third"

    def test_remove_middle_element(self):
        """Test la suppression d'un élément au milieu."""
        ll = LinkedList()
        ll.append("first")
        ll.append("second")
        ll.append("third")

        ll.remove(1)

        assert ll.size() == 2
        assert ll.get(0) == "first"
        assert ll.get(1) == "third"

    def test_remove_last_element(self):
        """Test la suppression du dernier élément."""
        ll = LinkedList()
        ll.append("first")
        ll.append("second")
        ll.append("third")

        ll.remove(2)

        assert ll.size() == 2
        assert ll.get(0) == "first"
        assert ll.get(1) == "second"

    def test_remove_invalid_index_raises_error(self):
        """Test que remove lève une erreur pour un index invalide."""
        ll = LinkedList()
        ll.append("test")

        with pytest.raises(IndexError):
            ll.remove(-1)

        with pytest.raises(IndexError):
            ll.remove(5)

    def test_clear_list(self):
        """Test le vidage de la liste."""
        ll = LinkedList()
        ll.append("a")
        ll.append("b")
        ll.append("c")

        ll.clear()

        assert ll.is_empty() is True
        assert ll.size() == 0

    def test_iteration(self):
        """Test l'itération sur la liste."""
        ll = LinkedList()
        ll.append(1)
        ll.append(2)
        ll.append(3)

        result = list(ll)

        assert result == [1, 2, 3]

    def test_str_representation(self):
        """Test la représentation textuelle."""
        ll = LinkedList()
        ll.append("a")
        ll.append("b")

        result = str(ll)

        assert "LinkedList" in result
        assert "a" in result
        assert "b" in result

    def test_len_magic_method(self):
        """Test la méthode __len__."""
        ll = LinkedList()
        ll.append(1)
        ll.append(2)

        assert len(ll) == 2

    def test_empty_list_iteration(self):
        """Test l'itération sur une liste vide."""
        ll = LinkedList()

        result = list(ll)

        assert not result
