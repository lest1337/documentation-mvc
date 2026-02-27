# Installation et Configuration

Ce guide vous explique comment installer et configurer CSB Blog sur votre machine.

## Prérequis

Avant de commencer, assurez-vous d'avoir installé :

- **PHP**: 7.0 ou supérieur
- **MySQL**: 5.7 ou supérieur
- **Git**: Pour cloner le projet
- **Composer** (optionnel): Bien qu'aucune dépendance PHP externe ne soit requise

## Étapes d'installation

### 1. Cloner le projet

Ouvrez votre terminal et clonez le repository :

```bash
git clone https://github.com/lest1337/blog-mvc
cd blog
```

Ou, si vous disposez du projet sous forme d'archive :

```bash
unzip blog.zip
cd blog
```

### 2. Configurer la base de données

#### Créer une base de données MySQL

Connectez-vous à MySQL :

```bash
mysql -u root -p
```

Exécutez les scripts SQL de configuration :

```sql
source db/blog.sql;
source db/blog.ext.sql;
```

Ces scripts vont créer :
- La base de données `blog`
- Les tables nécessaires (USERS, POSTS, COMMENTS)
- Des données de test d'exemple

#### Créer un utilisateur MySQL

Créez un utilisateur dédié pour l'application (remplacez les identifiants selon vos préférences) :

```sql
CREATE USER 'blog_user'@'127.0.0.1' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON blog.* TO 'blog_user'@'127.0.0.1';
FLUSH PRIVILEGES;
```

### 3. Configurer les identifiants de base de données

Ouvrez le fichier `app/models/db.inc.php` et mettez à jour les informations de connexion :

```php
$USERNAME = "blog_user";      // Nom d'utilisateur MySQL
$PASSWORD = "password";         // Mot de passe MySQL
$DBNAME = "blog";              // Nom de la base de données
$HOST = "127.0.0.1";          // Hôte MySQL
```

### 4. Créer le répertoire des logs

Le système de journalisation nécessite un répertoire `logs`. Créez-le s'il n'existe pas :

```bash
mkdir -p logs
chmod 755 logs
```

### 5. Permissions des fichiers

Assurez-vous que les permissions sont correctes :

```bash
chmod 755 .
chmod 755 app logs assets
chmod 644 index.php
```

## Lancer l'application

### Avec le serveur PHP intégré

Pour développement local, utilisez le serveur PHP intégré :

```bash
php -S localhost:8080
```

Puis ouvrez votre navigateur et allez à : `http://localhost:8080`

### Avec Apache ou Nginx

Pour un déploiement en production, configurez votre serveur web pour pointer vers le répertoire racine du projet.

#### Configuration Apache

Créez un fichier `.htaccess` si nécessaire :

```apache
<IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteCond %{REQUEST_FILENAME} !-f
    RewriteCond %{REQUEST_FILENAME} !-d
    RewriteRule ^(.*)$ index.php?action=$1 [QSA,L]
</IfModule>
```

#### Configuration Nginx

Configurez le bloc `location` :

```nginx
location / {
    try_files $uri $uri/ /index.php?action=$request_uri;
}
```

## Vérifier l'installation

Une fois lancé, testez l'application :

1. Visitez `http://localhost:8080` - vous devriez voir la page d'accueil
2. Cliquez sur "Inscription" pour créer un compte utilisateur
3. Connectez-vous
4. Consultez les articles existants
5. Ajoutez un commentaire à un article

## Problèmes courants

### Erreur de connexion à la base de données

**Problème**: "SQLSTATE[HY000] [1049] Unknown database"

**Solution**: Vérifiez que :
- MySQL est en cours d'exécution
- La base de données `blog` a été créée correctement
- Les identifiants dans `db.inc.php` sont corrects

### Permissions insuffisantes

**Problème**: "Warning: file_put_contents(): Failed to open stream"

**Solution**: Assurez-vous que le répertoire `logs` existe et est accessible en écriture :

```bash
mkdir -p logs
chmod 755 logs
```

### Page blanche ou erreurs PHP

**Problème**: L'application affiche une page blanche

**Solution**: Activez l'affichage des erreurs pour le débogage temporaire dans `index.php` :

```php
ini_set('display_errors', 1);
error_reporting(E_ALL);
```

### Sessions non fonctionnelles

**Problème**: Les sessions utilisateur ne persistent pas

**Solution**: Vérifiez la configuration PHP :

```bash
php -i | grep "session.save_path"
```

Assurez-vous que le répertoire de sauvegarde des sessions existe et est accessible.

## Configuration additionnelle

### Variables d'environnement (recommandé)

Pour une meilleure sécurité en production, créez un fichier `.env` :

```bash
DB_USER=blog_user
DB_PASSWORD=your_secure_password
DB_NAME=blog
DB_HOST=127.0.0.1
```

Puis modifiez `db.inc.php` pour lire depuis ce fichier plutôt que d'utiliser des valeurs en dur.

### Configuration du fuseau horaire

Définissez le fuseau horaire dans `index.php` ou un fichier de configuration :

```php
date_default_timezone_set('Europe/Paris');
```

## Prochaines étapes

Après l'installation réussie :

1. Lisez la section **Architecture** pour comprendre la structure du projet
2. Consultez le **Guide Utilisateur** pour apprendre à utiliser l'application
3. Explorez la documentation **API** pour développer des extensions

---

**Besoin d'aide?** Vérifiez les fichiers de log dans le répertoire `logs/` pour diagnostiquer les problèmes.
