# Installation et configuration

Ce guide décrit comment installer **blog-mvc** (CSB Blog) et préparer la base MySQL, en local ou avec Docker.

## Prérequis

| Composant | Version / remarque |
|-----------|-------------------|
| PHP | 7.4 ou supérieur (extensions PDO MySQL) |
| MySQL | 8 recommandé (compatible avec le `docker-compose` du dépôt) |
| Git | Pour cloner le dépôt |
| Docker (optionnel) | Docker Compose v2 pour la pile PHP + MySQL |

Aucune dépendance Composer n’est requise pour l’application elle-même.

## 1. Obtenir le code

```bash
git clone <url-du-depot> blog-mvc
cd blog-mvc
```

Le répertoire de travail doit contenir `index.php`, le dossier `app/`, `db/`, etc.

## 2. Base de données

### Fichiers SQL

| Fichier | Rôle |
|---------|------|
| `db/blog.sql` | Supprime la base `blog` si elle existe, recrée la base et les tables (`USERS`, `POSTS`, `COMMENTS`) |
| `db/blog.ext.sql` | Données de démonstration (à exécuter **après** `blog.sql`) |

Le script `blog.sql` exécute `DROP DATABASE IF EXISTS blog` : le compte MySQL utilisé pour l’import doit avoir les droits suffisants (souvent l’utilisateur `root` en développement).

### Import en ligne de commande (hôte)

```bash
mysql -h 127.0.0.1 -u root -p < db/blog.sql
mysql -h 127.0.0.1 -u root -p < db/blog.ext.sql
```

Adaptez `-h`, `-u` et le mot de passe à votre installation.

### Réinitialiser ou initialiser la base (script interactif)

Depuis la racine du dépôt, le script `scripts/db-reset.sh` propose un menu interactif (outil [Charm Gum](https://github.com/charmbracelet/gum)) :

**Prérequis** : `gum` installé ; pour le mode **MySQL local**, le client `mysql` sur la machine hôte. Pour le mode **Docker**, le service `db` doit être joignable (`docker compose up -d`).

- Choix **Docker** ou **MySQL local**
- Actions possibles : schéma seul, schéma + données de démo, ou (Docker) suppression du volume puis recréation avec confirmation à chaque étape sensible

En mode local, le script demande **hôte**, **utilisateur** et **mot de passe** (saisie masquée) sans valeurs par défaut imposées.

```bash
chmod +x scripts/db-reset.sh   # une seule fois si besoin
./scripts/db-reset.sh
```

## 3. Variables d’environnement (connexion MySQL)

La connexion est définie dans `app/models/db.inc.php` via `getenv()` avec des **valeurs par défaut** si les variables ne sont pas définies :

| Variable | Défaut |
|----------|--------|
| `DB_HOST` | `127.0.0.1` |
| `DB_USER` | `admin` |
| `DB_PASSWORD` | `root` |
| `DB_NAME` | `blog` |

**Exemple** sous Linux ou macOS avant de lancer le serveur PHP :

```bash
export DB_HOST=127.0.0.1
export DB_USER=mon_utilisateur
export DB_PASSWORD=mon_mot_de_passe
export DB_NAME=blog
php -S localhost:8080
```

Avec **Docker Compose** du dépôt, les variables sont déjà fixées pour le service `php` (hôte `db`, utilisateur `admin`, etc.) — voir la section Docker ci-dessous.

Le dépôt ne fournit pas de chargeur `.env` intégré : vous pouvez exporter les variables dans votre shell, les définir dans la configuration du serveur web, ou étendre le projet pour lire un fichier `.env` (hors scope de ce guide).

## 4. Répertoire des journaux (`logs/`)

- Le dossier `logs/` est en général **absent** après un clone (souvent listé dans `.gitignore`).
- La classe `Logger` (`app/models/logger.inc.php`) **crée le répertoire** `logs/` au besoin avant d’écrire un fichier du type `YYYY-MM-DD.log`.

Si l’écriture échoue (droits du système de fichiers), créez le dossier manuellement :

```bash
mkdir -p logs
chmod 755 logs
```

## 5. Lancer l’application

### Serveur de développement PHP

À la racine du projet :

```bash
php -S localhost:8080
```

Ouvrez `http://localhost:8080` (ou le port indiqué). Le routeur utilise `index.php` et le paramètre GET `action`.

### Docker Compose

Fichier `docker-compose.yml` à la racine : services `php` (Apache + PHP, port **8000** exposé) et `db` (MySQL 8).

```bash
docker compose up --build
```

Application : **http://localhost:8000**. La base est initialisée avec les identifiants du fichier Compose ; pour réinjecter le schéma ou les données, utilisez `./scripts/db-reset.sh` en mode Docker ou importez les SQL comme ci-dessus.

## 6. Vérification rapide

1. Page d’accueil sans erreur PDO.
2. Inscription d’un utilisateur puis connexion.
3. Présence de fichiers dans `logs/` après une action journalisée.

## Problèmes courants

### Unknown database ou erreur de connexion

- MySQL démarré et base `blog` créée (exécuter `db/blog.sql`).
- Variables `DB_*` cohérentes avec le compte réel.

### Avertissement ou erreur sur `logs/`

- Vérifier les droits du répertoire projet ; le code tente de créer `logs/` automatiquement.

### Page blanche

- Activer temporairement l’affichage des erreurs PHP pour diagnostiquer (uniquement en développement).

---

Voir aussi : [Architecture](architecture.md), [Base de données](base-donnees.md), [Développement](developpement.md)
