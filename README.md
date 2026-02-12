# 🌤️ Application Météo - Clean Code & Design Patterns

Application Python complète pour consulter les données météorologiques, développée selon les principes du Clean Code et utilisant plusieurs design patterns.

## 📁 Structure du Projet

```
Weather/                            # Racine du projet
├── weather_app/                   # Package Python
│   ├── __init__.py               # Initialisation du package
│   ├── __main__.py               # Point d'entrée de l'application
│   ├── config/
│   │   ├── __init__.py
│   │   └── singleton_config.py   # Pattern Singleton pour la configuration
│   ├── models/
│   │   ├── __init__.py
│   │   ├── location.py           # Classes Pays, Ville, Station (héritage)
│   │   ├── measurement.py        # Classe Measurement
│   │   └── builders.py           # Pattern Builder pour Station et Ville
│   ├── data_structures/
│   │   ├── __init__.py
│   │   ├── linked_list.py        # Liste Chaînée pour les stations
│   │   └── queue.py              # File pour les requêtes API
│   ├── patterns/
│   │   ├── __init__.py
│   │   ├── observer.py           # Pattern Observer
│   │   ├── decorator.py          # Pattern Decorator
│   │   └── command.py            # Pattern Command
│   ├── services/
│   │   ├── __init__.py
│   │   └── api_service.py        # Service d'appel à l'API
│   └── ui/
│       ├── __init__.py
│       └── menu.py               # Interface utilisateur
├── tests/                         # Tests unitaires
│   ├── __init__.py
│   └── test_*.py
├── data/                          # Données persistantes
│   └── config.json               # Configuration (créé automatiquement)
├── requirements.txt               # Dépendances Python
├── Dockerfile                     # Configuration Docker
├── docker-compose.yml             # Docker Compose
└── README.md                      # Cette documentation
```

## 🎯 Principes et Patterns Implémentés

### Principes Clean Code

- **SOLID** : Séparation des responsabilités, interfaces claires
- **DRY** : Code réutilisable sans répétition
- **KISS** : Solutions simples et compréhensibles
- **YAGNI** : Implémentation uniquement du nécessaire

### Design Patterns

1. **Singleton** : Configuration unique partagée (`singleton_config.py`)
2. **Builder** : Construction progressive des stations (`builders.py`)
3. **Observer** : Chargement automatique des données lors de la sélection (`observer.py`)
4. **Command** : Encapsulation des actions utilisateur (`command.py`)
5. **Decorator** : Affichage formaté des mesures (`decorator.py`)

### Structures de Données

- **Liste Chaînée** : Affichage des stations météo
- **File (Queue)** : Gestion des requêtes API

### Héritage

```
Location (classe abstraite)
    ├── Pays
    ├── Ville (hérite de Location)
    └── Station (hérite de Location)
```

## 🚀 Installation et Lancement

### Méthode 1 : Python Local

#### Installation

```bash
# Se placer à la racine du projet
cd Weather

# Installer les dépendances
pip install -r requirements.txt
```

#### Lancement

```bash
# Depuis la racine du projet Weather/
python -m weather_app
```

### Méthode 2 : Docker (Recommandée) 🐳

#### Prérequis

- Docker installé
- Docker Compose installé

#### Lancement en Mode Interactif

```bash
# Depuis la racine du projet Weather/
docker-compose run --rm weather_app
```

**💡 Pourquoi `docker-compose run` ?**
- ✅ Permet l'interaction avec le terminal (navigation dans les menus)
- ✅ Monte automatiquement le volume `data/` pour persister la configuration
- ✅ Supprime automatiquement le conteneur à la sortie (`--rm`)

#### Autres Commandes Docker

```bash
# Build l'image (si modifications du code)
docker-compose build

# Arrêter et supprimer les conteneurs
docker-compose down

# Nettoyer complètement (conteneurs + images + volumes)
docker-compose down --rmi all --volumes
docker system prune -a --volumes --force

# Rebuild complet
docker-compose build --no-cache
docker-compose run --rm weather_app
```

#### Alternative : Docker sans Compose

```bash
# Build l'image
docker build -t weather_app .

# Lancer en mode interactif
docker run -it --rm -v ${PWD}/data:/app/data weather_app
```

**Sur Windows PowerShell :**
```powershell
docker run -it --rm -v ${PWD}/data:/app/data weather_app
```

### Configuration Docker

#### Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=utf-8
CMD ["python", "-m", "weather_app"]
```

#### docker-compose.yml

```yaml
services:
  weather_app:
    build: .
    container_name: weather_app
    stdin_open: true      # Mode interactif
    tty: true             # Terminal
    volumes:
      - ./data:/app/data  # Persistance des données
    environment:
      - PYTHONUNBUFFERED=1
      - PYTHONIOENCODING=utf-8
```

**Important** : Ne pas utiliser `docker-compose up` car cela lance en mode détaché. Utilisez toujours `docker-compose run --rm weather_app` pour pouvoir interagir avec les menus.

## 📋 Utilisation

### Premier lancement

Au premier lancement, aucune donnée n'est configurée. Vous devez :

1. Aller dans **Configuration** (choix `2`)
2. Ajouter un **Pays** (exemple : France)
3. Ajouter une **Ville** (exemple : Toulouse, liée à France)
4. Ajouter une **Station** (exemple : Montaudran, liée à Toulouse)

### Navigation

L'application propose plusieurs menus :

#### Menu Principal
```
════════════════════════════════════════════════════════════════
                    🌤️  MENU PRINCIPAL
════════════════════════════════════════════════════════════════

1. Voir la météo
2. Configuration
0. Quitter le programme
```

#### Voir la Météo
- Sélectionner une station
- Afficher les mesures
- Rafraîchir les données

#### Configuration
- Gérer les pays (lister, ajouter, supprimer)
- Gérer les villes (lister, ajouter, supprimer)
- Gérer les stations (lister, ajouter, modifier URL, supprimer)

## 🔧 Exemple de Configuration

### Station Toulouse Montaudran

**URL API :**
```
https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets/12-station-meteo-toulouse-montaudran/records?select=heure_de_paris%2C%20humidite%2C%20temperature_en_degre_c%2C%20pression&order_by=heure_de_paris%20DESC&limit=100
```

**Configuration étape par étape :**
1. Menu Principal → `2` (Configuration)
2. Gérer les pays → `2` (Ajouter un pays)
   - Nom du pays : `France`
3. Gérer les villes → `2` (Ajouter une ville)
   - Sélectionner le pays : `1` (France)
   - Nom de la ville : `Toulouse`
4. Gérer les stations → `2` (Ajouter une station)
   - Sélectionner la ville : `1` (Toulouse)
   - Nom de la station : `Montaudran`
   - URL de l'API : (copier l'URL ci-dessus)

### Station Toulouse Compans-Cafarelli

**URL API :**
```
https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets/42-station-meteo-toulouse-parc-compans-cafarelli/records?select=heure_de_paris%2C%20humidite%2C%20temperature_en_degre_c%2C%20pression&order_by=heure_de_paris%20DESC&limit=100
```

## 📊 Format des Données API

L'application attend des données au format JSON :

```json
{
  "total_count": 112613,
  "results": [
    {
      "heure_de_paris": "2025-12-15T10:00:00+00:00",
      "humidite": 81,
      "temperature_en_degre_c": 15,
      "pression": 99400
    }
  ]
}
```

## 💾 Stockage et Persistance

### En local
- La configuration est sauvegardée dans `Weather/data/config.json`
- Le fichier est créé automatiquement au premier lancement

### Avec Docker
- Le dossier `data/` est monté comme volume : `./data:/app/data`
- Les configurations sont **persistées** entre les redémarrages
- Le fichier `config.json` est accessible depuis votre machine locale

**Chemin du fichier** :
- Local : `Weather/data/config.json`
- Docker : `/app/data/config.json` (monté depuis `Weather/data/`)

## 🎨 Fonctionnalités

- ✅ Affichage des mesures météo (température, humidité, pression)
- ✅ Rafraîchissement des données en temps réel
- ✅ Gestion hiérarchique : Pays → Ville → Station
- ✅ Interface terminal avec nettoyage d'écran
- ✅ Navigation intuitive par numéros
- ✅ Validation des URLs API
- ✅ Gestion des erreurs réseau
- ✅ Support Docker avec persistance des données
- ✅ Encodage UTF-8 pour Windows

## 🧪 Tests

### Lancer les tests

```bash
# Tous les tests
pytest

# Avec rapport de couverture
pytest --cov=weather_app --cov-report=html

# Tests spécifiques
pytest tests/test_singleton_config.py
pytest tests/test_observer.py
```

### Voir le rapport de couverture

```bash
# Ouvrir le rapport HTML
# Linux/Mac
open htmlcov/index.html

# Windows
start htmlcov/index.html
```

## 🧩 Architecture Technique

### Séparation des Responsabilités

- **Models** : Entités métier (Pays, Ville, Station, Measurement)
- **Services** : Logique métier (ApiService)
- **Patterns** : Comportements réutilisables (Observer, Command, Decorator)
- **Data Structures** : Structures personnalisées (LinkedList, Queue)
- **UI** : Interface utilisateur (Menu)
- **Config** : Configuration (Singleton)

### Flux de Données

1. L'utilisateur sélectionne une station (via UI)
2. Le pattern **Command** encapsule l'action
3. Le pattern **Observer** détecte la sélection
4. L'**ApiService** récupère les données (via Queue)
5. Le pattern **Decorator** formate l'affichage
6. Les données sont affichées dans le terminal

### Diagramme de séquence simplifié

```
User → Menu → Command → Observer → ApiService → API
                           ↓
                      DataLoader
                           ↓
                       Station
                           ↓
                      Decorator → Display
```

## 🐛 Dépannage

### Erreur : "No module named 'weather_app'"

**Solution** : Vous devez lancer l'application depuis la racine du projet
```bash
cd Weather
python -m weather_app
```

### Erreur : "UnicodeEncodeError" (Windows)

**Solution** : Le fichier `menu.py` doit contenir la gestion UTF-8 au début
```python
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
```

### Docker : Impossible d'interagir avec les menus

**Solution** : Utilisez `docker-compose run` au lieu de `docker-compose up`
```bash
docker-compose run --rm weather_app
```

### Docker : Conteneur déjà existant

**Solution** : Supprimer l'ancien conteneur
```bash
docker rm -f weather_app
docker-compose run --rm weather_app
```

### Configuration non persistée dans Docker

**Solution** : Vérifier que le volume est bien monté dans `docker-compose.yml`
```yaml
volumes:
  - ./data:/app/data
```

## 📝 Notes Techniques

- Les données de configuration sont stockées avec des UUID courts (8 caractères)
- Le terminal est nettoyé à chaque changement de menu pour une meilleure lisibilité
- Les mesures sont affichées par jour et par heure
- La validation des URLs API est faite lors de l'ajout d'une station
- Le pattern Singleton garantit une seule instance de configuration
- Les tests utilisent des mocks pour éviter les appels API réels

## 🔐 Sécurité

- Aucune donnée sensible n'est stockée
- Les URLs API sont publiques
- Pas d'authentification requise pour les APIs de Toulouse Métropole

## 🌍 APIs Supportées

L'application fonctionne avec toute API retournant des données au format :
```json
{
  "results": [
    {
      "heure_de_paris": "ISO 8601 datetime",
      "temperature_en_degre_c": float,
      "humidite": int,
      "pression": int
    }
  ]
}
```

**APIs testées** :
- ✅ Toulouse Métropole Open Data (stations météo)

## 🤝 Contribution

Ce projet est un exemple d'application des principes du Clean Code et des design patterns en Python. Il suit les conventions :

- **PEP 8** : Style de code Python
- **Type hints** : Annotations de types
- **Docstrings** : Documentation des fonctions
- **Tests unitaires** : Couverture de code
- **SOLID** : Principes de conception orientée objet

## 📄 Licence

Ce projet est à but éducatif.

## 👥 Auteurs

Projet réalisé dans le cadre du cours d'Algorithmique et Développement - M1 EIA.

---

**🌤️ Bonnes prévisions météo !**