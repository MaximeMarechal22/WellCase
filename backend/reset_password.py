import argparse
import getpass
import sys

from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash


def main() -> int:
    parser = argparse.ArgumentParser(description='Reset a WellCase user password safely.')
    parser.add_argument('username', help='Exact username to reset')
    args = parser.parse_args()

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == args.username).first()
        if user is None:
            print(f'ERREUR: utilisateur introuvable: {args.username}')
            return 1

        if not user.is_active:
            print('ERREUR: ce compte est désactivé.')
            return 1

        p1 = getpass.getpass('Nouveau mot de passe: ')
        p2 = getpass.getpass('Confirmez le mot de passe: ')
        if not p1:
            print('ERREUR: mot de passe vide.')
            return 1
        if p1 != p2:
            print('ERREUR: les mots de passe ne correspondent pas.')
            return 1

        if len(p1) < 6:
            print('ERREUR: minimum 6 caractères.')
            return 1

        user.hashed_password = get_password_hash(p1)
        db.commit()
        print(f'OK: mot de passe réinitialisé pour {user.username}.')
        print(f'Compte ID: {user.id} | Admin: {bool(user.is_admin)} | Balance: {user.virtual_balance:.2f} €')
        return 0
    except Exception as exc:
        db.rollback()
        print(f'ERREUR: {exc}')
        return 1
    finally:
        db.close()


if __name__ == '__main__':
    raise SystemExit(main())
