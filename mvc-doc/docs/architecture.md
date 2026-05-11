# Architecture

CSB Blog suit une architecture **MVC** (Modèle–Vue–Contrôleur) sans framework : le routeur est léger et les fichiers PHP sont regroupés par rôle sous `app/`.

## Rôle des couches

| Couche | Rôle |
|--------|------|
| **Modèle** | Accès à la base (PDO), classes par domaine (`Utilisateur`, `Post`, `Comment`, `Logger`, etc.) |
| **Vue** | Fichiers `*.view.php` : HTML et affichage, données déjà préparées par le contrôleur |
| **Contrôleur** | Scripts sous `app/controllers/*.php` : lecture des entrées HTTP, appels aux modèles, redirections, inclusion des vues |

## Flux d’une requête HTTP

1. Le navigateur appelle `index.php` (souvent avec `?action=…` et d’autres paramètres GET).
2. `index.php` charge `app/controllers/main.php` et lit `$action` (défaut : `default`).
3. La fonction `rout($action)` renvoie le **nom de fichier** du contrôleur à exécuter.
4. `index.php` inclut `app/controllers/<fichier>`.
5. Le contrôleur utilise les modèles, met à jour la session si besoin, puis inclut une ou plusieurs **vues**.
6. La réponse HTML est renvoyée au client.

**Cas particulier** : la page d’un article charge d’abord `post.php`, qui inclut ensuite `comment.php` pour traiter l’ajout de commentaire en POST et afficher le bloc commentaires (`comment.view.php`). `comment.php` n’est **pas** une entrée du tableau des actions dans `main.php` : il est toujours invoqué dans le contexte de `post.php`.

## Routage (`app/controllers/main.php`)

La fonction `rout($action)` associe une chaîne d’action à un fichier contrôleur. Si l’action est inconnue, le contrôleur par défaut est `home.php`.

| Valeur de `action` | Fichier contrôleur |
|--------------------|-------------------|
| `default` | `home.php` |
| `post` | `post.php` |
| `register` | `register.php` |
| `login` | `login.php` |
| `logout` | `logout.php` |
| `search` | `search.php` |
| `edit_comment` | `edit_comment.php` |
| `delete_comment` | `delete_comment.php` |
| `profil` | `profil.php` |
| `admin` | `admin.php` |

Exemples d’URL :

- `index.php` ou `index.php?action=default` — accueil  
- `index.php?action=post&id=1` — article d’identifiant 1  
- `index.php?action=admin&tab=users` — administration, onglet utilisateurs  

## Arborescence utile du dépôt

| Chemin | Contenu |
|--------|---------|
| `index.php` | Point d’entrée HTTP, chargement du routeur et du contrôleur |
| `app/controllers/` | Contrôleurs et `main.php` (routage) |
| `app/models/` | Connexion PDO (`db.inc.php`), modèles, `auth.inc.php`, `logger.inc.php` |
| `app/views/` | Vues partagées (`header`, `footer`) et vues par écran |
| `assets/css/` | Feuilles de style (`main.css`, `main.dark.css`) |
| `assets/images/` | Images statiques |
| `db/` | `blog.sql`, `blog.ext.sql` |
| `logs/` | Journaux quotidiens (création automatique côté code si possible) |
| `scripts/db-reset.sh` | Script optionnel d’initialisation / reset de la base (voir [Installation](installation.md)) |

## Modèles principaux

| Classe / fichier | Responsabilité |
|------------------|----------------|
| `getPdo()` dans `db.inc.php` | Connexion PDO à partir des variables d’environnement |
| `Utilisateur` | Comptes, profil, droits |
| `Post` | Articles, liste, pagination |
| `Comment` | Commentaires liés aux articles |
| `Logger` | Écriture d’événements dans `logs/YYYY-MM-DD.log` |

## Vues

- Suffixe **`.view.php`**.
- Les données affichées passent par `htmlspecialchars()` là où le projet l’impose pour limiter les risques XSS.

## Sessions

Après authentification, la session conserve notamment `userId`, `email`, `username`, `isAdmin` (voir le code de connexion et `auth.inc.php`).

## Extensibilité

1. Nouvelle page exposée par URL : ajouter une entrée dans le tableau `$actions` de `main.php`, créer le contrôleur et la vue.  
2. Nouvelle donnée persistante : script SQL + modèle + utilisation depuis les contrôleurs concernés.

---

Voir aussi : [Guide utilisateur](guide-utilisateur.md), [Développement](developpement.md), [Installation](installation.md)
