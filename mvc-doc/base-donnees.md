# Base de Données

Cette section docummente la structure et le schéma de la base de données MySQL.

## Vue d'ensemble

La base de données `blog` utilise MySQL pour stocker tous les données de l'application. Elle est organisée en trois tables principales : `USERS`, `POSTS`, et `COMMENTS`.

**Caractéristiques:**
- Moteur: InnoDB (support des transactions)
- Encodage: UTF-8 (support multilingue)
- Relations: Clés étrangères (intégrité référentielle)

## Tables

### Table USERS

Stocke les informations des utilisateurs.

```
USERS
├── USER_ID (INT, PRIMARY KEY, AUTO_INCREMENT)
├── USERNAME (VARCHAR(100), UNIQUE)
├── EMAIL (VARCHAR(100), UNIQUE)
├── PSSWRD (VARCHAR(255))  // Haché avec CRYPT_SHA256
├── IS_ADMIN (TINYINT, DEFAULT 0)
└── CREATED_AT (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
```

**Détails des colonnes:**

| Colonne | Type | Contraintes | Description |
|---------|------|------------|-------------|
| `USER_ID` | INT | PRIMARY KEY, AUTO_INCREMENT | Identifiant unique |
| `USERNAME` | VARCHAR(100) | NOT NULL, UNIQUE | Nom d'utilisateur public |
| `EMAIL` | VARCHAR(100) | NOT NULL, UNIQUE | Email unique pour connexion |
| `PSSWRD` | VARCHAR(255) | NOT NULL | Mot de passe haché |
| `IS_ADMIN` | TINYINT | DEFAULT 0 | 0=utilisateur, 1=administrateur |
| `CREATED_AT` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Date de création |

**Schéma SQL:**

```sql
CREATE TABLE USERS (
    USER_ID INT AUTO_INCREMENT PRIMARY KEY,
    USERNAME VARCHAR(100) NOT NULL UNIQUE,
    EMAIL VARCHAR(100) NOT NULL UNIQUE,
    PSSWRD VARCHAR(255) NOT NULL,
    IS_ADMIN TINYINT DEFAULT 0,
    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**Index:**
- PRIMARY KEY sur `USER_ID`
- UNIQUE sur `USERNAME`
- UNIQUE sur `EMAIL`

---

### Table POSTS

Stocke les articles du blog.

```
POSTS
├── POST_ID (INT, PRIMARY KEY, AUTO_INCREMENT)
├── TITLE (VARCHAR(200))
├── CONTENT (LONGTEXT)
├── PUBLISH_DATE (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
└── AUTHOR_ID (INT, FOREIGN KEY -> USERS)
```

**Détails des colonnes:**

| Colonne | Type | Contraintes | Description |
|---------|------|------------|-------------|
| `POST_ID` | INT | PRIMARY KEY, AUTO_INCREMENT | Identifiant unique |
| `TITLE` | VARCHAR(200) | NOT NULL | Titre de l'article |
| `CONTENT` | LONGTEXT | NOT NULL | Contenu complet |
| `PUBLISH_DATE` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Date de publication |
| `AUTHOR_ID` | INT | FOREIGN KEY | Auteur (référence USERS) |

**Schéma SQL:**

```sql
CREATE TABLE POSTS (
    POST_ID INT AUTO_INCREMENT PRIMARY KEY,
    TITLE VARCHAR(200) NOT NULL,
    CONTENT LONGTEXT NOT NULL,
    PUBLISH_DATE TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    AUTHOR_ID INT,
    FOREIGN KEY (AUTHOR_ID) REFERENCES USERS(USER_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**Index:**
- PRIMARY KEY sur `POST_ID`
- FOREIGN KEY sur `AUTHOR_ID`
- INDEX sur `PUBLISH_DATE` (pour tri)

---

### Table COMMENTS

Stocke les commentaires sur les articles.

```
COMMENTS
├── COMMENT_ID (INT, PRIMARY KEY, AUTO_INCREMENT)
├── POST_ID (INT, FOREIGN KEY -> POSTS)
├── USER_ID (INT, FOREIGN KEY -> USERS)
├── CONTENT (TEXT)
└── CREATED_AT (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
```

**Détails des colonnes:**

| Colonne | Type | Contraintes | Description |
|---------|------|------------|-------------|
| `COMMENT_ID` | INT | PRIMARY KEY, AUTO_INCREMENT | Identifiant unique |
| `POST_ID` | INT | NOT NULL, FOREIGN KEY | Article commenté |
| `USER_ID` | INT | NOT NULL, FOREIGN KEY | Auteur du commentaire |
| `CONTENT` | TEXT | NOT NULL | Texte du commentaire |
| `CREATED_AT` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Date de création |

**Schéma SQL:**

```sql
CREATE TABLE COMMENTS (
    COMMENT_ID INT AUTO_INCREMENT PRIMARY KEY,
    POST_ID INT NOT NULL,
    USER_ID INT NOT NULL,
    CONTENT TEXT NOT NULL,
    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (POST_ID) REFERENCES POSTS(POST_ID) ON DELETE CASCADE,
    FOREIGN KEY (USER_ID) REFERENCES USERS(USER_ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**Index:**
- PRIMARY KEY sur `COMMENT_ID`
- FOREIGN KEY sur `POST_ID` (avec CASCADE delete)
- FOREIGN KEY sur `USER_ID`
- INDEX sur `POST_ID` (pour recherche rapide)

---

## Diagramme de relations

```
USERS
  ├── 1 ----< * POSTS
  └── 1 ----< * COMMENTS

POSTS
  ├── 1 ----< * COMMENTS
  └── * ----> 1 USERS (author)

COMMENTS
  ├── * ----> 1 USERS
  └── * ----> 1 POSTS
```

**Explicitation:**
- Un utilisateur peut créer plusieurs articles
- Un utilisateur peut laisser plusieurs commentaires
- Un article peut avoir plusieurs commentaires
- Un article appartient à un utilisateur
- Un commentaire appartient à un utilisateur et à un article

---

## Contraintes et intégrité

### Clés étrangères

Les clés étrangères garantissent l'intégrité des relations :

- `POSTS.AUTHOR_ID` -> `USERS.USER_ID`
  - Un article doit faire référence à un utilisateur valide
  
- `COMMENTS.POST_ID` -> `POSTS.POST_ID` avec CASCADE DELETE
  - Un commentaire doit faire référence à un article valide
  - Suppression d'un article supprime automatiquement ses commentaires
  
- `COMMENTS.USER_ID` -> `USERS.USER_ID`
  - Un commentaire doit faire référence à un utilisateur valide

### Actions de suppression

**CASCADE DELETE:**
- Quand un article est supprimé, tous ses commentaires sont supprimés automatiquement
- Quand un utilisateur est supprimé, ses articles restent (orphelins) - à améliorer

**Recommandation pour amélioration:**
```sql
ALTER TABLE POSTS ADD FOREIGN KEY (AUTHOR_ID) 
  REFERENCES USERS(USER_ID) ON DELETE SET NULL;
```

---

## Données de test

### Script d'initialisation (blog.sql)

Crée la structure de base avec quelques utilisateurs et articles d'exemple.

```sql
-- Utilisateurs de test
INSERT INTO USERS (USERNAME, EMAIL, PSSWRD, IS_ADMIN) VALUES
('admin', 'admin@blog.local', HASH('admin123'), 1),
('user1', 'user1@blog.local', HASH('password'), 0),
('user2', 'user2@blog.local', HASH('password'), 0);

-- Articles de test
INSERT INTO POSTS (TITLE, CONTENT, AUTHOR_ID) VALUES
('Premier article', 'Contenu du premier article...', 1),
('Deuxième article', 'Contenu du deuxième article...', 2);

-- Commentaires de test
INSERT INTO COMMENTS (POST_ID, USER_ID, CONTENT) VALUES
(1, 2, 'Très bon article!'),
(1, 3, 'Merci pour ce partage');
```

### Script d'extension (blog.ext.sql)

Ajoute des données supplémentaires pour le test et démonstration.

---

## Requêtes communes

### Récupérer un article avec commentaires

```sql
SELECT p.*, u.USERNAME as author_name,
       c.COMMENT_ID, c.CONTENT as comment_content, 
       u2.USERNAME as commenter_name
FROM POSTS p
LEFT JOIN USERS u ON p.AUTHOR_ID = u.USER_ID
LEFT JOIN COMMENTS c ON p.POST_ID = c.POST_ID
LEFT JOIN USERS u2 ON c.USER_ID = u2.USER_ID
WHERE p.POST_ID = 1
ORDER BY c.CREATED_AT DESC;
```

### Compter les commentaires par article

```sql
SELECT p.POST_ID, p.TITLE, COUNT(c.COMMENT_ID) as comment_count
FROM POSTS p
LEFT JOIN COMMENTS c ON p.POST_ID = c.POST_ID
GROUP BY p.POST_ID
ORDER BY comment_count DESC;
```

### Rechercher des articles

```sql
SELECT POST_ID, TITLE, CONTENT, PUBLISH_DATE
FROM POSTS
WHERE TITLE LIKE '%keyword%' OR CONTENT LIKE '%keyword%'
ORDER BY PUBLISH_DATE DESC;
```

### Utilisateurs les plus actifs

```sql
SELECT u.USER_ID, u.USERNAME, 
       COUNT(DISTINCT p.POST_ID) as post_count,
       COUNT(DISTINCT c.COMMENT_ID) as comment_count
FROM USERS u
LEFT JOIN POSTS p ON u.USER_ID = p.AUTHOR_ID
LEFT JOIN COMMENTS c ON u.USER_ID = c.USER_ID
GROUP BY u.USER_ID
ORDER BY post_count DESC;
```

---

## Performances et optimisations

### Index recommandés

```sql
-- Index accélère recherche par email (connexion)
CREATE INDEX idx_email ON USERS(EMAIL);

-- Index accélère affichage articles par date
CREATE INDEX idx_publish_date ON POSTS(PUBLISH_DATE DESC);

-- Index accélère recherche commentaires par article
CREATE INDEX idx_post_comments ON COMMENTS(POST_ID);

-- Index accélère recherche par terme
CREATE FULLTEXT INDEX idx_content ON POSTS(TITLE, CONTENT);
```

### Pagination efficace

```sql
-- Bonne approche avec OFFSET/LIMIT
SELECT * FROM POSTS ORDER BY PUBLISH_DATE DESC LIMIT 10 OFFSET 0;

-- Mauvais pour grandes données
SELECT * FROM POSTS ORDER BY PUBLISH_DATE DESC LIMIT 1000000, 10;

-- Meilleur pour grandes données (keyset pagination)
SELECT * FROM POSTS 
WHERE PUBLISH_DATE < (SELECT PUBLISH_DATE FROM POSTS ORDER BY PUBLISH_DATE DESC LIMIT 1 OFFSET 10)
ORDER BY PUBLISH_DATE DESC LIMIT 10;
```

---

## Sauvegarde et restauration

### Exporter la base de données

```bash
mysqldump -u blog_user -p blog > backup.sql
```

### Importer une sauvegarde

```bash
mysql -u blog_user -p blog < backup.sql
```

### Sauvegarde complète du serveur

```bash
mysqldump -u root -p --all-databases > backup_all.sql
```

---

## Migration et évolution

### Ajouter une colonne

```sql
ALTER TABLE POSTS ADD COLUMN CATEGORY VARCHAR(50) AFTER TITLE;
```

### Modifier un type de colonne

```sql
ALTER TABLE USERS MODIFY COLUMN USERNAME VARCHAR(150);
```

### Ajouter un index

```sql
ALTER TABLE USERS ADD UNIQUE INDEX idx_unique_email (EMAIL);
```

### Supprimer une colonne

```sql
ALTER TABLE POSTS DROP COLUMN CATEGORY;
```

---

## Sécurité des données

### Hachage des mots de passe

Ne jamais stocker les mots de passe en clair:

```sql
-- Mauvais: stockage en clair
INSERT INTO USERS (PASSWORD) VALUES ('password123');

-- Bon: stockage haché
INSERT INTO USERS (PSSWRD) VALUES (PASSWORD_FUNCTION('password123'));
```

**En PHP:**
```php
$hashed = password_hash($password, CRYPT_SHA256);
$stored = hash('sha256', $password);  // Non recommandé

// Vérification
password_verify($input, $stored);  // Recommandé
```

### Protection contre injections SQL

Toujours utiliser requêtes préparées:

```php
// Mauvais
$query = "SELECT * FROM USERS WHERE EMAIL = '$email'";

// Bon
$stmt = $pdo->prepare("SELECT * FROM USERS WHERE EMAIL = :email");
$stmt->execute([":email" => $email]);
```

---

## Export et formats

### Format CSV

```bash
mysql -u blog_user -p blog -e "SELECT * FROM USERS" > users.csv
```

### Format JSON

```php
$users = $pdo->query("SELECT * FROM USERS")->fetchAll(PDO::FETCH_ASSOC);
echo json_encode($users, JSON_UNESCAPED_UNICODE);
```

---

Voir aussi : [Installation](../installation.md), [Modèles](../api/modeles.md)
