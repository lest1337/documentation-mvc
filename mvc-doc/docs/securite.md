# Sécurité

Cette section documente les mesures de sécurité implémentées dans CSB Blog.

## Vue d'ensemble

La sécurité est un aspect fondamental de CSB Blog. L'application utilise plusieurs techniques pour protéger les données et prévenir les attaques courantes.

### Menaces adressées

- Injections SQL
- Attaques CSRF
- Vol de session
- Mots de passe faibles
- Accès non autorisé

---

## Protection contre les injections SQL

### Requêtes préparées

Toutes les requêtes utilisent PDO avec des paramètres liés :

```php
// Approche SÉCURISÉE
$stmt = $pdo->prepare("SELECT * FROM USERS WHERE EMAIL = :email");
$stmt->execute([":email" => $userInput]);

// Approche NON SÉCURISÉE (à éviter)
$query = "SELECT * FROM USERS WHERE EMAIL = '$userInput'";
$stmt = $pdo->query($query);
```

**Avantages:**
- Séparation entre code SQL et données
- Échappement automatique des caractères spéciaux
- Prévention des injections SQL

### Exemple d'utilisation

```php
// Class: Utilisateur
function getUserByMail($email) {
    $stmt = $this->pdo->prepare(
        "SELECT USER_ID, USERNAME, EMAIL, PSSWRD, IS_ADMIN 
         FROM USERS 
         WHERE EMAIL = :email"
    );
    $stmt->execute([":email" => $email]);
    return $stmt->fetch(PDO::FETCH_ASSOC);
}
```

### Validation des types

Utiliser les paramètres typés pour les entiers :

```php
$stmt = $pdo->prepare("SELECT * FROM POSTS WHERE POST_ID = :id");
$stmt->bindValue(":id", $id, PDO::PARAM_INT);
$stmt->execute();
```

---

## Hachage des mots de passe

### Fonction password_hash()

Les mots de passe sont hachés avec un algorithme sécurisé :

```php
// Lors de l'inscription
$hashedPassword = password_hash($password, CRYPT_SHA256);
$user->addUser($username, $email, $hashedPassword);
```

### Vérification avec password_verify()

Pour la connexion, vérifier sans jamais comparer les hachés directement :

```php
$userData = $user->getUserByMail($email);
if ($userData && password_verify($password, $userData["PSSWRD"])) {
    // Mot de passe correct
    $_SESSION["userId"] = $userData["USER_ID"];
} else {
    // Échec d'authentification
    $error = "Email ou mot de passe incorrect";
}
```

### Avantages de password_hash()

- Utilise un algorithme sécurisé (CRYPT_SHA256)
- Ajoute automatiquement un salt
- Résistant aux attaques par force brute
- Les anciennes implémentations (md5, SHA1) sont non recommandées

### Password strength

Recommandations pour un mot de passe sûr :

```php
function isStrongPassword($password) {
    // Au moins 8 caractères
    if (strlen($password) < 8) return false;
    
    // Au moins une majuscule
    if (!preg_match('/[A-Z]/', $password)) return false;
    
    // Au moins une minuscule
    if (!preg_match('/[a-z]/', $password)) return false;
    
    // Au moins un chiffre
    if (!preg_match('/[0-9]/', $password)) return false;
    
    // Au moins un caractère spécial
    if (!preg_match('/[^A-Za-z0-9]/', $password)) return false;
    
    return true;
}
```

---

## Gestion des sessions

### Démarrage sécurisé

Vérifier l'état de la session avant de la démarrer :

```php
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}
```

### Propriétés de sécurité

Configuration recommandée dans `php.ini` ou au contrôleur :

```php
// Cookies de session
ini_set('session.cookie_httponly', 1);  // Non accessible par JavaScript
ini_set('session.cookie_secure', 1);    // Uniquement en HTTPS
ini_set('session.cookie_samesite', 'Strict'); // Protection CSRF
```

### Destruction de session

Toujours détruire la session à la déconnexion :

```php
function logout() {
    if (session_status() === PHP_SESSION_NONE) {
        session_start();
    }
    
    // Log de la déconnexion
    Logger::log("LOGOUT", ["user_id" => $_SESSION["userId"]]);
    
    // Destruction
    session_unset();
    session_destroy();
    
    // Redirection
    header("Location: index.php");
    exit();
}
```

---

## Protection d'accès aux pages

### Vérification d'authentification

Pour les pages nécessitant une connexion :

```php
<?php
require_once "app/models/auth.inc.php";

if (!isLoggedOn()) {
    header("Location: index.php?action=login");
    exit();
}

// Code de la page protégée
?>
```

### Vérification des droits admin

Pour les pages réservées à l'administrateur :

```php
<?php
if (!isLoggedOn() || !isAdmin()) {
    header("Location: index.php");
    exit();
}

// Code réservé admin
?>
```

### Vérification de propriété

Pour les actions sur les données utilisateur :

```php
if (!isLoggedOn()) {
    header("Location: index.php?action=login");
    exit();
}

$comment = new Comment();
$commentData = $comment->getCommentById($commentId);
$currentUserId = (new Utilisateur())->getCurrentUserId();

// L'utilisateur peut modifier son propre commentaire ou est admin
if ($commentData["USER_ID"] != $currentUserId && !isAdmin()) {
    header("Location: index.php");
    exit();
}

// Permet la modification
$comment->updateComment($commentId, $currentUserId, $newContent);
```

---

## Validation des entrées

### Validation côté serveur

Ne jamais faire confiance aux données client :

```php
// Email
if (!filter_var($_POST["email"], FILTER_VALIDATE_EMAIL)) {
    $error = "Email invalide";
}

// Longueur
if (strlen($_POST["username"]) < 3 || strlen($_POST["username"]) > 100) {
    $error = "Nom d'utilisateur entre 3 et 100 caractères";
}

// Format alphanumérique
if (!ctype_alnum(str_replace('_', '', $_POST["username"]))) {
    $error = "Caractères non autorisés";
}
```

### Échappement pour l'affichage

Toujours échapper les données avant de les afficher en HTML :

```php
// Bon: prévient les injections XSS
echo htmlspecialchars($article['TITLE'], ENT_QUOTES, 'UTF-8');

// Mauvais: risque de XSS
echo $article['TITLE'];

// Alternative
<?= htmlspecialchars($article['TITLE']) ?>
```

### Exemple complet de validation

```php
// Validation inscription
if ($_SERVER["REQUEST_METHOD"] === "POST") {
    $username = trim($_POST["username"] ?? "");
    $email = trim($_POST["email"] ?? "");
    $password = $_POST["password"] ?? "";
    $password2 = $_POST["password2"] ?? "";
    
    $errors = [];
    
    // Validation
    if (empty($username)) {
        $errors[] = "Nom d'utilisateur requis";
    } elseif (strlen($username) < 3 || strlen($username) > 100) {
        $errors[] = "Nom d'utilisateur: 3 a 100 caracteres";
    }
    
    if (empty($email) || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $errors[] = "Email invalide";
    }
    
    if (empty($password) || strlen($password) < 8) {
        $errors[] = "Mot de passe: minimum 8 caracteres";
    }
    
    if ($password !== $password2) {
        $errors[] = "Les mots de passe ne correspondent pas";
    }
    
    // Traitement si valide
    if (empty($errors)) {
        try {
            $user = new Utilisateur();
            $user->addUser($username, $email, $password);
            header("Location: index.php?action=login");
        } catch (PDOException $e) {
            $errors[] = "Cet utilisateur existe déjà";
        }
    }
}
```

---

## Protection CSRF

### Tokens CSRF

Pour les formulaires sensibles, utiliser des tokens :

```php
// Génération du token
session_start();
if (empty($_SESSION['csrf_token'])) {
    $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
}

// Dans le formulaire
<form method="POST">
    <input type="hidden" name="csrf_token" value="<?= $_SESSION['csrf_token'] ?>">
    ...
</form>

// Vérification
if (!hash_equals($_SESSION['csrf_token'], $_POST['csrf_token'] ?? '')) {
    die("CSRF token invalid");
}
```

### Recommandation

Appliquer sur tous les formulaires POST sensibles (modification de compte, suppression, etc.)

---

## Journalisation et audit

### Logging des actions sensibles

Enregistrer toutes les actions de sécurité :

```php
// Connexion
Logger::log("LOGIN", ["username" => $username]);

// Modification de profil
Logger::log("PROFILE_UPDATE", ["user_id" => $userId]);

// Suppression
Logger::log("POST_DELETE", ["post_id" => $postId]);

// Tentatives échouées
Logger::log("FAILED_LOGIN", ["email" => $email]);
```

### Format du log

```
[2026-02-27 14:30:45] | 192.168.1.1 | 5 | john_doe | LOGIN | ...
 [timestamp]           [IP client]  [ID] [username] [action] [details]
```

### Accès aux logs

Seul l'administrateur peut consulter les logs :

```php
if (!isAdmin()) {
    header("Location: index.php");
    exit();
}

$logs = Logger::getLogs(7);  // 7 derniers jours
```

### Retention

Recommandations:
- Conserver les logs au minimum 90 jours
- Archiver les anciens logs mensuellement
- Chiffrer les logs contenant des informations sensibles

---

## Communication sécurisée (HTTPS)

### Redirection HTTPS

En production, forcer HTTPS :

```php
// Dans index.php ou au niveau du serveur
if (empty($_SERVER['HTTPS']) || $_SERVER['HTTPS'] === 'off') {
    header('Location: https://' . $_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI']);
    exit;
}
```

### Certificat SSL/TLS

- Obtenir un certificat SSL valide (Let's Encrypt gratuit)
- Configurer le serveur web
- Rediriger HTTP vers HTTPS
- Activer HSTS header

### Configuration Apache

```apache
<VirtualHost *:443>
    ServerName blog.example.com
    SSLEngine on
    SSLCertificateFile /etc/ssl/certs/cert.pem
    SSLCertificateKeyFile /etc/ssl/private/key.pem
    
    # HSTS
    Header always set Strict-Transport-Security "max-age=31536000"
</VirtualHost>

# Redirection HTTP vers HTTPS
<VirtualHost *:80>
    ServerName blog.example.com
    Redirect / https://blog.example.com
</VirtualHost>
```

---

## Sécurité de la configuration

### Fichier de configuration

Ne jamais committer les informations sensibles :

```php
// Mauvais: dans le git
$PASSWORD = "password123";

// Bon: dans .env (non commité)
// .env
DB_PASSWORD=password123

// .gitignore
.env
*.env
```

### Lecture depuis .env

```php
$envFile = __DIR__ . '/.env';
if (file_exists($envFile)) {
    $lines = file($envFile, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
    foreach ($lines as $line) {
        if (strpos($line, '=') !== false) {
            list($key, $value) = explode('=', $line, 2);
            $_ENV[trim($key)] = trim($value);
        }
    }
}

$dbPassword = $_ENV['DB_PASSWORD'] ?? 'default';
```

### Permissions des fichiers

```bash
# Configuration: lecture uniquement
chmod 600 config/database.php

# Logs: appartient à l'application
chmod 755 logs
chmod 644 logs/*.log

# Répertoire web
chmod 755 public/
chmod 644 public/*
```

---

## En-têtes de sécurité HTTP

### Recommandations

```php
// Dans index.php
header('X-Content-Type-Options: nosniff');           // Pas de MIME-sniffing
header('X-Frame-Options: SAMEORIGIN');               // Controle clickjacking
header('X-XSS-Protection: 1; mode=block');           // Protection XSS
header('Content-Security-Policy: default-src \'self\''); // CSP
header('Referrer-Policy: strict-origin-when-cross-origin');
```

### Content Security Policy (CSP)

Pour prévenir les injections XSS :

```php
header("Content-Security-Policy: 
    default-src 'self';
    script-src 'self' 'unsafe-inline';
    style-src 'self' 'unsafe-inline';
    img-src 'self' data: https:;
    font-src 'self';
    connect-src 'self';
    frame-ancestors 'none';
");
```

---

## Checklist de sécurité

Avant le déploiement en production :

- [ ] Tous les mots de passe utilisent `password_hash()`
- [ ] Toutes les requêtes SQL sont préparées (PDO)
- [ ] Les données affichées sont échappées avec `htmlspecialchars()`
- [ ] Les sessions sont correctement protégées
- [ ] HTTPS est activé et forcé
- [ ] Les credentials de base de données ne sont pas en dur
- [ ] Les logs sont centralisés et archivés
- [ ] Un administrateur par défaut est défini
- [ ] Les fichiers sensibles ont les bonnes permissions
- [ ] Les erreurs ne sont pas affichées au public
- [ ] Validation des entrées côté serveur
- [ ] Gestion des droits d'accès correcte
- [ ] CSRF tokens sur les formulaires sensibles
- [ ] Pas de données sensibles dans les logs

---

## Ressources supplémentaires

- OWASP Top 10: https://owasp.org/www-project-top-ten/
- PHP Security: https://www.php.net/manual/en/security.php
- CWE/SANS Top 25: https://cwe.mitre.org/top25/

---

Voir aussi : [Installation](installation.md), [Architecture](architecture.md)
