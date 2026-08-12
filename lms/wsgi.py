import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lms.settings')

application = get_wsgi_application()

# Automated database migration & seeding on container boot (Render/Production)
try:
    from django.core.management import call_command
    print("=== Auto-running database migrations on WSGI startup ===")
    call_command("migrate", interactive=False)
    
    from seed_data import seed_database
    print("=== Auto-seeding database records on WSGI startup ===")
    seed_database()
except Exception as e:
    print(f"WSGI Auto-bootstrap notice: {e}")
