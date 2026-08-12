import threading
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
                        print("=== AutoMigrateMiddleware: Running migrate ===")
                        call_command("migrate", interactive=False)
                        try:
                            from seed_data import seed_database
                            print("=== AutoMigrateMiddleware: Running seed_database ===")
                            seed_database()
                        except Exception as se:
                            print("Seed Error:", se)
                    except Exception as me:
                        print("Migrate Error:", me)
                    _migrated = True
        return self.get_response(request)
