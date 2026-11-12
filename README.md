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

## Présentation des APK sur l’accueil ZAPIKI

La page d’accueil ZAPIKI présente désormais le téléchargement sans Play Store dans une section autonome, conçue sur le modèle visuel « Un seul lecteur. Vos propres sources. ». La présentation mentionne les variantes Universal, ARM 32 bits et ARM 64 bits et renvoie à `/zapiki/download/`. La section est traduite en dix langues. Le texte auparavant ajouté sous les boutons principaux a été retiré.

## Affichage mobile du téléchargement APK ZAPIKI

Le bloc d'illustration de fichiers APK est masqué sur téléphone et tablette compacte (largeur CSS jusqu'à 800 px). Le titre, l'explication, les pastilles de compatibilité et le bouton de téléchargement restent visibles et espacés. Les dix pages linguistiques utilisent une URL CSS versionnée afin d'éviter les anciennes feuilles de style en cache. Le déploiement du domaine central recopie la branche principale de `Zapiki-Website`.

## Mise à jour ZAPIKI du 12 novembre 2026

Le téléchargement public ZAPIKI a été mis à jour de **1.0.0.0** vers **1.0.0.1** dans `kama54/Zapiki-Website` (branche `main`). La release officielle `kama54/Zapiki-Downloads/releases/tag/v1.0.0.1` contient les trois APK Release signés (Universal, ARM32 et ARM64). Ce commit de synchronisation déclenche l'assemblage et le déploiement du domaine principal `gogostudio.app`, qui recopie la version actuelle des sites applicatifs.
