# Sécurité

Ce document décrit les mesures **réellement présentes** dans le code du dépôt blog-mvc, les **lacunes** connues et des **recommandations** pour un environnement plus exposé (Internet).

## Ce que l’application fait déjà

### Injections SQL

Les accès passent par **PDO** avec des **requêtes préparées** et des paramètres nommés, ce qui réduit fortement le risque d’injection SQL lorsque cette discipline est respectée partout.

### Mots de passe

Les mots de passe sont hachés avec `password_hash()` et vérifiés avec `password_verify()` dans le modèle utilisateur (algorithme configuré dans le projet, voir `app/models/utilisateur.inc.php`).

### Affichage (XSS)

Les vues s’appuient sur `htmlspecialchars()` pour une partie des données affichées. Toute nouvelle vue doit conserver cette prudence sur les contenus issus de la base ou des entrées utilisateur.

### Authentification et rôles

- Vérifications du type `isLoggedOn()` / `isAdmin()` avant les actions sensibles.
- L’administration impose un utilisateur connecté avec droits administrateur.

### Journalisation

Des actions importantes sont enregistrées via `Logger::log()` dans des fichiers datés sous `logs/` (utile pour audit interne, pas un substitut à une supervision complète).

## Lacunes importantes (à connaître)

### Absence de protection CSRF

**Les formulaires ne vérifient pas de jeton CSRF.** Une session authentifiée peut donc théoriquement être exploitée par une requête forgée depuis un autre site si l’utilisateur ouvre une page malveillante pendant sa session.

**Piste d’évolution** : générer un jeton en session, l’injecter en champ caché dans chaque formulaire mutatif (POST), et le valider avec `hash_equals()` côté serveur avant toute action.

### Pas d’en-têtes HTTP de sécurité globaux

Le dépôt ne configure pas par défaut CSP, HSTS, `X-Frame-Options`, etc. Ces éléments relèvent en pratique du **serveur web** ou d’un bootstrap PHP dédié en production.

### Configuration des sessions

Des réglages tels que `session.cookie_httponly`, `session.cookie_secure` (HTTPS) ou `SameSite` sont **recommandés en production** via `php.ini` ou `session_set_cookie_params()` ; ils ne constituent pas une liste imposée par le dépôt tel quel.

### Secrets et fichiers sensibles

Les identifiants MySQL par défaut conviennent au **développement local** uniquement. En production : mots de passe forts, compte SQL à privilèges minimaux, et pas de secrets dans le dépôt Git.

## Recommandations par environnement

| Contexte | Mesures |
|----------|---------|
| Développement local | Variables `DB_*`, base jetable, pas d’exposition réseau large |
| Production | HTTPS obligatoire, durcissement session, CSRF sur les POST, sauvegardes base, rotation des logs |

## Checklist réaliste avant exposition publique

- [ ] Variables d’environnement pour la base, mots de passe forts  
- [ ] HTTPS et cookies de session `Secure` / `SameSite` adaptés  
- [ ] Jetons **CSRF** sur les actions modifiant l’état (formulaires POST)  
- [ ] Désactivation de l’affichage des erreurs PHP côté client  
- [ ] Compte MySQL à permissions minimales (pas de `DROP DATABASE` pour l’utilisateur applicatif si possible)  
- [ ] Revue des points d’entrée admin et des suppressions en masse  

## Ressources externes

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)  
- [Documentation sécurité PHP](https://www.php.net/manual/fr/security.php)  

---

Voir aussi : [Installation](installation.md), [Architecture](architecture.md), [Base de données](base-donnees.md)
