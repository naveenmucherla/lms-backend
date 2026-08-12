import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms.settings')
django.setup()

from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

print("=== Running DB Migrations on WSGI Startup ===")
try:
    call_command("migrate", interactive=False)
except Exception as e:
    print(f"Migration warning: {e}")

print("=== Running Seed Data on WSGI Startup ===")
try:
    from seed_data import seed_database
    seed_database()
except Exception as e:
    print(f"Seeding warning: {e}")

application = get_wsgi_application()
