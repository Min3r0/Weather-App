"""
Tests unitaires pour les classes de localisation.
Test de l'héritage et des relations entre classes.
"""
from weather_app.models.location import Location, Pays, Ville, Station
from weather_app.models.measurement import Measurement


class TestPays:
    """Tests pour la classe Pays."""

    def test_pays_creation(self):
        """Test la création d'un pays."""
        pays = Pays("fr001", "France")

        assert pays.id == "fr001"
        assert pays.nom == "France"
        assert isinstance(pays.get_villes(), list)
        assert len(pays.get_villes()) == 0

    def test_pays_inherits_from_location(self):
        """Test que Pays hérite de Location."""
        pays = Pays("fr001", "France")

        assert isinstance(pays, Location)

    def test_add_ville_to_pays(self):
        """Test l'ajout d'une ville à un pays."""
        pays = Pays("fr001", "France")
        ville = Ville("v001", "Toulouse", pays)

        villes = pays.get_villes()

        assert len(villes) == 1
        assert villes[0] == ville

    def test_add_multiple_villes(self):
        """Test l'ajout de plusieurs villes."""
        pays = Pays("fr001", "France")
        ville1 = Ville("v001", "Toulouse", pays)
        ville2 = Ville("v002", "Paris", pays)
        ville3 = Ville("v003", "Lyon", pays)

        villes = pays.get_villes()

        assert len(villes) == 3
        assert ville1 in villes
        assert ville2 in villes
        assert ville3 in villes

    def test_add_ville_twice_ignored(self):
        """Test qu'ajouter deux fois la même ville est ignoré."""
        pays = Pays("fr001", "France")
        ville = Ville("v001", "Toulouse", pays)
        pays.add_ville(ville)  # Ajout explicite supplémentaire

        villes = pays.get_villes()

        assert len(villes) == 1

    def test_get_info(self):
        """Test la méthode get_info."""
        pays = Pays("fr001", "France")
        Ville("v001", "Toulouse", pays)
        Ville("v002", "Paris", pays)

        info = pays.get_info()

        assert "Pays: France" in info
        assert "fr001" in info
        assert "2 ville(s)" in info

    def test_get_villes_returns_copy(self):
        """Test que get_villes retourne une copie."""
        pays = Pays("fr001", "France")
        Ville("v001", "Toulouse", pays)

        villes1 = pays.get_villes()
        villes2 = pays.get_villes()

        assert villes1 == villes2
        assert villes1 is not villes2  # Copies différentes


class TestVille:
    """Tests pour la classe Ville."""

    def test_ville_creation(self):
        """Test la création d'une ville."""
        pays = Pays("fr001", "France")
        ville = Ville("v001", "Toulouse", pays)

        assert ville.id == "v001"
        assert ville.nom == "Toulouse"
        assert ville.pays == pays
        assert isinstance(ville.get_stations(), list)
        assert len(ville.get_stations()) == 0

    def test_ville_inherits_from_location(self):
        """Test que Ville hérite de Location."""
        pays = Pays("fr001", "France")
        ville = Ville("v001", "Toulouse", pays)

        assert isinstance(ville, Location)

    def test_ville_auto_added_to_pays(self):
        """Test que la ville est automatiquement ajoutée au pays."""
        pays = Pays("fr001", "France")
        ville = Ville("v001", "Toulouse", pays)

        assert ville in pays.get_villes()

    def test_add_station_to_ville(self):
        """Test l'ajout d'une station à une ville."""
        pays = Pays("fr001", "France")
        ville = Ville("v001", "Toulouse", pays)
        station = Station("s001", "Montaudran", ville, "https://api.example.com")

        stations = ville.get_stations()

        assert len(stations) == 1
        assert stations[0] == station

    def test_add_multiple_stations(self):
        """Test l'ajout de plusieurs stations."""
        pays = Pays("fr001", "France")
        ville = Ville("v001", "Toulouse", pays)
        station1 = Station("s001", "Montaudran", ville, "https://api1.com")
        station2 = Station("s002", "Blagnac", ville, "https://api2.com")

        stations = ville.get_stations()

        assert len(stations) == 2
        assert station1 in stations
        assert station2 in stations

    def test_get_info(self):
        """Test la méthode get_info."""
        pays = Pays("fr001", "France")
        ville = Ville("v001", "Toulouse", pays)
        Station("s001", "Montaudran", ville, "https://api.com")

        info = ville.get_info()

        assert "Ville: Toulouse" in info
        assert "Pays: France" in info
        assert "1 station(s)" in info

    def test_get_stations_returns_copy(self):
        """Test que get_stations retourne une copie."""
        pays = Pays("fr001", "France")
        ville = Ville("v001", "Toulouse", pays)
        Station("s001", "Montaudran", ville, "https://api.com")

        stations1 = ville.get_stations()
        stations2 = ville.get_stations()

        assert stations1 == stations2
        assert stations1 is not stations2


class TestStation:
    """Tests pour la classe Station."""

    def test_station_creation(self):
        """Test la création d'une station."""
        pays = Pays("fr001", "France")
        ville = Ville("v001", "Toulouse", pays)
        station = Station("s001", "Montaudran", ville, "https://api.example.com")

        assert station.id == "s001"
        assert station.nom == "Montaudran"
        assert station.ville == ville
        assert station.api_url == "https://api.example.com"
        assert len(station.get_measurements()) == 0

    def test_station_inherits_from_location(self):
        """Test que Station hérite de Location."""
        pays = Pays("fr001", "France")
        ville = Ville("v001", "Toulouse", pays)
        station = Station("s001", "Montaudran", ville, "https://api.com")

        assert isinstance(station, Location)

    def test_station_auto_added_to_ville(self):
        """Test que la station est automatiquement ajoutée à la ville."""
        pays = Pays("fr001", "France")
        ville = Ville("v001", "Toulouse", pays)
        station = Station("s001", "Montaudran", ville, "https://api.com")

        assert station in ville.get_stations()

    def test_api_url_getter(self):
        """Test le getter de api_url."""
        pays = Pays("fr001", "France")
        ville = Ville("v001", "Toulouse", pays)
        station = Station("s001", "Montaudran", ville, "https://api.example.com")

        assert station.api_url == "https://api.example.com"

    def test_api_url_setter(self):
        """Test le setter de api_url."""
        pays = Pays("fr001", "France")
        ville = Ville("v001", "Toulouse", pays)
        station = Station("s001", "Montaudran", ville, "https://api.example.com")

        station.api_url = "https://new-api.example.com"

        assert station.api_url == "https://new-api.example.com"

    def test_add_measurement(self):
        """Test l'ajout d'une mesure."""
        pays = Pays("fr001", "France")
        ville = Ville("v001", "Toulouse", pays)
        station = Station("s001", "Montaudran", ville, "https://api.com")

        measurement = Measurement(
            heure="2025-02-11T10:00:00+00:00",
            temperature=20.0,
            humidite=70,
            pression=101000
        )

        station.add_measurement(measurement)

        measurements = station.get_measurements()
        assert len(measurements) == 1
        assert measurements[0] == measurement

    def test_add_multiple_measurements(self):
        """Test l'ajout de plusieurs mesures."""
        pays = Pays("fr001", "France")
        ville = Ville("v001", "Toulouse", pays)
        station = Station("s001", "Montaudran", ville, "https://api.com")

        m1 = Measurement("2025-02-11T10:00:00+00:00", 20.0, 70, 101000)
        m2 = Measurement("2025-02-11T11:00:00+00:00", 21.0, 68, 101100)
        m3 = Measurement("2025-02-11T12:00:00+00:00", 22.0, 65, 101200)

        station.add_measurement(m1)
        station.add_measurement(m2)
        station.add_measurement(m3)

        measurements = station.get_measurements()
        assert len(measurements) == 3
        assert m1 in measurements
        assert m2 in measurements
        assert m3 in measurements

    def test_clear_measurements(self):
        """Test le nettoyage des mesures."""
        pays = Pays("fr001", "France")
        ville = Ville("v001", "Toulouse", pays)
        station = Station("s001", "Montaudran", ville, "https://api.com")

        station.add_measurement(Measurement("2025-02-11T10:00:00+00:00", 20.0, 70, 101000))
        station.add_measurement(Measurement("2025-02-11T11:00:00+00:00", 21.0, 68, 101100))

        station.clear_measurements()

        assert len(station.get_measurements()) == 0

    def test_get_info(self):
        """Test la méthode get_info."""
        pays = Pays("fr001", "France")
        ville = Ville("v001", "Toulouse", pays)
        station = Station("s001", "Montaudran", ville, "https://api.com")

        station.add_measurement(Measurement("2025-02-11T10:00:00+00:00", 20.0, 70, 101000))
        station.add_measurement(Measurement("2025-02-11T11:00:00+00:00", 21.0, 68, 101100))

        info = station.get_info()

        assert "Station: Montaudran" in info
        assert "Ville: Toulouse" in info
        assert "Pays: France" in info
        assert "2 mesure(s)" in info

    def test_get_measurements_returns_copy(self):
        """Test que get_measurements retourne une copie."""
        pays = Pays("fr001", "France")
        ville = Ville("v001", "Toulouse", pays)
        station = Station("s001", "Montaudran", ville, "https://api.com")

        station.add_measurement(Measurement("2025-02-11T10:00:00+00:00", 20.0, 70, 101000))

        measurements1 = station.get_measurements()
        measurements2 = station.get_measurements()

        assert measurements1 == measurements2
        assert measurements1 is not measurements2


class TestLocationHierarchy:
    """Tests de la hiérarchie complète."""

    def test_full_hierarchy(self):
        """Test la création d'une hiérarchie complète."""
        pays = Pays("fr001", "France")
        ville = Ville("v001", "Toulouse", pays)
        station = Station("s001", "Montaudran", ville, "https://api.com")

        # Vérifier les relations
        assert pays.get_villes()[0] == ville
        assert ville.pays == pays
        assert ville.get_stations()[0] == station
        assert station.ville == ville
        assert station.ville.pays == pays

    def test_multiple_levels(self):
        """Test une hiérarchie avec plusieurs niveaux."""
        # Créer 2 pays
        france = Pays("fr001", "France")
        espagne = Pays("es001", "Espagne")

        # Créer des villes
        toulouse = Ville("v001", "Toulouse", france)
        paris = Ville("v002", "Paris", france)
        madrid = Ville("v003", "Madrid", espagne)

        # Créer des stations
        Station("s001", "Montaudran", toulouse, "https://api1.com")
        Station("s002", "Blagnac", toulouse, "https://api2.com")
        Station("s003", "Orly", paris, "https://api3.com")
        Station("s004", "Barajas", madrid, "https://api4.com")

        # Vérifications
        assert len(france.get_villes()) == 2
        assert len(espagne.get_villes()) == 1
        assert len(toulouse.get_stations()) == 2
        assert len(paris.get_stations()) == 1
        assert len(madrid.get_stations()) == 1
