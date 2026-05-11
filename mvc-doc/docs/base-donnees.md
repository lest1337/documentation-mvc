# Base de données

Référence alignée sur les scripts du dépôt : `db/blog.sql` (schéma) et `db/blog.ext.sql` (données de démonstration).

## Base et encodage

- **Nom de la base** : `blog` (recréée par `blog.sql` : suppression puis création).
- **Moteur** : tables créées par défaut selon la configuration MySQL du serveur (en pratique InnoDB).
- **Jeu de caractères** : non forcé dans `blog.sql` ; en production, prévoir `utf8mb4` explicitement si besoin.

## Tables et colonnes

### `USERS`

| Colonne | Type (script) | Contraintes / défaut | Description |
|---------|---------------|----------------------|-------------|
| `USER_ID` | `INT` | `AUTO_INCREMENT`, clé primaire | Identifiant |
| `USERNAME` | `VARCHAR(32)` | | Nom affiché |
| `EMAIL` | `VARCHAR(64)` | | Email (connexion) |
| `PSSWRD` | `VARCHAR(128)` | | Mot de passe haché (voir application PHP) |
| `IS_ADMIN` | `TINYINT(1)` | défaut `0` | Droit administrateur |
| `IS_RESTRICTED` | `TINYINT(1)` | défaut `0` | Compte restreint (ex. ne peut plus commenter) |

### `POSTS`

| Colonne | Type (script) | Contraintes / défaut | Description |
|---------|---------------|----------------------|-------------|
| `POST_ID` | `INT` | `AUTO_INCREMENT`, clé primaire | Identifiant |
| `TITLE` | `VARCHAR(32)` | | Titre |
| `CONTENT` | `TEXT` | | Corps de l’article |
| `PUBLISH_DATE` | `DATETIME` | défaut `NOW()` | Date de publication |

Il n’y a **pas** de colonne auteur dans le schéma SQL livré : l’application ne relie pas formellement un article à un `USER_ID` au niveau base dans ce fichier.

### `COMMENTS`

| Colonne | Type (script) | Contraintes / défaut | Description |
|---------|---------------|----------------------|-------------|
| `COMMENT_ID` | `INT` | `AUTO_INCREMENT`, clé primaire | Identifiant |
| `CONTENT` | `TEXT` | | Texte du commentaire |
| `USER_ID` | `INT` | `FOREIGN KEY` → `USERS(USER_ID)` | Auteur du commentaire |
| `POST_ID` | `INT` | `FOREIGN KEY` → `POSTS(POST_ID)` | Article commenté |

Les clés étrangères sont déclarées **sans** `ON DELETE CASCADE` dans `blog.sql` : le comportement à la suppression d’un post ou d’un utilisateur dépend des règles MySQL et du code applicatif.

## Relations (prose)

- Un **utilisateur** (`USERS`) peut être référencé par **plusieurs** commentaires (`COMMENTS.USER_ID`).
- Un **article** (`POSTS`) peut être référencé par **plusieurs** commentaires (`COMMENTS.POST_ID`).
- Chaque **commentaire** référence au plus un utilisateur et un article via les clés étrangères.

## DDL de référence (extrait du dépôt)

Le fichier source canonique est `db/blog.sql`. En résumé, il contient notamment :

```sql
USE blog;

CREATE TABLE IF NOT EXISTS USERS (
    USER_ID INT AUTO_INCREMENT PRIMARY KEY,
    USERNAME VARCHAR(32),
    EMAIL VARCHAR(64),
    PSSWRD VARCHAR(128),
    IS_ADMIN TINYINT(1) DEFAULT 0,
    IS_RESTRICTED TINYINT(1) DEFAULT 0
);

CREATE TABLE IF NOT EXISTS POSTS (
    POST_ID INT AUTO_INCREMENT PRIMARY KEY,
    TITLE VARCHAR(32),
    CONTENT TEXT,
    PUBLISH_DATE DATETIME DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS COMMENTS (
    COMMENT_ID INT AUTO_INCREMENT PRIMARY KEY,
    CONTENT TEXT,
    USER_ID INT,
    POST_ID INT,
    FOREIGN KEY (USER_ID) REFERENCES USERS(USER_ID),
    FOREIGN KEY (POST_ID) REFERENCES POSTS(POST_ID)
);
```

## Données de démonstration (`db/blog.ext.sql`)

Ce fichier insère des lignes dans `USERS`, `POSTS` et `COMMENTS` **après** que le schéma existe. Les mots de passe sont des chaînes hachées de démonstration : en environnement réel, régénérez des utilisateurs via l’application ou adaptez les inserts.

## Exemples de requêtes (schéma actuel)

### Commentaires d’un article avec nom d’utilisateur

```sql
SELECT c.COMMENT_ID, c.CONTENT, c.USER_ID, u.USERNAME
FROM COMMENTS c
JOIN USERS u ON u.USER_ID = c.USER_ID
WHERE c.POST_ID = :postId
ORDER BY c.COMMENT_ID;
```

### Nombre de commentaires par article

```sql
SELECT p.POST_ID, p.TITLE, COUNT(c.COMMENT_ID) AS nb_commentaires
FROM POSTS p
LEFT JOIN COMMENTS c ON c.POST_ID = p.POST_ID
GROUP BY p.POST_ID, p.TITLE
ORDER BY nb_commentaires DESC;
```

### Recherche simple dans les titres d’articles

```sql
SELECT POST_ID, TITLE, PUBLISH_DATE
FROM POSTS
WHERE TITLE LIKE :motcle
ORDER BY PUBLISH_DATE DESC;
```

## Mots de passe côté application

L’application PHP utilise `password_hash()` et `password_verify()` avec l’algorithme passé dans le code (voir `app/models/utilisateur.inc.php`, constante `CRYPT_SHA256` dans ce projet). Les valeurs dans `blog.ext.sql` sont indépendantes et sertes à la démo SQL.

## Sauvegarde et restauration

```bash
mysqldump -h … -u … -p blog > sauvegarde_blog.sql
mysql -h … -u … -p blog < sauvegarde_blog.sql
```

---

Voir aussi : [Installation](installation.md), [Développement](developpement.md), [Sécurité](securite.md)
