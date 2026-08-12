from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.core.management import call_command

# Idempotently run migrations and seed data when URLs module is initialized
try:
    print("=== Running DB Migrations & Seeding ===")
    call_command("migrate", interactive=False)
    from seed_data import seed_database
    seed_database()
except Exception as e:
    print(f"Auto-Migrate Notice: {e}")

from accounts.views import InitDBView

urlpatterns = [
    path("api/", lambda request: JsonResponse({
        "status": "LMS Backend API is running"
    })),
    path("api/init-db/", InitDBView.as_view()),

    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/accounts/", include("accounts.urls")),
    path("api/courses/", include("courses.urls")),
    path("api/progress/", include("progress.urls")),
    path("api/certificates/", include("certificates.urls")),
]
