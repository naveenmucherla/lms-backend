import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms.settings')
django.setup()

from django.core.management import call_command
from django.core.wsgi import get_wsgi_application
from django.db import connection

# Ensure database tables and seed data are populated on container boot
try:
    tables = connection.introspection.table_names()
    if 'accounts_user' not in tables:
        print("=== Table 'accounts_user' missing! Running migrations & seeding ===")
        call_command("migrate", interactive=False)
        from seed_data import seed_database
        seed_database()
except Exception as err:
    print(f"WSGI Bootstrap Notice: {err}")
    try:
        call_command("migrate", interactive=False)
        from seed_data import seed_database
        seed_database()
    except Exception as e2:
        print(f"WSGI Force Migration Exception: {e2}")

application = get_wsgi_application()
