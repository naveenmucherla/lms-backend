import os
import uuid

from django.core.files.base import ContentFile
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.permissions import IsStudent
from courses.models import Course
from .models import Certificate
from .utils import generate_certificate_pdf



class DownloadCertificateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, certificate_id):
        certificate = get_object_or_404(
            Certificate,
            certificate_id=certificate_id
        )

        if certificate.student != request.user and not request.user.is_staff:
            return Response({"detail": "Unauthorized"}, status=403)

        if not certificate.certificate_file:
            return Response({"detail": "Certificate file missing"}, status=404)

        if not os.path.exists(certificate.certificate_file.path):
            return Response(
                {"detail": "Certificate file not found on server"},
                status=404
            )

        return FileResponse(
            open(certificate.certificate_file.path, "rb"),
            content_type="application/pdf",
            as_attachment=True,
            filename=f"{certificate_id}.pdf"
        )



class GenerateCertificateView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def post(self, request, course_id):
        student = request.user
        course = get_object_or_404(Course, id=course_id)

        existing = Certificate.objects.filter(
            student=student,
            course=course
        ).first()

        if existing and existing.certificate_file:
            return Response({
                "certificate_id": existing.certificate_id,
                "message": "Certificate already generated"
            })

        certificate_id = str(uuid.uuid4())

        pdf_path = generate_certificate_pdf(
            student.username,
            course.title,
            certificate_id
        )

        # Read PDF safely
        with open(pdf_path, "rb") as f:
            pdf_content = f.read()

        certificate = Certificate.objects.create(
            student=student,
            course=course,
            certificate_id=certificate_id,
        )

        # ✅ Save WITHOUT allowing Django to rename
        certificate.certificate_file.save(
            f"certificates/{certificate_id}.pdf",
            ContentFile(pdf_content),
            save=True
        )

        return Response({
            "certificate_id": certificate_id,
            "message": "Certificate generated successfully"
        }, status=201)



class VerifyCertificateView(APIView):
    def get(self, request, certificate_id):
        cert = get_object_or_404(
            Certificate,
            certificate_id=certificate_id
        )

        return Response({
            "valid": True,
            "student": cert.student.username,
            "course": cert.course.title,
            "certificate_id": cert.certificate_id,
        })
