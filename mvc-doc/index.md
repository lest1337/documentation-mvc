# CSB Blog

Bienvenue dans la documentation de **CSB Blog**, un blog minimaliste et léger développé en PHP natif suivant une architecture MVC (Model-View-Controller).

## Vue d'ensemble

CSB Blog est une plateforme de blogging simple et efficace conçue à des fins pédagogiques. Le projet propose une base propre, une architecture compréhensible et maintenable, ainsi qu'une grande extensibilité et personnalisabilité.

### Technologies principales

- **Langage**: PHP 7+
- **Base de données**: MySQL
- **Architecture**: MVC (Model-View-Controller)
- **Dépendances externes**: Aucune

## Fonctionnalités principales

- Affichage des articles (posts) avec paginaison
- Système de commentaires sur les articles
- Gestion des utilisateurs (inscription, connexion, profil)
- Recherche d'articles
- Tableau de bord administrateur
- Système de journalisation (logging) des actions
- Interface utilisateur responsive

## Points clés

### Sécurité

- Sécurisation des routes avec vérification d'authentification
- Protection contre les injections SQL via les requêtes préparées PDO
- Protection contre les attaques CSRF
- Hachage sécurisé des mots de passe avec CRYPT_SHA256

### Architecture propre

- Séparation claire entre Modèles, Vues et Contrôleurs
- Routage simple basé sur les paramètres GET
- Pas de framework, code PHP natif pour une meilleure compréhension
- Structure organisée et facilement extensible

## À propos du projet

Ce projet a été créé à titre d'exemple pédagogique pour montrer comment construire une application PHP structurée et sécurisée sans dépendre d'un framework externe. Il est idéal pour apprendre les concepts fondamentaux du développement web.

## Navigation

Cette documentation est organisée en plusieurs sections :

- **Installation**: Comment configurer et lancer le projet
- **Architecture**: Description de la structure MVC et de l'organisation du code
- **Guide Utilisateur**: Utilisation de l'application (pour les utilisateurs finaux)
- **API & Modèles**: Documentation technique détaillée des modèles
- **Contrôleurs**: Documentation des contrôleurs et des routes
- **Base de Données**: Schéma et structure des données
- **Sécurité**: Mesures de sécurité implémentées
- **Développement**: Guide pour contribuer et étendre le projet

---

**Version**: 1.0  
**Dernier mise à jour**: 2026  
**Auteur**: Equipe de développement
