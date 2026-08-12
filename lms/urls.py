from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

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
