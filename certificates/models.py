from django.db import models
from django.conf import settings
from courses.models import Course
import uuid

class Certificate(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    certificate_id = models.UUIDField(default=uuid.uuid4, unique=True)
    certificate_file = models.FileField(
        upload_to="certificates/",
        null=True,      
        blank=True      
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.course.title}"
