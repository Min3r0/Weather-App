# 🌦️ Weather App – Application météo en Python

## 📌 Description

**Weather App** est une application météo en ligne de commande développée en **Python**, permettant de consulter, gérer et afficher des données météorologiques provenant d’APIs publiques.

Le projet a été conçu dans un objectif **pédagogique et professionnel**, en respectant rigoureusement :

* les **principes du Clean Code**
* l’utilisation de **structures de données complexes**
* l’implémentation de **Design Patterns reconnus**

---

## 🎯 Objectifs du projet

* Concevoir une application modulaire et maintenable
* Appliquer plusieurs **Design Patterns** de manière cohérente
* Manipuler des **structures de données complexe**
* Séparer clairement les responsabilités (architecture propre)
* Fournir une interface utilisateur simple en ligne de commande

---

## 🧱 Architecture du projet

```text
weather_app/
├── __main__.py
├── config/
│   ├── __init__.py
│   └── config_singleton.py
├── models/
│   ├── __init__.py
│   ├── measurement.py
│   ├── station.py
│   └── linked_list.py
├── patterns/
│   ├── __init__.py
│   ├── builder.py
│   ├── command.py
│   ├── decorator.py
│   └── observer.py
├── services/
│   ├── __init__.py
│   ├── api_queue.py
│   └── api_service.py
└── ui/
    ├── __init__.py
    └── display.py
```

---

## 🧼 Respect des principes du Clean Code

Le projet respecte les règles fondamentales du **Clean Code** :

### ✔ Lisibilité

* Nommage explicite des classes, méthodes et variables
* Méthodes courtes et spécialisées
* Commentaires utiles et non redondants

### ✔ Responsabilité unique (SRP)

* `APIService` : récupération des données
* `WeatherApp` : gestion de l’interface utilisateur
* `Station` / `Measurement` : modèles de données
* `ConfigSingleton` : gestion de la configuration

### ✔ Faible couplage / forte cohésion

* Modules indépendants
* Communication via interfaces et patterns

### ✔ Extensibilité

* Ajout facile de nouvelles stations
* Possibilité d’ajouter d’autres sources météo ou types d’affichage

---

## 🗂️ Structures de données complexes utilisées

### 🔗 Liste chaînée personnalisée

**`LinkedList`**

* Stockage dynamique des stations météo
* Implémentation manuelle avec `Node`
* Méthodes : `append`, `get`, `find_by_name`, `to_list`

👉 Permet de démontrer la maîtrise des structures de données non natives.

---

### 📦 File (Queue)

**`APIQueue`**

* Basée sur `collections.deque`
* Gestion des rafraîchissements API
* Traitement séquentiel des requêtes

---

### 🗺️ Dictionnaires imbriqués

**Configuration des stations**

```json
countries → cities → stations
```

* Organisation hiérarchique des données
* Stockage persistant via JSON

---

## 🧩 Design Patterns implémentés

### 🟢 Singleton

**`ConfigSingleton`**

* Une seule instance de configuration
* Centralisation des paramètres
* Chargement et sauvegarde automatique

---

### 🟡 Builder

**`StationBuilder`**

* Construction contrôlée des objets `Station`
* Lisibilité et sécurité lors de l’instanciation

---

### 🔵 Command

**Commandes utilisateur**

* `SelectStationCommand`
* `RefreshDataCommand`
* `QuitCommand`
* `UpdateStationURLCommand`

👉 Encapsulation des actions utilisateur pour une meilleure extensibilité.

---

### 🟣 Observer

**Chargement automatique des données**

* Lorsqu’une station est sélectionnée
* Découplage entre l’UI et le service API

---

### 🟠 Decorator

**`MeasurementDisplayDecorator`**

* Ajout dynamique de fonctionnalités d’affichage
* Formatage avancé des données météo
* Respect du principe Open/Closed

---

## 🖥️ Fonctionnalités

* 📍 Sélection de stations météo
* 🔄 Rafraîchissement des données
* ➕ Ajout de nouvelles stations
* ✏️ Modification dynamique des URLs
* 📊 Affichage des mesures par date et heure
* 💾 Sauvegarde persistante (JSON)

---

## 🚀 Lancement de l’application

### Prérequis

* Python **3.9+**
* Bibliothèque :

```bash
pip install requests
```

### Exécution

```bash
python -m weather_app
```

---

## 📈 Améliorations possibles

* Interface graphique (GUI)
* Export CSV / JSON des données météo
* Tests unitaires
* Gestion du cache API
* Multithreading pour les appels API

---

## 👨‍💻 Auteur

Projet développé dans un objectif **académique**, mettant en pratique :

* Clean Code
* Programmation Orientée Objet
* Design Patterns
* Structures de données avancées
