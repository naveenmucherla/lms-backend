import os
from django.conf import settings
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor

def generate_certificate_pdf(student_name, course_title, certificate_id):
    certificates_dir = os.path.join(settings.MEDIA_ROOT, "certificates")
    os.makedirs(certificates_dir, exist_ok=True)

    file_path = os.path.join(
        certificates_dir,
        f"{certificate_id}.pdf"
    )

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    # Colors
    blue = HexColor("#2563EB")

    # Background
    c.setFillColorRGB(1, 1, 1)
    c.rect(0, 0, width, height, fill=1)

    # Border
    c.setStrokeColor(blue)
    c.setLineWidth(4)
    c.rect(30, 30, width - 60, height - 60)

    # Title
    c.setFillColor(blue)
    c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(width / 2, height - 140, "CERTIFICATE OF COMPLETION")

    # Text
    c.setFont("Helvetica", 16)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(width / 2, height - 220, "This is to certify that")

    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(width / 2, height - 260, student_name)

    c.setFont("Helvetica", 16)
    c.drawCentredString(width / 2, height - 310, "has successfully completed the course")

    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(blue)
    c.drawCentredString(width / 2, height - 350, course_title)

    c.setFont("Helvetica", 12)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(width / 2, 120, f"Certificate ID: {certificate_id}")

    c.showPage()
    c.save()

    return file_path
