"""
Tests unitaires pour les Builders.
Test du pattern Builder.
"""
from weather_app.models.builders import StationBuilder, VilleBuilder
from weather_app.models.location import Pays, Ville, Station


class TestStationBuilder:
    """Tests pour la classe StationBuilder."""

    def test_builder_creation(self):
        """Test la création d'un builder."""
        builder = StationBuilder()

        assert builder is not None

    def test_set_id(self):
        """Test la définition de l'ID."""
        builder = StationBuilder()

        result = builder.set_id("s001")

        assert result is builder  # Fluent interface

    def test_set_nom(self):
        """Test la définition du nom."""
        builder = StationBuilder()

        result = builder.set_nom("Montaudran")

        assert result is builder

    def test_set_ville(self):
        """Test la définition de la ville."""
        pays = Pays("fr001", "France")
        ville = Ville("v001", "Toulouse", pays)
        builder = StationBuilder()

        result = builder.set_ville(ville)

        assert result is builder

    def test_set_api_url(self):
        """Test la définition de l'URL API."""
        builder = StationBuilder()

        result = builder.set_api_url("https://api.example.com")

        assert result is builder

    def test_build_complete_station(self):
        """Test la construction d'une station complète."""
        pays = Pays("fr001", "France")
        ville = Ville("v001", "Toulouse", pays)

        builder = StationBuilder()
        station = (builder
                   .set_id("s001")
                   .set_nom("Montaudran")
                   .set_ville(ville)
                   .set_api_url("https://api.example.com")
                   .build())

        assert isinstance(station, Station)
        assert station.id == "s001"
        assert station.nom == "Montaudran"
        assert station.ville == ville
        assert station.api_url == "https://api.example.com"

    def test_build_without_id_raises_error(self):
        """Test que build sans ID lève une erreur."""
        pays = Pays("fr001", "France")
        ville = Ville("v001", "Toulouse", pays)
        builder = StationBuilder()

        builder.set_nom("Montaudran")
        builder.set_ville(ville)
        builder.set_api_url("https://api.example.com")

        try:
            builder.build()
            assert False, "ValueError expected"
        except ValueError as e:
            assert "ID" in str(e)

    def test_build_without_nom_raises_error(self):
        """Test que build sans nom lève une erreur."""
        pays = Pays("fr001", "France")
        ville = Ville("v001", "Toulouse", pays)
        builder = StationBuilder()

        builder.set_id("s001")
        builder.set_ville(ville)
        builder.set_api_url("https://api.example.com")

        try:
            builder.build()
            assert False, "ValueError expected"
        except ValueError as e:
            assert "nom" in str(e)

    def test_build_without_ville_raises_error(self):
        """Test que build sans ville lève une erreur."""
        builder = StationBuilder()

        builder.set_id("s001")
        builder.set_nom("Montaudran")
        builder.set_api_url("https://api.example.com")

        try:
            builder.build()
            assert False, "ValueError expected"
        except ValueError as e:
            assert "ville" in str(e)

    def test_build_without_api_url_raises_error(self):
        """Test que build sans URL API lève une erreur."""
        pays = Pays("fr001", "France")
        ville = Ville("v001", "Toulouse", pays)
        builder = StationBuilder()

        builder.set_id("s001")
        builder.set_nom("Montaudran")
        builder.set_ville(ville)

        try:
            builder.build()
            assert False, "ValueError expected"
        except ValueError as e:
            assert "API URL" in str(e)

    def test_build_with_multiple_missing_fields(self):
        """Test que build avec plusieurs champs manquants affiche tous les champs."""
        builder = StationBuilder()

        try:
            builder.build()
            assert False, "ValueError expected"
        except ValueError as e:
            error_message = str(e)
            assert "ID" in error_message
            assert "nom" in error_message
            assert "ville" in error_message
            assert "API URL" in error_message

    def test_reset_builder(self):
        """Test la réinitialisation du builder."""
        pays = Pays("fr001", "France")
        ville = Ville("v001", "Toulouse", pays)
        builder = StationBuilder()

        builder.set_id("s001")
        builder.set_nom("Montaudran")
        builder.set_ville(ville)
        builder.set_api_url("https://api.example.com")

        result = builder.reset()

        # Vérifier que reset retourne le builder
        assert result is builder

        # Vérifier qu'on ne peut plus build sans données
        try:
            builder.build()
            assert False, "ValueError expected after reset"
        except ValueError:
            pass  # Comportement attendu

    def test_build_multiple_stations_with_reset(self):
        """Test la construction de plusieurs stations avec reset."""
        pays = Pays("fr001", "France")
        ville = Ville("v001", "Toulouse", pays)
        builder = StationBuilder()

        # Première station
        station1 = (builder
                    .set_id("s001")
                    .set_nom("Montaudran")
                    .set_ville(ville)
                    .set_api_url("https://api1.com")
                    .build())

        # Reset et deuxième station
        station2 = (builder
                    .reset()
                    .set_id("s002")
                    .set_nom("Blagnac")
                    .set_ville(ville)
                    .set_api_url("https://api2.com")
                    .build())

        assert station1.id == "s001"
        assert station1.nom == "Montaudran"
        assert station2.id == "s002"
        assert station2.nom == "Blagnac"

    def test_fluent_interface_chaining(self):
        """Test l'interface fluide avec enchaînement."""
        pays = Pays("fr001", "France")
        ville = Ville("v001", "Toulouse", pays)

        # Tout en une ligne
        station = (StationBuilder()
                   .set_id("s001")
                   .set_nom("Montaudran")
                   .set_ville(ville)
                   .set_api_url("https://api.com")
                   .build())

        assert station.id == "s001"


class TestVilleBuilder:
    """Tests pour la classe VilleBuilder."""

    def test_builder_creation(self):
        """Test la création d'un builder."""
        builder = VilleBuilder()

        assert builder is not None

    def test_set_id(self):
        """Test la définition de l'ID."""
        builder = VilleBuilder()

        result = builder.set_id("v001")

        assert result is builder

    def test_set_nom(self):
        """Test la définition du nom."""
        builder = VilleBuilder()

        result = builder.set_nom("Toulouse")

        assert result is builder

    def test_set_pays(self):
        """Test la définition du pays."""
        pays = Pays("fr001", "France")
        builder = VilleBuilder()

        result = builder.set_pays(pays)

        assert result is builder

    def test_build_complete_ville(self):
        """Test la construction d'une ville complète."""
        pays = Pays("fr001", "France")

        builder = VilleBuilder()
        ville = (builder
                 .set_id("v001")
                 .set_nom("Toulouse")
                 .set_pays(pays)
                 .build())

        assert isinstance(ville, Ville)
        assert ville.id == "v001"
        assert ville.nom == "Toulouse"
        assert ville.pays == pays

    def test_build_incomplete_raises_error(self):
        """Test que build incomplet lève une erreur."""
        builder = VilleBuilder()
        builder.set_id("v001")

        try:
            builder.build()
            assert False, "ValueError expected"
        except ValueError as e:
            assert "Informations manquantes" in str(e)

    def test_reset_builder(self):
        """Test la réinitialisation du builder."""
        pays = Pays("fr001", "France")
        builder = VilleBuilder()

        builder.set_id("v001")
        builder.set_nom("Toulouse")
        builder.set_pays(pays)

        result = builder.reset()

        # Vérifier que reset retourne le builder
        assert result is builder

        # Vérifier qu'on ne peut plus build sans données
        try:
            builder.build()
            assert False, "ValueError expected after reset"
        except ValueError:
            pass  # Comportement attendu

    def test_fluent_interface(self):
        """Test l'interface fluide."""
        pays = Pays("fr001", "France")

        ville = (VilleBuilder()
                 .set_id("v001")
                 .set_nom("Toulouse")
                 .set_pays(pays)
                 .build())

        assert ville.nom == "Toulouse"

    def test_build_multiple_villes(self):
        """Test la construction de plusieurs villes."""
        france = Pays("fr001", "France")
        espagne = Pays("es001", "Espagne")
        builder = VilleBuilder()

        toulouse = (builder
                    .set_id("v001")
                    .set_nom("Toulouse")
                    .set_pays(france)
                    .build())

        madrid = (builder
                  .reset()
                  .set_id("v002")
                  .set_nom("Madrid")
                  .set_pays(espagne)
                  .build())

        assert toulouse.nom == "Toulouse"
        assert toulouse.pays == france
        assert madrid.nom == "Madrid"
        assert madrid.pays == espagne
