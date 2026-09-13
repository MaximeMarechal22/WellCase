# Réinitialiser un mot de passe WellCase

Le compte `Maxime` est conservé. Pour changer uniquement son mot de passe sans toucher au solde, inventaire, XP, badges, prestige ou rôle admin :

```bat
cd D:\WellCase\backend
python reset_password.py Maxime
```

Le script demande le nouveau mot de passe deux fois et utilise la base configurée par `DATABASE_URL` (Neon).

Ne partage jamais ton mot de passe dans le chat.
