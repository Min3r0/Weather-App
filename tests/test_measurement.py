"""
Tests unitaires pour la classe Measurement.
"""
from weather_app.models.measurement import Measurement


class TestMeasurement:
    """Tests pour la classe Measurement."""

    def test_measurement_creation(self):
        """Test la création d'une mesure."""
        m = Measurement(
            heure="2025-02-11T10:00:00+00:00",
            temperature=15.5,
            humidite=75,
            pression=101325
        )

        assert m.heure == "2025-02-11T10:00:00+00:00"
        assert m.temperature == 15.5
        assert m.humidite == 75
        assert m.pression == 101325

    def test_heure_property(self):
        """Test la propriété heure."""
        m = Measurement(
            heure="2025-02-11T10:00:00+00:00",
            temperature=15.0,
            humidite=70,
            pression=101000
        )

        assert m.heure == "2025-02-11T10:00:00+00:00"

    def test_temperature_property(self):
        """Test la propriété temperature."""
        m = Measurement(
            heure="2025-02-11T10:00:00+00:00",
            temperature=25.7,
            humidite=60,
            pression=101000
        )

        assert m.temperature == 25.7

    def test_humidite_property(self):
        """Test la propriété humidite."""
        m = Measurement(
            heure="2025-02-11T10:00:00+00:00",
            temperature=20.0,
            humidite=85,
            pression=101000
        )

        assert m.humidite == 85

    def test_pression_property(self):
        """Test la propriété pression."""
        m = Measurement(
            heure="2025-02-11T10:00:00+00:00",
            temperature=20.0,
            humidite=70,
            pression=99500
        )

        assert m.pression == 99500

    def test_format_heure_valid_iso(self):
        """Test le formatage d'une heure ISO valide."""
        m = Measurement(
            heure="2025-02-11T14:30:00+00:00",
            temperature=20.0,
            humidite=70,
            pression=101000
        )

        result = m.format_heure()

        assert result == "11/02/2025 14:30"

    def test_format_heure_with_z(self):
        """Test le formatage d'une heure avec Z."""
        m = Measurement(
            heure="2025-12-25T23:59:00Z",
            temperature=0.0,
            humidite=90,
            pression=101000
        )

        result = m.format_heure()

        assert result == "25/12/2025 23:59"

    def test_format_heure_invalid_format(self):
        """Test le formatage d'une heure invalide."""
        m = Measurement(
            heure="invalid_date",
            temperature=20.0,
            humidite=70,
            pression=101000
        )

        result = m.format_heure()

        # Devrait retourner la chaîne d'origine
        assert result == "invalid_date"

    def test_str_representation(self):
        """Test la représentation textuelle."""
        m = Measurement(
            heure="2025-02-11T10:00:00+00:00",
            temperature=18.5,
            humidite=65,
            pression=101300
        )

        result = str(m)

        assert "11/02/2025 10:00" in result
        assert "18.5°C" in result
        assert "65%" in result
        assert "101300 Pa" in result

    def test_repr_representation(self):
        """Test la représentation technique."""
        m = Measurement(
            heure="2025-02-11T10:00:00+00:00",
            temperature=18.5,
            humidite=65,
            pression=101300
        )

        result = repr(m)

        assert "Measurement" in result
        assert "2025-02-11T10:00:00+00:00" in result
        assert "18.5°C" in result
        assert "65%" in result
        assert "101300Pa" in result

    def test_negative_temperature(self):
        """Test avec une température négative."""
        m = Measurement(
            heure="2025-01-15T08:00:00+00:00",
            temperature=-5.0,
            humidite=95,
            pression=102000
        )

        assert m.temperature == -5.0
        assert "-5.0°C" in str(m)

    def test_zero_humidite(self):
        """Test avec une humidité à zéro."""
        m = Measurement(
            heure="2025-02-11T10:00:00+00:00",
            temperature=30.0,
            humidite=0,
            pression=101000
        )

        assert m.humidite == 0

    def test_high_pression(self):
        """Test avec une haute pression."""
        m = Measurement(
            heure="2025-02-11T10:00:00+00:00",
            temperature=20.0,
            humidite=50,
            pression=105000
        )

        assert m.pression == 105000

    def test_float_temperature(self):
        """Test avec une température à virgule."""
        m = Measurement(
            heure="2025-02-11T10:00:00+00:00",
            temperature=22.75,
            humidite=70,
            pression=101000
        )

        assert m.temperature == 22.75
        assert isinstance(m.temperature, float)

    def test_different_date_formats(self):
        """Test avec différents formats de date."""
        # Format avec +00:00
        m1 = Measurement(
            heure="2025-02-11T10:00:00+00:00",
            temperature=20.0,
            humidite=70,
            pression=101000
        )

        # Format avec Z
        m2 = Measurement(
            heure="2025-02-11T10:00:00Z",
            temperature=20.0,
            humidite=70,
            pression=101000
        )

        assert "11/02/2025 10:00" in m1.format_heure()
        assert "11/02/2025 10:00" in m2.format_heure()
