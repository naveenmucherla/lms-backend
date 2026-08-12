import sys
from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        # Prevent running during CLI management commands like migrate/makemigrations
        if any(cmd in sys.argv for cmd in ['migrate', 'makemigrations', 'collectstatic']):
            return

        try:
            from django.db import connection
            tables = connection.introspection.table_names()
            if 'accounts_user' not in tables:
                print("=== Auto-migrating and seeding database on startup ===")
                from django.core.management import call_command
                call_command("migrate", interactive=False)
                from seed_data import seed_database
                seed_database()
        except Exception as e:
            print("Auto-migrate notice:", e)
