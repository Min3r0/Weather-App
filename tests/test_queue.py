"""
Tests unitaires pour la File (Queue).
Principe AAA: Arrange, Act, Assert.
"""
import pytest
from weather_app.data_structures.queue import Queue


class TestQueue:
    """Tests pour la classe Queue."""

    def test_empty_queue_creation(self):
        """Test la création d'une file vide."""
        q = Queue()

        assert q.is_empty() is True
        assert q.size() == 0
        assert len(q) == 0

    def test_enqueue_single_item(self):
        """Test l'ajout d'un seul élément."""
        q = Queue()
        q.enqueue("item1")

        assert q.is_empty() is False
        assert q.size() == 1
        assert len(q) == 1

    def test_enqueue_multiple_items(self):
        """Test l'ajout de plusieurs éléments."""
        q = Queue()
        q.enqueue("item1")
        q.enqueue("item2")
        q.enqueue("item3")

        assert q.size() == 3

    def test_dequeue_single_item(self):
        """Test le retrait d'un seul élément."""
        q = Queue()
        q.enqueue("item1")

        result = q.dequeue()

        assert result == "item1"
        assert q.is_empty() is True

    def test_dequeue_fifo_order(self):
        """Test que les éléments sont retirés dans l'ordre FIFO."""
        q = Queue()
        q.enqueue("first")
        q.enqueue("second")
        q.enqueue("third")

        assert q.dequeue() == "first"
        assert q.dequeue() == "second"
        assert q.dequeue() == "third"

    def test_dequeue_empty_queue_raises_error(self):
        """Test que dequeue sur une file vide lève une erreur."""
        q = Queue()

        with pytest.raises(IndexError, match="vide"):
            q.dequeue()

    def test_peek_returns_first_item(self):
        """Test que peek retourne le premier élément sans le retirer."""
        q = Queue()
        q.enqueue("first")
        q.enqueue("second")

        result = q.peek()

        assert result == "first"
        assert q.size() == 2  # La taille ne change pas

    def test_peek_empty_queue_raises_error(self):
        """Test que peek sur une file vide lève une erreur."""
        q = Queue()

        with pytest.raises(IndexError, match="vide"):
            q.peek()

    def test_clear_queue(self):
        """Test le vidage de la file."""
        q = Queue()
        q.enqueue("item1")
        q.enqueue("item2")
        q.enqueue("item3")

        q.clear()

        assert q.is_empty() is True
        assert q.size() == 0

    def test_str_representation(self):
        """Test la représentation textuelle."""
        q = Queue()
        q.enqueue(1)
        q.enqueue(2)

        result = str(q)

        assert "Queue" in result
        assert "1" in result
        assert "2" in result

    def test_repr_equals_str(self):
        """Test que __repr__ retourne la même chose que __str__."""
        q = Queue()
        q.enqueue("test")

        assert repr(q) == str(q)

    def test_queue_with_different_types(self):
        """Test une file avec différents types de données."""
        q = Queue()
        q.enqueue("string")
        q.enqueue(42)
        q.enqueue({"key": "value"})
        q.enqueue([1, 2, 3])

        assert q.dequeue() == "string"
        assert q.dequeue() == 42
        assert q.dequeue() == {"key": "value"}
        assert q.dequeue() == [1, 2, 3]

    def test_enqueue_after_clear(self):
        """Test l'ajout d'éléments après avoir vidé la file."""
        q = Queue()
        q.enqueue("item1")
        q.clear()
        q.enqueue("item2")

        assert q.size() == 1
        assert q.dequeue() == "item2"

    def test_multiple_operations_sequence(self):
        """Test une séquence complexe d'opérations."""
        q = Queue()

        # Ajouter 3 éléments
        q.enqueue("a")
        q.enqueue("b")
        q.enqueue("c")

        # Retirer 1
        assert q.dequeue() == "a"

        # Ajouter 2
        q.enqueue("d")
        q.enqueue("e")

        # Vérifier l'état
        assert q.size() == 4
        assert q.peek() == "b"

        # Retirer tous
        assert q.dequeue() == "b"
        assert q.dequeue() == "c"
        assert q.dequeue() == "d"
        assert q.dequeue() == "e"

        assert q.is_empty() is True
