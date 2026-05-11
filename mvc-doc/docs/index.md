# CSB Blog

Bienvenue dans la documentation de **CSB Blog**, un blog minimaliste développé en **PHP** sans framework, selon une architecture **MVC** (Modèle–Vue–Contrôleur).

## Vue d'ensemble

Le projet sert de base pédagogique : code lisible, séparation Modèle / Vue / Contrôleur, et extension possible sans dépendances Composer obligatoires.

### Technologies principales

| Élément | Détail |
|--------|--------|
| Langage | PHP 7.4 ou supérieur |
| Base de données | MySQL 8 (ex. conteneur Docker du dépôt) |
| Architecture | MVC |
| Dépendances PHP | Aucune (PHP natif, PDO) |

## Fonctionnalités principales

- Liste des articles avec pagination
- Lecture d’un article et commentaires associés
- Inscription, connexion, déconnexion, profil
- Recherche d’articles
- Espace administrateur (création d’articles, suppression, gestion des commentaires et des utilisateurs, restriction de comptes)
- Journalisation des actions dans des fichiers datés sous `logs/`

## Sécurité et qualité (aperçu honnête)

- **Requêtes SQL** : PDO avec requêtes préparées et paramètres nommés
- **Affichage** : usage d’`htmlspecialchars()` pour limiter le risque XSS dans les vues
- **Mots de passe** : `password_hash` / `password_verify` avec l’algorithme configuré dans le code (`CRYPT_SHA256`)
- **Sessions** : authentification et contrôle admin côté serveur

**Limites connues** : les formulaires ne mettent pas en œuvre de jetons **CSRF** ; en environnement exposé, il convient d’ajouter une protection CSRF et les en-têtes HTTP adaptés (voir [Sécurité](securite.md)).

## Organisation de cette documentation

| Section | Rôle (Diátaxis) |
|--------|------------------|
| [Installation](installation.md) | Mettre en route le projet (local ou Docker), base de données, logs |
| [Guide utilisateur](guide-utilisateur.md) | Utiliser le site (compte, articles, commentaires, admin) |
| [Développement](developpement.md) | Contribuer, conventions, extension du code |
| [Architecture](architecture.md) | Routage, flux de requête, rôle des dossiers |
| [Base de données](base-donnees.md) | Schéma réel, relations, exemples SQL |
| [Sécurité](securite.md) | Mesures en place, risques résiduels, recommandations |

---

**Dernière mise à jour** : 2026
