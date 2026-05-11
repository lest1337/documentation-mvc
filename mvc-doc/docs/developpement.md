# Guide de développement

Ce guide s’adresse aux personnes qui modifient ou étendent **blog-mvc** (CSB Blog).

## Démarrage rapide

1. Cloner le dépôt et se placer à la racine du projet (répertoire contenant `index.php`).
2. Importer la base : voir [Installation](installation.md) (`db/blog.sql` puis `db/blog.ext.sql`, ou `./scripts/db-reset.sh`).
3. Définir les variables `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` si vos identifiants diffèrent des défauts dans `app/models/db.inc.php`.
4. Lancer `php -S localhost:8080` (ou le port de votre choix).

## Organisation des fichiers

| Emplacement | Rôle |
|-------------|------|
| `app/controllers/main.php` | Fonction `rout($action)` : table de correspondance action → fichier contrôleur |
| `app/controllers/*.php` | Contrôleurs (sauf `main.php` chargé par `index.php`) |
| `app/models/*.inc.php` | Modèles et utilitaires (`db.inc.php`, `auth.inc.php`, etc.) |
| `app/views/*.view.php` | Vues ; en-tête et pied communs dans `header.view.php` / `footer.view.php` |
| `db/blog.sql` | Schéma (destructif : recrée la base `blog`) |
| `db/blog.ext.sql` | Données de démo |
| `scripts/db-reset.sh` | Menu interactif (Gum + Docker ou MySQL local) pour réappliquer schéma / données |

**Commentaires** : `post.php` inclut `comment.php` pour le formulaire et l’affichage des commentaires sur la page article. Ce n’est pas une route séparée dans `rout()`.

## Connexion base de données

`getPdo()` lit `getenv("DB_HOST")`, `getenv("DB_USER")`, `getenv("DB_PASSWORD")`, `getenv("DB_NAME")` avec des valeurs par défaut documentées dans [Installation](installation.md). Pas de chargeur `.env` dans le dépôt de base : export shell, configuration du serveur web, ou évolution maison.

## Ajouter une route

1. Créer `app/controllers/ma_fonctionnalite.php` et la vue associée sous `app/views/`.
2. Dans `app/controllers/main.php`, ajouter une ligne dans le tableau `$actions`, par exemple `"ma_route" => "ma_fonctionnalite.php"`.
3. Tester avec `index.php?action=ma_route`.

## Conventions du projet

| Élément | Convention |
|---------|------------|
| Fichiers modèles | suffixe `.inc.php` |
| Fichiers vues | suffixe `.view.php` |
| Tables / colonnes SQL | en général **MAJUSCULES** dans le code et les scripts (`USERS`, `USER_ID`, …) |
| Requêtes | PDO préparé, paramètres nommés (`:email`, …) |
| Indentation | 4 espaces |

## Journalisation

```php
Logger::log("NOM_ACTION", ["cle" => "valeur"]);
```

Les fichiers sont créés sous `logs/` ; le répertoire est créé automatiquement si les droits le permettent.

## Gestion des erreurs

- Les modèles utilisent en général PDO en mode exception.
- Les contrôleurs assignent souvent `$error` ou redirigent avec `header("Location: …")` après une action POST réussie.

## Qualité et vérifications manuelles

```bash
find app -name "*.php" -exec php -l {} \;
php -l index.php
```

Tester les routes critiques : accueil, inscription, connexion, article, commentaire, admin (compte admin).

## Déploiement (rappel)

- Variables d’environnement `DB_*` sur l’hôte ou dans la configuration du conteneur.
- Ne pas exposer `display_errors` en production.
- Prévoir HTTPS et durcissement des sessions au niveau serveur.

---

Voir aussi : [Architecture](architecture.md), [Base de données](base-donnees.md), [Sécurité](securite.md), [Installation](installation.md)
