# Guide de Développement

Ce guide aide les développeurs à contribuer et étendre CSB Blog.

## Démarrage rapide pour développeurs

### Configuration de l'environnement de développement

1. Cloner le repository
```bash
git clone https://github.com/lest1337/blog-mvc
cd blog
```

2. Installer les dépendances (PHP intégré, pas de dépendances externes)

3. Configurer la base de données
```bash
mysql -u root -p < db/blog.sql
mysql -u root -p < db/blog.ext.sql
```

4. Lancer le serveur
```bash
php -S localhost:8080
```

### Structure du projet

```
app/
├── controllers/    # Logique métier et routage
├── models/        # Accès aux données
└── views/         # Affichage HTML

assets/
├── css/           # Feuilles de style
└── images/        # Images statiques

db/
├── blog.sql       # Schéma initial
└── blog.ext.sql   # Données de test

logs/              # Fichiers de journalisation
```

---

## Architecture MVC

### Modèles (Models)

Les modèles gèrent l'accès aux données et la logique métier.

**Créer un nouveau modèle:**

```php
<?php
// app/models/category.inc.php
include_once "db.inc.php";

class Category {
    private PDO $pdo;
    
    function __construct() {
        $this->pdo = getPdo();
    }
    
    function getCategories() {
        $stmt = $this->pdo->query("SELECT * FROM CATEGORIES");
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }
    
    function addCategory($name, $description) {
        $stmt = $this->pdo->prepare(
            "INSERT INTO CATEGORIES (NAME, DESCRIPTION) 
             VALUES (:name, :description)"
        );
        $stmt->execute([
            ":name" => $name,
            ":description" => $description
        ]);
    }
}
?>
```

**Bonnes pratiques:**
- Une classe = une table
- Requêtes préparées obligatoires
- Méthodes publiques pour les opérations CRUD
- Propriété privée pour PDO

### Contrôleurs (Controllers)

Les contrôleurs gèrent le flux de l'application et les interactions utilisateur.

**Créer un nouveau contrôleur:**

```php
<?php
// app/controllers/category.php
require_once "app/models/auth.inc.php";
include_once "app/models/category.inc.php";

// Vérifier l'authentification si nécessaire
if (!isLoggedOn()) {
    header("Location: index.php?action=login");
    exit();
}

// Traiter les données
$category = new Category();

if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $name = $_POST["name"] ?? "";
    $description = $_POST["description"] ?? "";
    
    if (!empty($name)) {
        $category->addCategory($name, $description);
        Logger::log("CATEGORY_ADD", ["name" => $name]);
        header("Location: index.php");
    }
}

// Récupérer les données
$categories = $category->getCategories();

// Afficher la vue
require_once "app/views/category.view.php";
?>
```

**Enregistrer la route dans main.php:**

```php
function rout($action) {
    $actions = array(
        "default" => "home.php",
        "category" => "category.php",  // Nouvelle route
        // ...
    );
    // ...
}
```

### Vues (Views)

Les vues affichent le HTML et reçoivent les données des contrôleurs.

**Créer une nouvelle vue:**

```php
<!-- app/views/category.view.php -->
<?php require_once "app/views/header.view.php"; ?>

<h1>Categories</h1>

<form method="POST">
    <input type="text" name="name" placeholder="Nom" required>
    <textarea name="description" placeholder="Description"></textarea>
    <button type="submit">Ajouter</button>
</form>

<ul>
<?php foreach ($categories as $cat): ?>
    <li><?= htmlspecialchars($cat['NAME']) ?></li>
<?php endforeach; ?>
</ul>

<?php require_once "app/views/footer.view.php"; ?>
```

**Bonnes pratiques:**
- Inclure header et footer
- Échapper toutes les données avec `htmlspecialchars()`
- Pas de logique complexe
- Une vue par action

---

## Ajouter une nouvelle fonctionnalité

### Exemple: Système de catégories

#### Etape 1: Créer la table dans la base de données

```sql
CREATE TABLE CATEGORIES (
    CATEGORY_ID INT AUTO_INCREMENT PRIMARY KEY,
    NAME VARCHAR(100) NOT NULL UNIQUE,
    DESCRIPTION TEXT,
    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE POSTS ADD COLUMN CATEGORY_ID INT;
ALTER TABLE POSTS ADD FOREIGN KEY (CATEGORY_ID) 
    REFERENCES CATEGORIES(CATEGORY_ID);
```

#### Etape 2: Créer le modèle

```php
<?php
// app/models/category.inc.php
class Category {
    // ... (voir exemple précédent)
}
?>
```

#### Etape 3: Créer le contrôleur

```php
<?php
// app/controllers/categories.php
// ... (voir exemple précédent)
?>
```

#### Etape 4: Créer la vue

```php
<!-- app/views/categories.view.php -->
<!-- ... (voir exemple précédent) -->
```

#### Etape 5: Enregistrer la route

```php
// app/controllers/main.php
function rout($action) {
    $actions = array(
        // ...
        "categories" => "categories.php"
    );
    // ...
}
```

#### Etape 6: Tester

Visiter: `http://localhost:8080/index.php?action=categories`

---

## Convention de nommage

### Fichiers

- **Modèles**: `lowercase.inc.php` (ex: `utilisateur.inc.php`)
- **Contrôleurs**: `lowercase.php` (ex: `post.php`)
- **Vues**: `lowercase.view.php` (ex: `post.view.php`)

### Variables PHP

```php
// Utilisateur ou utilisateurs (singulier/pluriel selon contexte)
$user = new Utilisateur();
$users = $user->getAllUsers();

// Données
$userData = $user->getUser($id);

// Booléens
$isLoggedIn = isLoggedOn();
$isAdmin = isAdmin();
```

### Variables dans les vues

```php
// Liste paginée
$page = 1;
$users = [];
$totalUsers = 0;

// Formulaire
$username = "";
$email = "";
$error = "";
$success = "";
```

### Requêtes SQL

- Noms de tables: MAJUSCULES (ex: `USERS`, `POSTS`)
- Noms de colonnes: MAJUSCULES (ex: `USER_ID`, `USERNAME`)
- Placeholders: `:nom_variable` (kebab-case)

---

## Gestion des erreurs

### Try-Catch pour les opérations de base de données

```php
try {
    $user = new Utilisateur();
    $user->addUser($username, $email, $password);
    $success = "Utilisateur créé";
} catch (PDOException $e) {
    error_log("Database error: " . $e->getMessage());
    $error = "Erreur lors de la création";
}
```

### Gestion des erreurs utilisateur

```php
$errors = [];

if (empty($username)) {
    $errors[] = "Nom d'utilisateur requis";
}

if (strlen($password) < 8) {
    $errors[] = "Mot de passe trop court";
}

if (!empty($errors)) {
    $error = implode("; ", $errors);
}
```

### Journalisation

```php
// Erreur
error_log("Critical error: " . $e->getMessage());

// Information
Logger::log("ACTION_NAME", ["detail" => "value"]);

// Debug (développement uniquement)
ini_set('display_errors', 1);
error_reporting(E_ALL);
```

---

## Tests

### Tests manuels

1. Vérifier chaque route
```bash
curl http://localhost:8080/index.php?action=home
curl http://localhost:8080/index.php?action=register
curl http://localhost:8080/index.php?action=login
```

2. Tester les formulaires
3. Vérifier les redirections
4. Tester les droits d'accès

### Créer des tests unitaires (futur)

Exemple avec PHPUnit:

```php
<?php
use PHPUnit\Framework\TestCase;

class UserTest extends TestCase {
    public function testAddUser() {
        $user = new Utilisateur();
        $user->addUser("test_user", "test@example.com", "password");
        
        $userData = $user->getUserByMail("test@example.com");
        $this->assertEquals("test_user", $userData['USERNAME']);
    }
    
    public function testPasswordVerification() {
        $hashed = password_hash("password", CRYPT_SHA256);
        $this->assertTrue(password_verify("password", $hashed));
    }
}
?>
```

---

## Bonnes pratiques

### Code propre

1. **Indentation** (4 espaces)
```php
<?php
if ($condition) {
    // Indentation
    $value = 10;
}
?>
```

2. **Commentaires**
```php
// Commentaire sur une ligne
$id = $_GET["id"];

/*
 * Commentaire sur plusieurs lignes
 * pour expliquer la logique complexe
 */
```

3. **Noms explicites**
```php
// Bon
$userEmail = $user->getEmail();

// Mauvais
$ue = $user->getEmail();
```

### Sécurité

1. Toujours utiliser les requêtes préparées
2. Toujours échapper les données affichées
3. Valider les entrées côté serveur
4. Vérifier l'authentification avant d'accéder aux données sensibles
5. Logger les actions importantes

### Performance

1. Minimiser les requêtes à la base de données
```php
// Mauvais: N requêtes
foreach ($postIds as $id) {
    $post = new Post();
    $post->getSinglePost($id);
}

// Bon: 1 requête
$posts = $post->getPosts();
```

2. Utiliser la pagination
```php
// Bon
$posts = $post->getPosts(10, 0);

// Mauvais: charger tous les articles
$posts = $post->getAllPosts();
```

3. Cacher les requêtes fréquentes
```php
// Utiliser Redis ou Memcached
$userCount = apcu_fetch('user_count');
if (!$userCount) {
    $userCount = (new Utilisateur())->getUserCount();
    apcu_store('user_count', $userCount, 3600);
}
```

---

## Déploiement

### Préparation

1. Vérifier que tout fonctionne en local
2. Exécuter les tests
3. Vérifier les erreurs de lint PHP
```bash
php -l app/controllers/*.php
php -l app/models/*.php
```

4. Créer une branche de déploiement
```bash
git checkout -b deploy/production
git push origin deploy/production
```

### Étapes de déploiement

1. Cloner sur le serveur
2. Installer les dépendances PHP
3. Configurer la base de données
4. Définir les variables d'environnement
5. Configurer le serveur web (Apache/Nginx)
6. Activer HTTPS
7. Tester l'application

### Configuration serveur de production

```php
// db.inc.php - Utiliser des variables d'environnement
$USERNAME = getenv('DB_USER') ?: 'blog_user';
$PASSWORD = getenv('DB_PASSWORD') ?: '';
$DBNAME = getenv('DB_NAME') ?: 'blog';
$HOST = getenv('DB_HOST') ?: '127.0.0.1';
```

### Gestion des logs

```bash
# Rotation des logs
find logs -name "*.log" -mtime +30 -delete

# Compression archivage
tar -czf logs/archive-$(date +%Y%m%d).tar.gz logs/*.log
```

---

## Contribution

### Pour contribuer

1. Fork le projet
2. Créer une branche feature
```bash
git checkout -b feature/nouvelle-feature
```

3. Commiter les changements
```bash
git commit -m "Ajoute: description courte"
```

4. Pusher vers le repository
```bash
git push origin feature/nouvelle-feature
```

5. Créer une Pull Request

### Standards de commit

```
Ajoute: Courte description
Corrite: Bug fix
Ameliore: Optimisations
Refactor: Restructuration de code
Docs: Documentation
Test: Ajout de tests
```

### Code review

- Vérifier la sécurité
- Vérifier la structure MVC
- Vérifier la documentation
- Tester manuellement
- Donner du feedback constructif

---

## Documentation

### Documenter le code

```php
/**
 * Récupère un utilisateur par son email
 * 
 * @param string $email L'adresse email de l'utilisateur
 * @return array|null Les données utilisateur ou null si non trouvé
 */
function getUserByMail($email) {
    // ...
}
```

### Documenter une route

```php
/**
 * Affiche un article complet avec commentaires
 * Route: index.php?action=post&id=X
 * Authentification: Aucune
 * 
 * GET params:
 *  - id (int): ID de l'article
 */
```

### Documenter une base de données

```sql
-- Stocke les articles du blog
-- Lié à USERS (auteur)
CREATE TABLE POSTS (
    POST_ID INT PRIMARY KEY,  -- Identifiant unique
    TITLE VARCHAR(200),       -- Titre de l'article
    // ...
);
```

---

## Ressources

- Documentation PHP: https://www.php.net/manual/
- PDO: https://www.php.net/manual/en/book.pdo.php
- MySQL: https://dev.mysql.com/doc/
- OWASP: https://owasp.org/
- Git: https://git-scm.com/doc

---

Voir aussi : [Architecture](architecture.md), [Sécurité](securite.md), [Base de Données](base-donnees.md)
