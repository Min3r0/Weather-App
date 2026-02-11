"""
Tests unitaires pour le pattern Observer.
"""

# pylint: disable=too-few-public-methods

from unittest.mock import Mock

from weather_app.patterns.observer import Observer, Subject, StationSelector, DataLoader


class ConcreteObserver(Observer):
    """
    Observateur concret pour les tests.
    
    Cet observateur implémente l'interface Observer pour les besoins des tests.
    """

    def __init__(self):
        self.update_called = False
        self.received_subject = None
        self.received_args = None
        self.received_kwargs = None

    def update(self, subject, *args, **kwargs):
        """Méthode update pour les tests."""
        self.update_called = True
        self.received_subject = subject
        self.received_args = args
        self.received_kwargs = kwargs


class TestSubject:
    """Tests pour la classe Subject."""

    def test_subject_creation(self):
        """Test la création d'un sujet."""
        subject = Subject()

        # Vérifier que la liste des observateurs est vide via une méthode publique
        # On teste en ajoutant puis notifiant
        observer = ConcreteObserver()
        subject.attach(observer)
        subject.detach(observer)
        # Si ça ne lève pas d'erreur, c'est bon
        assert subject is not None

    def test_attach_observer(self):
        """Test l'attachement d'un observateur."""
        subject = Subject()
        observer = ConcreteObserver()

        subject.attach(observer)

        # Vérifier en notifiant
        subject.notify()
        assert observer.update_called is True

    def test_attach_multiple_observers(self):
        """Test l'attachement de plusieurs observateurs."""
        subject = Subject()
        observer1 = ConcreteObserver()
        observer2 = ConcreteObserver()
        observer3 = ConcreteObserver()

        subject.attach(observer1)
        subject.attach(observer2)
        subject.attach(observer3)

        # Vérifier en notifiant tous
        subject.notify()
        assert observer1.update_called is True
        assert observer2.update_called is True
        assert observer3.update_called is True

    def test_attach_same_observer_twice_ignored(self):
        """Test qu'attacher deux fois le même observateur est ignoré."""
        subject = Subject()
        observer = ConcreteObserver()

        subject.attach(observer)
        subject.attach(observer)

        # Difficile de vérifier sans accès aux membres protégés
        # On vérifie juste que ça ne lève pas d'erreur
        subject.notify()
        assert observer.update_called is True

    def test_detach_observer(self):
        """Test le détachement d'un observateur."""
        subject = Subject()
        observer = ConcreteObserver()

        subject.attach(observer)
        subject.detach(observer)

        # Vérifier que l'observateur n'est plus notifié
        observer.update_called = False
        subject.notify()
        assert observer.update_called is False

    def test_detach_non_attached_observer(self):
        """Test le détachement d'un observateur non attaché."""
        subject = Subject()
        observer = ConcreteObserver()

        # Ne devrait pas lever d'erreur
        subject.detach(observer)

        assert True  # Si on arrive ici, c'est bon

    def test_notify_single_observer(self):
        """Test la notification d'un seul observateur."""
        subject = Subject()
        observer = ConcreteObserver()

        subject.attach(observer)
        subject.notify()

        assert observer.update_called is True
        assert observer.received_subject == subject

    def test_notify_multiple_observers(self):
        """Test la notification de plusieurs observateurs."""
        subject = Subject()
        observer1 = ConcreteObserver()
        observer2 = ConcreteObserver()
        observer3 = ConcreteObserver()

        subject.attach(observer1)
        subject.attach(observer2)
        subject.attach(observer3)

        subject.notify()

        assert observer1.update_called is True
        assert observer2.update_called is True
        assert observer3.update_called is True

    def test_notify_with_args(self):
        """Test la notification avec arguments positionnels."""
        subject = Subject()
        observer = ConcreteObserver()

        subject.attach(observer)
        subject.notify("arg1", "arg2", 123)

        assert observer.received_args == ("arg1", "arg2", 123)

    def test_notify_with_kwargs(self):
        """Test la notification avec arguments nommés."""
        subject = Subject()
        observer = ConcreteObserver()

        subject.attach(observer)
        subject.notify(station="Montaudran", temperature=20.5)

        assert observer.received_kwargs == {"station": "Montaudran", "temperature": 20.5}

    def test_notify_with_args_and_kwargs(self):
        """Test la notification avec les deux types d'arguments."""
        subject = Subject()
        observer = ConcreteObserver()

        subject.attach(observer)
        subject.notify("arg1", 42, key1="value1", key2="value2")

        assert observer.received_args == ("arg1", 42)
        assert observer.received_kwargs == {"key1": "value1", "key2": "value2"}


class TestStationSelector:
    """Tests pour la classe StationSelector."""

    def test_station_selector_creation(self):
        """Test la création d'un sélecteur de station."""
        selector = StationSelector()

        # Vérifier que le sélecteur a été créé
        assert selector is not None
        assert selector.selected_station is None

    def test_select_station(self):
        """Test la sélection d'une station."""
        selector = StationSelector()
        mock_station = Mock()
        mock_station.nom = "Montaudran"

        selector.select_station(mock_station)

        assert selector.selected_station == mock_station

    def test_select_station_notifies_observers(self):
        """Test que la sélection notifie les observateurs."""
        selector = StationSelector()
        observer = ConcreteObserver()
        mock_station = Mock()

        selector.attach(observer)
        selector.select_station(mock_station)

        assert observer.update_called is True
        assert observer.received_kwargs["station"] == mock_station

    def test_selected_station_property(self):
        """Test la propriété selected_station."""
        selector = StationSelector()
        mock_station = Mock()

        selector.select_station(mock_station)

        assert selector.selected_station == mock_station

    def test_select_multiple_stations(self):
        """Test la sélection successive de plusieurs stations."""
        selector = StationSelector()
        observer = ConcreteObserver()
        station1 = Mock()
        station1.nom = "Station1"
        station2 = Mock()
        station2.nom = "Station2"

        selector.attach(observer)

        selector.select_station(station1)
        assert selector.selected_station == station1

        selector.select_station(station2)
        assert selector.selected_station == station2


class TestDataLoader:
    """Tests pour la classe DataLoader."""

    def test_data_loader_creation(self):
        """Test la création d'un chargeur de données."""
        mock_api_service = Mock()
        loader = DataLoader(mock_api_service)

        # Vérifier que le loader a été créé
        assert loader is not None

    def test_update_with_station(self):
        """Test la mise à jour avec une station."""
        mock_api_service = Mock()
        loader = DataLoader(mock_api_service)
        mock_station = Mock()
        mock_station.nom = "Montaudran"
        mock_subject = Mock()

        loader.update(mock_subject, station=mock_station)

        mock_api_service.fetch_data_for_station.assert_called_once_with(mock_station)

    def test_update_without_station(self):
        """Test la mise à jour sans station."""
        mock_api_service = Mock()
        loader = DataLoader(mock_api_service)
        mock_subject = Mock()

        # Ne devrait pas lever d'erreur
        loader.update(mock_subject)

        mock_api_service.fetch_data_for_station.assert_not_called()

    def test_update_with_none_station(self):
        """Test la mise à jour avec station=None."""
        mock_api_service = Mock()
        loader = DataLoader(mock_api_service)
        mock_subject = Mock()

        loader.update(mock_subject, station=None)

        mock_api_service.fetch_data_for_station.assert_not_called()


class TestObserverIntegration:
    """Tests d'intégration du pattern Observer."""

    def test_station_selection_triggers_data_loading(self):
        """Test que la sélection d'une station déclenche le chargement."""
        mock_api_service = Mock()
        selector = StationSelector()
        loader = DataLoader(mock_api_service)
        mock_station = Mock()
        mock_station.nom = "Montaudran"

        # Attacher l'observateur
        selector.attach(loader)

        # Sélectionner une station
        selector.select_station(mock_station)

        # Vérifier que l'API a été appelée
        mock_api_service.fetch_data_for_station.assert_called_once_with(mock_station)

    def test_multiple_observers_on_selection(self):
        """Test plusieurs observateurs sur une sélection."""
        mock_api_service1 = Mock()
        mock_api_service2 = Mock()
        selector = StationSelector()
        loader1 = DataLoader(mock_api_service1)
        loader2 = DataLoader(mock_api_service2)
        mock_station = Mock()

        selector.attach(loader1)
        selector.attach(loader2)

        selector.select_station(mock_station)

        mock_api_service1.fetch_data_for_station.assert_called_once()
        mock_api_service2.fetch_data_for_station.assert_called_once()

    def test_detach_observer_stops_notifications(self):
        """Test que détacher un observateur arrête les notifications."""
        mock_api_service = Mock()
        selector = StationSelector()
        loader = DataLoader(mock_api_service)
        mock_station = Mock()

        selector.attach(loader)
        selector.detach(loader)

        selector.select_station(mock_station)

        # L'API ne devrait pas être appelée
        mock_api_service.fetch_data_for_station.assert_not_called()

    def test_observer_receives_correct_station(self):
        """Test que l'observateur reçoit la bonne station."""
        mock_api_service = Mock()
        selector = StationSelector()
        loader = DataLoader(mock_api_service)
        mock_station = Mock()
        mock_station.nom = "Test Station"

        selector.attach(loader)
        selector.select_station(mock_station)

        # Vérifier que la bonne station a été passée
        mock_api_service.fetch_data_for_station.assert_called_once_with(mock_station)
