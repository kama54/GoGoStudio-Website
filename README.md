# GoGoStudio — site officiel

Site central des applications Android de GoGoStudio. Les pages sont construites automatiquement à partir des dépôts publics `Stopododo-Website`, `ClikoSpido-Website` et `Zapiki-Website`, qui restent inchangés.

- Accueil : https://gogostudio.app/
- Stopododo : https://gogostudio.app/stopododo/
- ClikoSpido Launcher : https://gogostudio.app/clikospido/
- ZAPIKI : https://gogostudio.app/zapiki/

L'activation de GitHub Pages et la configuration du domaine dans Settings > Pages sont nécessaires avant le basculement DNS. Ne pas modifier les URLs existantes des pages légales référencées sur Google Play.

## Guides ClikoSpido

Les guides du dépôt source `ClikoSpido-Website` présentent désormais, en dix langues, les solutions concrètes proposées par ClikoSpido Launcher (grandes touches, proches avec photos, Mode Famille). Chaque guide conserve ses conseils Android et ajoute un lien direct vers Google Play. Les guides sont intégrés automatiquement au site officiel `https://gogostudio.app/clikospido/` à chaque publication GitHub Pages.

## Vidéos Stopododo : balisage Google (10 novembre 2026)

Les dix pages de vidéos promotionnelles de Stopododo possèdent désormais `VideoObject.uploadDate` (date ISO 8601 sourcée du premier commit public des MP4, 31 octobre 2026). Cela corrige l'alerte Search Console « Champ uploadDate manquant ». Aucun fichier vidéo, visuel ou contenu commercial n'est modifié. Le déploiement de `gogostudio.app` reprend les pages du dépôt source `Stopododo-Website`.

## Publication du site unifié

Le dépôt `GoGoStudio-Website` construit et publie le domaine `gogostudio.app` en récupérant les branches `main` de chacun des trois dépôts `*-Website`. Un déploiement GitHub Pages du dépôt d'une application ne suffit donc **pas** à mettre à jour son sous-dossier sur `gogostudio.app`.

Après une modification de `Zapiki-Website`, `Stopododo-Website` ou `ClikoSpido-Website`, relancer le workflow **« Publier GoGoStudio et les trois sites »** dans ce dépôt (onglet Actions > Run workflow), ou déclencher une publication via un nouveau commit sur `main`. Une publication planifiée est également configurée chaque matin à 05 h 17 UTC.
