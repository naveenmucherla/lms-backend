import threading
from django.db import connection
from django.core.management import call_command

_migrated = False
_lock = threading.Lock()

class AutoMigrateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        global _migrated
        if not _migrated:
            with _lock:
                if not _migrated:
                    try:
                        tables = connection.introspection.table_names()
                        if 'accounts_user' not in tables:
                            print("=== AutoMigrateMiddleware: Running migrations & seeding ===")
                            call_command("migrate", interactive=False)
                            try:
                                from seed_data import seed_database
                                seed_database()
                            except Exception as se:
                                print("AutoMigrateMiddleware Seed Notice:", se)
                    except Exception as e:
                        print("AutoMigrateMiddleware Notice:", e)
                    _migrated = True
        return self.get_response(request)
