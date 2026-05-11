# Guide utilisateur

Ce guide décrit l’usage du site **CSB Blog** pour un visiteur ou un compte enregistré.

## Page d’accueil

L’accueil liste les articles publiés, en général du plus récent au plus ancien, avec pagination si le nombre d’articles est élevé.

## Inscription

1. Cliquez sur **Inscription** dans le menu.  
2. Renseignez nom d’utilisateur, email et mot de passe (et confirmation si le formulaire le demande).  
3. Validez le formulaire.  
4. En cas de succès, vous êtes en général redirigé vers la page de **connexion**.

**Mot de passe** : préférez une phrase longue ou un mot de passe complexe ; le site peut imposer des règles minimales côté serveur.

## Connexion et déconnexion

- **Connexion** : email et mot de passe, puis menu vers l’accueil une fois authentifié.  
- **Déconnexion** : lien visible lorsque vous êtes connecté ; la session est terminée.

## Navigation principale (utilisateur connecté)

Selon les droits du compte, le menu peut inclure notamment :

- **Accueil** — liste des articles  
- **Recherche** — recherche par mots dans les titres ou contenus  
- **Profil** — consultation ou modification des informations du compte  
- **Admin** — uniquement si vous êtes **administrateur**  
- **Déconnexion**

## Lire un article

1. Cliquez sur le titre d’un article dans la liste.  
2. Le texte complet s’affiche, avec la zone des **commentaires** en dessous.

## Commentaires

### Publier un commentaire

1. Ouvrez la page de l’article.  
2. Connectez-vous si nécessaire.  
3. Si votre compte est **restreint** par un administrateur, l’ajout de commentaires peut être bloqué (message affiché à la place du formulaire).  
4. Sinon, saisissez votre texte dans le champ prévu et validez.

Les commentaires apparaissent sans étape de modération obligatoire dans l’application telle que livrée.

### Modifier ou supprimer **vos** commentaires

Pour les commentaires que **vous** avez écrits, l’interface prévoit un menu contextuel (clic droit sur le commentaire) permettant d’**éditer** ou de **supprimer** après confirmation. Les autres utilisateurs ne voient pas ces actions sur vos messages.

## Recherche

1. Ouvrez **Recherche**.  
2. Saisissez un ou plusieurs mots.  
3. Les résultats correspondent aux articles dont le titre ou le contenu contient la requête (comportement exact selon l’implémentation du contrôleur).

## Profil

- Affichage des informations du compte.  
- Possibilité de mettre à jour identifiants ou mot de passe selon les champs proposés sur la page **Profil**.

## Espace administrateur

Visible dans le menu uniquement pour les comptes **administrateur**.

Fonctions typiques :

- **Articles** : consulter la liste, **créer** un nouvel article (formulaire dédié), **supprimer** un article.  
- **Commentaires** : voir les commentaires du site et **supprimer** ceux qui posent problème.  
- **Utilisateurs** : liste des comptes, indication du statut admin, **restriction** ou **levée de restriction** d’un utilisateur non admin (un compte restreint ne peut plus commenter).  

La promotion d’un utilisateur au rang d’**admin** ne passe pas par une simple action de ce tableau dans la version décrite : elle suppose une modification en base ou un outillage supplémentaire.

## Dépannage rapide

| Problème | Piste |
|----------|--------|
| Impossible de se connecter | Vérifier email / mot de passe, casse du clavier, compte existant. |
| Pas de formulaire de commentaire | Être connecté ; compte non restreint. |
| Modification de profil sans effet | Vérifier les messages d’erreur affichés sur la page. |

---

Voir aussi : [Installation](installation.md), [Architecture](architecture.md)
