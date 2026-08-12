from django.contrib import admin
from .models import Certificate

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'student',
        'course',
        'certificate_id',
    )
    search_fields = ('certificate_id', 'student__username', 'course__title')
