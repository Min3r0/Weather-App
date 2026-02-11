"""
Tests unitaires pour le pattern Decorator.
"""
import time
from unittest.mock import patch

from weather_app.patterns.decorator import (
    display_measurements_decorator,
    execution_time_decorator,
    error_handler_decorator
)
from weather_app.models.measurement import Measurement


class TestDisplayMeasurementsDecorator:
    """Tests pour display_measurements_decorator."""

    def test_decorator_with_empty_list(self):
        """Test le décorateur avec une liste vide."""

        @display_measurements_decorator
        def get_measurements():
            return []

        with patch('builtins.print'):
            result = get_measurements()

        assert not result

    def test_decorator_with_measurements(self):
        """Test le décorateur avec des mesures."""
        measurements = [
            Measurement("2025-02-11T10:00:00+00:00", 20.0, 70, 101000),
            Measurement("2025-02-11T11:00:00+00:00", 21.0, 68, 101100),
        ]

        @display_measurements_decorator
        def get_measurements():
            return measurements

        with patch('builtins.print'):
            result = get_measurements()

        assert result == measurements

    def test_decorator_with_none(self):
        """Test le décorateur avec None."""

        @display_measurements_decorator
        def get_measurements():
            return None

        with patch('builtins.print'):
            result = get_measurements()

        assert result is None

    def test_decorator_with_non_list(self):
        """Test le décorateur avec un type non-liste."""

        @display_measurements_decorator
        def get_measurements():
            return "not a list"

        with patch('builtins.print'):
            result = get_measurements()

        assert result == "not a list"

    def test_decorator_preserves_function_name(self):
        """Test que le décorateur préserve le nom de la fonction."""

        @display_measurements_decorator
        def my_function():
            return []

        assert my_function.__name__ == "my_function"

    def test_decorator_with_function_args(self):
        """Test le décorateur avec des arguments de fonction."""

        @display_measurements_decorator
        def get_measurements(_station_id, _limit=10):
            return []

        with patch('builtins.print'):
            result = get_measurements("s001", _limit=5)

        assert not result

    @patch('builtins.print')
    def test_decorator_calls_display_function(self, mock_print):
        """Test que le décorateur appelle la fonction d'affichage."""
        measurements = [
            Measurement("2025-02-11T10:00:00+00:00", 20.0, 70, 101000)
        ]

        @display_measurements_decorator
        def get_measurements():
            return measurements

        get_measurements()

        # Vérifier que print a été appelé (l'affichage a eu lieu)
        assert mock_print.called


class TestExecutionTimeDecorator:
    """Tests pour execution_time_decorator."""

    def test_decorator_measures_time(self):
        """Test que le décorateur mesure le temps."""

        @execution_time_decorator
        def slow_function():
            time.sleep(0.1)
            return "result"

        with patch('builtins.print'):
            result = slow_function()

        assert result == "result"

    @patch('builtins.print')
    def test_decorator_prints_execution_time(self, mock_print):
        """Test que le décorateur affiche le temps d'exécution."""

        @execution_time_decorator
        def fast_function():
            return "result"

        fast_function()

        # Vérifier qu'un message contenant le temps a été affiché
        assert mock_print.called
        call_args = str(mock_print.call_args)
        assert "Temps d'exécution" in call_args or "exécution" in call_args.lower()

    def test_decorator_returns_correct_result(self):
        """Test que le décorateur retourne le bon résultat."""

        @execution_time_decorator
        def add_numbers(first_num, second_num):
            return first_num + second_num

        with patch('builtins.print'):
            result = add_numbers(5, 3)

        assert result == 8

    def test_decorator_preserves_function_name(self):
        """Test que le décorateur préserve le nom de la fonction."""

        @execution_time_decorator
        def my_function():
            pass

        assert my_function.__name__ == "my_function"

    def test_decorator_with_exception(self):
        """Test que le décorateur gère les exceptions."""

        @execution_time_decorator
        def failing_function():
            raise ValueError("Test error")

        with patch('builtins.print'):
            try:
                failing_function()
                assert False, "ValueError expected"
            except ValueError as e:
                assert str(e) == "Test error"


class TestErrorHandlerDecorator:
    """Tests pour error_handler_decorator."""

    def test_decorator_returns_result_on_success(self):
        """Test que le décorateur retourne le résultat en cas de succès."""

        @error_handler_decorator
        def successful_function():
            return "success"

        result = successful_function()

        assert result == "success"

    @patch('builtins.print')
    def test_decorator_handles_value_error(self, mock_print):
        """Test que le décorateur gère ValueError."""

        @error_handler_decorator
        def failing_function():
            raise ValueError("Test error")

        result = failing_function()

        assert result is None
        assert mock_print.called

    @patch('builtins.print')
    def test_decorator_handles_type_error(self, mock_print):
        """Test que le décorateur gère TypeError."""

        @error_handler_decorator
        def failing_function():
            raise TypeError("Test error")

        result = failing_function()

        assert result is None
        assert mock_print.called

    @patch('builtins.print')
    def test_decorator_handles_key_error(self, mock_print):
        """Test que le décorateur gère KeyError."""

        @error_handler_decorator
        def failing_function():
            data = {}
            return data["missing_key"]

        result = failing_function()

        assert result is None
        assert mock_print.called

    @patch('builtins.print')
    def test_decorator_handles_attribute_error(self, mock_print):
        """Test que le décorateur gère AttributeError."""

        @error_handler_decorator
        def failing_function():
            obj = None
            return obj.missing_attribute

        result = failing_function()

        assert result is None
        assert mock_print.called

    def test_decorator_does_not_catch_other_exceptions(self):
        """Test que le décorateur ne capture pas d'autres exceptions."""

        @error_handler_decorator
        def failing_function():
            raise RuntimeError("Test error")

        try:
            failing_function()
            assert False, "RuntimeError expected"
        except RuntimeError as e:
            assert str(e) == "Test error"

    def test_decorator_preserves_function_name(self):
        """Test que le décorateur préserve le nom de la fonction."""

        @error_handler_decorator
        def my_function():
            pass

        assert my_function.__name__ == "my_function"

    def test_decorator_with_function_args(self):
        """Test le décorateur avec des arguments."""

        @error_handler_decorator
        def divide(first_num, second_num):
            if second_num == 0:
                raise ValueError("Division by zero")
            return first_num / second_num

        # Succès
        assert divide(10, 2) == 5.0

        # Erreur
        with patch('builtins.print'):
            result = divide(10, 0)
        assert result is None


class TestDecoratorCombination:
    """Tests de combinaison de décorateurs."""

    def test_multiple_decorators(self):
        """Test l'utilisation de plusieurs décorateurs."""

        @execution_time_decorator
        @error_handler_decorator
        def complex_function():
            return "result"

        with patch('builtins.print'):
            result = complex_function()

        assert result == "result"

    def test_decorators_order_matters(self):
        """Test que l'ordre des décorateurs compte."""

        @error_handler_decorator
        @execution_time_decorator
        def failing_function():
            raise ValueError("Error")

        with patch('builtins.print'):
            result = failing_function()

        # L'erreur devrait être capturée
        assert result is None

    def test_all_three_decorators(self):
        """Test l'utilisation des trois décorateurs ensemble."""
        measurements = [
            Measurement("2025-02-11T10:00:00+00:00", 20.0, 70, 101000)
        ]

        @display_measurements_decorator
        @execution_time_decorator
        @error_handler_decorator
        def get_measurements():
            return measurements

        with patch('builtins.print'):
            result = get_measurements()

        assert result == measurements


class TestDecoratorEdgeCases:
    """Tests de cas limites pour les décorateurs."""

    def test_display_decorator_with_large_list(self):
        """Test le décorateur d'affichage avec beaucoup de mesures."""
        measurements = [
            Measurement(f"2025-02-11T{i:02d}:00:00+00:00", 20.0 + i, 70, 101000)
            for i in range(100)
        ]

        @display_measurements_decorator
        def get_measurements():
            return measurements

        with patch('builtins.print'):
            result = get_measurements()

        assert len(result) == 100

    def test_execution_time_with_zero_time(self):
        """Test le décorateur de temps avec une fonction instantanée."""

        @execution_time_decorator
        def instant_function():
            return "instant"

        with patch('builtins.print'):
            result = instant_function()

        assert result == "instant"

    @patch('builtins.print')
    def test_error_handler_prints_error_message(self, mock_print):
        """Test que le gestionnaire d'erreurs affiche le message d'erreur."""

        @error_handler_decorator
        def failing_function():
            raise ValueError("Custom error message")

        failing_function()

        # Vérifier que le message d'erreur est affiché
        call_str = str(mock_print.call_args)
        assert "Custom error message" in call_str or "Erreur" in call_str
