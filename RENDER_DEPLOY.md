# WellCase — déploiement Render stable

Cette version est prévue pour **un seul Web Service Render** : FastAPI sert aussi le build React et les images, donc le front et l'API partagent exactement la même origine.

## 1. Créer le service

Dans Render, crée un **Web Service** depuis le dépôt/ZIP extrait et utilise :

- Runtime : Docker
- Dockerfile : `Dockerfile`
- Health check : `/health`

Le `render.yaml` inclus peut aussi être utilisé via un Blueprint.

## 2. Variables obligatoires

Configure une base persistante, idéalement PostgreSQL :

```text
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST/DB?sslmode=require
```

Optionnel :

```text
ADMIN_USERNAME=tonpseudo
FRONTEND_URLS=https://wellcase.onrender.com
FRONTEND_ORIGIN_REGEX=https://.*\\.onrender\\.com
```

## 3. Ce que fait le démarrage

Au démarrage, le backend :

- crée les tables manquantes ;
- ajoute les colonnes de progression absentes ;
- **recrée/répare le catalogue de base** si une DB neuve ou partiellement vide est utilisée ;
- synchronise les 30 skins du catalogue ;
- synchronise les 14 caisses ;
- synchronise les pools de récompenses ;
- corrige les anciens chemins d'images stockés en DB.

## 4. Images

Les images des caisses et skins sont maintenant **importées dans le bundle React** au lieu d'être uniquement lues depuis `public/` ou la DB.

Le backend sert aussi `/images/*` depuis le build React sur Render.

## 5. API

En production, le frontend utilise la même origine :

```text
https://wellcase.onrender.com/cases/
https://wellcase.onrender.com/openings/1
https://wellcase.onrender.com/market/
```

Tu n'as donc plus de dépendance cachée à un `/api` séparé.
