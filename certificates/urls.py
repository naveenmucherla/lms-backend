from django.urls import path
from .views import GenerateCertificateView, DownloadCertificateView, VerifyCertificateView

urlpatterns = [
    path(
        "generate/<int:course_id>/",
        GenerateCertificateView.as_view(),
        name="generate-certificate",
    ),

    path(
        "download/<uuid:certificate_id>/",
        DownloadCertificateView.as_view(),
        name="download-certificate",
    ),

    path(
        "verify/<uuid:certificate_id>/",
        VerifyCertificateView.as_view(),
        name="verify-certificate",
    ),
]
