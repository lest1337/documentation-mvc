# Architecture

CSB Blog suit une architecture MVC (Model-View-Controller) classique. Cette section décrit la structure du projet et l'organisation du code.

## Vue d'ensemble de l'architecture MVC

L'architecture MVC sépare l'application en trois couches :

```
┌─────────────────────────────────────────────────────────┐
│                  INDEX.PHP (Point d'entrée)             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ CONTROLLERS  │  │   MODELS     │  │    VIEWS     │ │
│  │              │  │              │  │              │ │
│  │ - Logique    │  │ - Données    │  │ - Interface  │ │
│  │ - Routage    │  │ - Requêtes   │  │ - Présentation
│  │ - Traitement │  │ - Validation │  │              │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│                         |                                │
│                    ┌────┴────┐                          │
│                    |          |                          │
│              ┌─────┴──┐  ┌───┴─────┐                   │
│              │ MySQL  │  │  Logs   │                   │
│              │Database│  │ Directory│                   │
│              └────────┘  └─────────┘                   │
└─────────────────────────────────────────────────────────┘
```

## Structure des répertoires

```
blog/
├── app/                              # Répertoire de l'application
│   ├── controllers/                  # Contrôleurs
│   │   ├── main.php                 # Routeur principal
│   │   ├── home.php                 # Accueil
│   │   ├── post.php                 # Affichage d'un article
│   │   ├── admin.php                # Tableau de bord admin
│   │   ├── login.php                # Connexion
│   │   ├── logout.php               # Déconnexion
│   │   ├── register.php             # Inscription
│   │   ├── profil.php               # Profil utilisateur
│   │   ├── search.php               # Recherche
│   │   ├── comment.php              # Gestion des commentaires
│   │   ├── edit_comment.php         # Modification de commentaire
│   │   └── delete_comment.php       # Suppression de commentaire
│   ├── models/                       # Modèles de données
│   │   ├── db.inc.php               # Connexion à la base de données
│   │   ├── auth.inc.php             # Authentification
│   │   ├── utilisateur.inc.php      # Gestion des utilisateurs
│   │   ├── post.inc.php             # Gestion des articles
│   │   ├── comment.inc.php          # Gestion des commentaires
│   │   └── logger.inc.php           # Journalisation
│   └── views/                        # Vues (templates)
│       ├── header.view.php          # En-tête HTML
│       ├── footer.view.php          # Pied de page
│       ├── home.view.php            # Page d'accueil
│       ├── post.view.php            # Vue d'un article
│       ├── admin.view.php           # Vue admin
│       ├── login.view.php           # Formulaire de connexion
│       ├── register.view.php        # Formulaire d'inscription
│       ├── profil.view.php          # Profil utilisateur
│       └── comment.view.php         # Affichage des commentaires
├── assets/                           # Ressources statiques
│   ├── css/
│   │   ├── main.css                 # Styles par défaut
│   │   └── main.dark.css            # Thème sombre
│   └── images/
├── db/                               # Fichiers de base de données
│   ├── blog.sql                     # Schéma initial
│   └── blog.ext.sql                 # Données de test
├── logs/                             # Fichiers de journalisation
├── config/                           # Configurations (futur)
├── index.php                         # Point d'entrée principal
└── README.md                         # Fichier README
```

## Flux de requête

Lorsqu'un utilisateur accède à l'application, voici le flux d'exécution :

```
1. Utilisateur accède à index.php?action=xxxx
        |
        v
2. index.php charge main.php (routeur)
        |
        v
3. Le routeur rout() mappe l'action au contrôleur approprié
        |
        v
4. Le contrôleur selectionné est inclus
        |
        v
5. Le contrôleur traite la logique métier
        |  +-- Interroge les modèles
        |  +-- Vérifie l'authentification
        |  +-- Manipule les données
        |
        v
6. Les données sont passées à la vue
        |
        v
7. La vue affiche le contenu HTML
        |
        v
8. Réponse envoyée au navigateur
```

## Couche Modèle

Les modèles sont des classes PHP qui gèrent la communication avec la base de données. Ils utilisent PDO (PHP Data Objects) pour sécuriser les requêtes SQL.

### Classes principales

| Classe | Fichier | Responsabilité |
|--------|---------|-----------------|
| `Utilisateur` | `utilisateur.inc.php` | Gestion des utilisateurs |
| `Post` | `post.inc.php` | Gestion des articles |
| `Comment` | `comment.inc.php` | Gestion des commentaires |
| `Logger` | `logger.inc.php` | Journalisation des actions |

### Exemple de modèle

```php
class Post {
    private PDO $pdo;
    
    function __construct() {
        $this->pdo = getPdo();
    }
    
    function getPosts($limit = 10, $offset = 0) {
        // Récupère les articles avec pagination
    }
    
    function getSinglePost($postId) {
        // Récupère un article spécifique
    }
}
```

## Couche Contrôleur

Les contrôleurs gèrent la logique métier et coordonnent les interactions entre les modèles et les vues.

### Caractéristiques

- Chaque action a un contrôleur dédié
- Les contrôleurs vérifient l'authentification si nécessaire
- Ils manipulent les données via les modèles
- Ils passent les données à la vue appropriée
- Ils gèrent les redirections après traitement

### Exemple de contrôleur

```php
// app/controllers/post.php
if (!isset($_GET["id"])) {
    header("Location: index.php");
    exit();
}

$post = new Post();
$article = $post->getSinglePost($_GET["id"]);
$comments = $post->getComments($_GET["id"]);

require_once "app/views/post.view.php";
```

## Couche Vue

Les vues sont des fichiers PHP qui contiennent le balisage HTML et l'affichage des données.

### Conventions

- Les fichiers de vue sont nommés avec l'extension `.view.php`
- Ils reçoivent les données des contrôleurs via des variables locales
- Ils n'exécutent pas de logique métier complexe
- Ils se concentrent sur la présentation des données

### Exemple de vue

```php
<!-- app/views/post.view.php -->
<?php require_once "app/views/header.view.php"; ?>

<article>
    <h1><?= htmlspecialchars($article['TITLE']) ?></h1>
    <p><?= htmlspecialchars($article['CONTENT']) ?></p>
</article>

<?php require_once "app/views/footer.view.php"; ?>
```

## Routage

Le routage est géré par la fonction `rout()` dans `app/controllers/main.php`. Elle mappe les actions aux contrôleurs :

```php
function rout($action) {
    $actions = array(
        "default" => "home.php",
        "post" => "post.php",
        "register" => "register.php",
        "login" => "login.php",
        // ... et ainsi de suite
    );
    
    return $actions[$action] ?? $actions["default"];
}
```

### Routes disponibles

| Route | Contrôleur | Description |
|-------|-----------|-------------|
| `index.php` ou `index.php?action=default` | `home.php` | Page d'accueil |
| `index.php?action=post&id=X` | `post.php` | Affiche un article |
| `index.php?action=register` | `register.php` | Page d'inscription |
| `index.php?action=login` | `login.php` | Page de connexion |
| `index.php?action=logout` | `logout.php` | Déconnecte l'utilisateur |
| `index.php?action=search` | `search.php` | Recherche d'articles |
| `index.php?action=profil` | `profil.php` | Profil utilisateur |
| `index.php?action=admin` | `admin.php` | Tableau de bord admin |
| `index.php?action=edit_comment` | `edit_comment.php` | Modifie un commentaire |
| `index.php?action=delete_comment` | `delete_comment.php` | Supprime un commentaire |

## Gestion des sessions

Les sessions PHP sont utilisées pour maintenir l'état de l'utilisateur :

```php
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

// Après authentification réussie
$_SESSION["userId"] = $user["USER_ID"];
$_SESSION["username"] = $user["USERNAME"];
$_SESSION["isAdmin"] = $user["IS_ADMIN"];
```

## Gestion des erreurs

L'application utilise une approche simple de gestion des erreurs :

- Les exceptions PDO sont attrapées et affichées
- Les redirections sont utilisées pour les erreurs de validation
- Les messages d'erreur sont affichés via les vues

## Extensibilité

L'architecture MVC rend facile l'extension de l'application :

1. **Ajouter une nouvelle page**: Créez un nouveau contrôleur et une vue, ajoutez la route dans `main.php`
2. **Ajouter une nouvelle fonctionnalité de données**: Créez une nouvelle classe modèle
3. **Modifier le style**: Éditez les fichiers CSS dans `assets/css/`

## Principes de conception

L'application suit ces principes :

- **Séparation des préoccupations**: Modèles, vues et contrôleurs sont séparés
- **DRY (Don't Repeat Yourself)**: Les vues communes sont incluses (header/footer)
- **Sécurité par défaut**: Utilisation de requêtes préparées, validation des entrées
- **Maintenabilité**: Code organisé et facile à comprendre
- **Pas de dépendances externes**: PHP natif pour une meilleure compréhension

---

Voir aussi : [Guide Utilisateur](guide-utilisateur.md), [Développement](developpement.md)
