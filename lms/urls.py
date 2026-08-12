from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.core.management import call_command
from django.db import connection

# Auto-migrate & seed database on URL loading (when apps are 100% ready)
try:
    tables = connection.introspection.table_names()
    if 'accounts_user' not in tables:
        print("=== URLs Auto-Migrate: Creating database tables & seeding ===")
        call_command("migrate", interactive=False)
        from seed_data import seed_database
        seed_database()
except Exception as e:
    print(f"URL Auto-Migrate Notice: {e}")

urlpatterns = [
    path("api/", lambda request: JsonResponse({
        "status": "LMS Backend API is running"
    })),

    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/accounts/", include("accounts.urls")),
    path("api/courses/", include("courses.urls")),
    path("api/progress/", include("progress.urls")),
    path("api/certificates/", include("certificates.urls")),
]
