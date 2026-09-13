# Lancer WellCase en local

Depuis `WellCase/frontend` :

```bash
npm run dev
```

Cela lance automatiquement :
- Frontend React : http://localhost:3000
- Backend FastAPI : http://127.0.0.1:8000

Sous Windows, tu peux aussi double-cliquer sur `start-wellcase.bat` à la racine du projet.

Le script utilise `concurrently` et arrête les deux processus si l'un des deux s'arrête.
