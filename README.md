# 🌦️Weather App — Application Météo Orientée Objet

## 🧭 Description du projet

**Toulouse Metro Weather** est une application Python permettant d’afficher et de gérer les données météorologiques des **stations de métro de Toulouse**.  
L’architecture du projet a été conçue selon les **principes du Clean Code et de SOLID**, afin de garantir **modularité, extensibilité et maintenabilité**.

L’application permet :
- De **récupérer des données météo** en temps réel via une API.  
- D’**afficher** les informations par **station**, **ville** ou **pays**.  
- D’**ajouter**, **supprimer** ou **actualiser** facilement des stations et des villes.  
- De **sauvegarder et charger** la configuration (stations, villes, API, etc.).  

> 🔭 À terme, le projet a vocation à accueillir d'autres villes et réseaux de transport.

---

## 🧱 Architecture logicielle

Le projet repose sur une architecture orientée objet et modulaire, respectant les principes **SOLID** :

- **S – Single Responsibility** : chaque classe a une responsabilité unique (extraction, affichage, sauvegarde, etc.).  
- **O – Open/Closed** : le code est ouvert à l’extension (nouvelles sources de données, nouveaux types de stations) mais fermé à la modification.  
- **L – Liskov Substitution** : les classes dérivées peuvent remplacer leurs classes mères sans casser le comportement.  
- **I – Interface Segregation** : les interfaces sont fines et spécifiques (ex. `IAffichable`).  
- **D – Dependency Inversion** : les dépendances sont abstraites (via `DataExtract`, `SaveAndLoad`, etc.), facilitant les tests et la maintenance.

---

## 🗺️ Diagramme UML

Le diagramme suivant illustre les relations entre les principales classes, interfaces et gestionnaires de l’application :
![Diagramme UML](https://uml.planttext.com/plantuml/svg/bLRTRjem5Bv7uXqiRaQxfj9kemereocBL08ZTDfTv2Q6UWfEv2JLfdKFqEVgYys_YGC6KYw0-1mVd-yxvtpnRLb1MjMxR3Zu19mJ7suFmhM_klUcVWJyDPW-U574_dfVe_NA2zP-T3u69XMY6vWW47YR3KwUuLE6mD_X0B3FPoYM48tJd124ol652ygA3WV_XeFX03wn_p2fG9B1iWHti8B-RxcY0snH5QTiVLpcDKsGsCrYf3Yfx44Y-88yaZxaC6s2b6mjhl9uWpCqBc3rBCCeQyPSumtDTuTsSS1v5lsVZAxfEbY4uCu7TuimV7_hmvtC-0U6tZ8uH5pJx02kIT7Dg-EepVtIrEMTlx-jtzyMVVEBAbZXdEW47PBlL1758qipXWKsbrInTTvY3SciKKrTiz3d-aHQawg66IwxzZ0dI92Y4tISIJUqDbnVlqxCzkHqIMmpL78F0Z55ohjiW9PgmGNixEf6sIVAoeDXH4tSfp7o80o1ZieXy2MZxCeK5v36ZEMnPffvgiCr8R_oseZLE5u1ineDHt88wgAWU6VPPN9f9MJqPGGkMREDBaTj8bPFmRGnWXzhp1dhojdAMtuBlZz-P7woLd7skxE0VrZzbknRBMoDj5rh_GKFCYZlABkBFfn7FdRs2u-XkqS4dEpLJtYCnRShSKZH4L5DreMj7vapF-9A57h1gZ-79aYF9rUs4gvovKmQZGQBmWLUKLnO8RL-RG7sFKytxnKufCMQhTA6ZaQPYg6FKR_DA7MdmzXWASenLy69WV2Odz3p8-hGVPkTh-_S3n_xbdMEI3s716uHFNmbxvWnPf904bp0R4znEqwcP1tp4LKzxM5MgkkOFEUun3JE2srZrmh1Y8d09kCzn6KHtWUpnvN7fw8lSTESRF1sZped4QjnSqDeieUKkSNIFBumttlixb6_e2saQSUXqTi-2BpbyY6OVYX_DfXDrctVoU7ILmO3aji5R6Ydg1hAEX8gHaCPcXbHDl6IY-L82DtZ-oOMxLKDurgan-fjDezxN07KNj5mEud6DST0LONMf5C6pXSNUmL5FqhGhL4Ifv_tEDFBDa1MMpTlxT99TZYuHIGLb_d_)  
