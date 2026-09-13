# WellCase Premium V4 — History / Assets / Upgrade

## Correctifs
- Historique backend: correction du shadowing `upgrade` qui cassait `/history`, événements newest-first, clés uniques et détails d'items/cases.
- Historique frontend: nouvelle UI premium avec filtres, images, succès/échec Upgrade et soldes réels des ouvertures/upgrades.
- Images: remplacement des assets incohérents par des renders générés et mappés 1:1 sur les 22 IDs existants. Les chemins DB restent stables.
- Caisses: assets recadrés pour supprimer les anciens prix/noms imprimés dans les images; prix/noms viennent désormais uniquement de la DB.
- Upgrade: nouvelle machine d'Upgrade animée, roulette de cible, pointeur central, probabilité, état UPGRADING et reveal succès/échec.
- Inventaire: suppression de l'affichage Float.
- Fallback images: fallback neutre au lieu d'un avatar rouge.
- Ouverture: overlay non fermable accidentellement pendant l'animation.

## Validation
- `python3 -m compileall -q backend/app` : OK
- Le ZIP n'inclut pas `frontend/node_modules`; lancer `npm install` puis `npm start`.
