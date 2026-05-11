# Documentation MkDocs (blog-mvc)

Site de documentation du projet blog-mvc, généré avec **MkDocs** et le thème **Material**.

## Prérequis

- Python 3.13+ (voir `.python-version`)
- [uv](https://docs.astral.sh/uv/) recommandé, ou `pip`

## Installation des dépendances

À la racine de ce dossier `documentation-mvc/` :

```bash
uv sync
```

Sans uv :

```bash
pip install mkdocs mkdocs-material
```

## Prévisualiser le site

Les fichiers sources sont dans `mvc-doc/` (configuration : `mvc-doc/mkdocs.yml`).

```bash
cd mvc-doc
uv run mkdocs serve
```

Puis ouvrez l’URL indiquée (souvent `http://127.0.0.1:8000`).

Alternative avec MkDocs déjà sur le PATH :

```bash
cd mvc-doc
mkdocs serve
```

## Build statique

```bash
cd mvc-doc
uv run mkdocs build
```

Le rendu HTML est produit dans `mvc-doc/site/`.
