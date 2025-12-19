# 🌤️ Application Météo - Clean Code & Design Patterns

Application Python complète pour consulter les données météorologiques, développée selon les principes du Clean Code et utilisant plusieurs design patterns.

## 📁 Structure du Projet

```
weather_app/
├── __main__.py                 # Point d'entrée de l'application
├── __init__.py                 # Initialisation du package
├── requirements.txt            # Dépendances Python
├── config/
│   ├── __init__.py
│   └── singleton_config.py     # Pattern Singleton pour la configuration
├── models/
│   ├── __init__.py
│   ├── location.py             # Classes Pays, Ville, Station (héritage)
│   ├── measurement.py          # Classe Measurement
│   └── builders.py             # Pattern Builder pour Station et Ville
├── data_structures/
│   ├── __init__.py
│   ├── linked_list.py          # Liste Chaînée pour les stations
│   └── queue.py                # File pour les requêtes API
├── patterns/
│   ├── __init__.py
│   ├── observer.py             # Pattern Observer
│   ├── decorator.py            # Pattern Decorator
│   └── command.py              # Pattern Command
├── services/
│   ├── __init__.py
│   └── api_service.py          # Service d'appel à l'API
└── ui/
    ├── __init__.py
    └── menu.py                 # Interface utilisateur
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

## 🚀 Installation

1. Cloner le projet :
```bash
cd weather_app
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## ▶️ Lancement

```bash
python __main__.py
```

ou

```bash
python -m weather_app
```

## 📋 Utilisation

### Premier lancement

Au premier lancement, aucune donnée n'est configurée. Vous devez :

1. Aller dans **Configuration**
2. Ajouter un **Pays**
3. Ajouter une **Ville** (liée au pays)
4. Ajouter une **Station** (liée à la ville)

### Navigation

L'application propose plusieurs menus :

#### Menu Principal
- Voir la météo
- Configuration
- Quitter

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

**Configuration :**
1. Ajouter pays : `France`
2. Ajouter ville : `Toulouse` (lié à France)
3. Ajouter station : `Montaudran` (lié à Toulouse) avec l'URL ci-dessus

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

## 💾 Stockage

La configuration est sauvegardée dans `config.json` et persiste entre les sessions.

## 🎨 Fonctionnalités

- ✅ Affichage des mesures météo (température, humidité, pression)
- ✅ Rafraîchissement des données en temps réel
- ✅ Gestion hiérarchique : Pays → Ville → Station
- ✅ Interface terminal avec nettoyage d'écran
- ✅ Navigation intuitive par numéros
- ✅ Validation des URLs API
- ✅ Gestion des erreurs réseau

## 🧪 Architecture Technique

### Séparation des Responsabilités

- **Models** : Entités métier (Pays, Ville, Station, Measurement)
- **Services** : Logique métier (ApiService)
- **Patterns** : Comportements réutilisables
- **Data Structures** : Structures personnalisées
- **UI** : Interface utilisateur

### Flux de Données

1. L'utilisateur sélectionne une station (via UI)
2. Le pattern **Command** encapsule l'action
3. Le pattern **Observer** détecte la sélection
4. L'**ApiService** récupère les données (via Queue)
5. Le pattern **Decorator** formate l'affichage

## 📝 Notes

- Les données de configuration sont stockées avec des UUID courts (8 caractères)
- Le terminal est nettoyé à chaque changement de menu pour une meilleure lisibilité
- Un maximum de 20 mesures est affiché par défaut (configurable dans le décorateur)
- La validation des URLs API est faite lors de l'ajout d'une station

## 🤝 Contribution

Ce projet est un exemple d'application des principes du Clean Code et des design patterns en Python.