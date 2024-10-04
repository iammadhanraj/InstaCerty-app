from django.shortcuts import render,redirect
from .forms import*
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from io import BytesIO
from django.http import HttpResponse,Http404
from django.core.files import File
from .models import Certificate
import qrcode
import tempfile
from PyPDF2 import PdfReader, PdfWriter
import os

def home(request):
    all_certificates=Certificate.objects.all()
    data={
        'certificates':all_certificates,
    }
    return render(request,'home.html',data)


def generate_certificate(request):
    if request.method == 'POST':
        form = CertificateForm(request.POST)
        if form.is_valid():
            # Extract form data
            name = form.cleaned_data['name']
            course = form.cleaned_data['course']
            instructor = form.cleaned_data['instructor']

            # Create and save Certificate object
            certificate = Certificate(name=name, course=course, instructor=instructor)
            certificate.save()

            # Generate QR code dynamically with certificate information
            qr_data = f"Certificate Number: {certificate.certificate_number}\nName: {certificate.name}\nCourse: {certificate.course}\nIssue Date: {certificate.issue_date}"
            qr_img = qrcode.make(qr_data)

             # Save the QR code to the certificate's qr_code field
            qr_io = BytesIO()  # Create an in-memory file object
            qr_img.save(qr_io, format='PNG')  # Save the QR code to the BytesIO object
            qr_io.seek(0)  # Move cursor to the beginning of the BytesIO object

            # Save the QR code to the certificate instance
            certificate.qr_code.save(f"{certificate.certificate_number}.png", File(qr_io), save=True)

            # Save QR code to a temporary file
            temp_qr_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
            qr_img.save(temp_qr_file.name)

            # Generate PDF certificate
            pdf_buffer = BytesIO()
            p = canvas.Canvas(pdf_buffer, pagesize=landscape(A4))  # A4 Landscape
            width, height = landscape(A4)

            # Add watermark or background image
            watermark_path = 'static/bg.jpg'
            p.saveState()
            p.setFillAlpha(1)
            p.drawImage(watermark_path, 0, 0, width=width, height=height, mask='auto')
            p.restoreState()

            ### Add Badge ###
            logo_path = 'static/badge.png'
            p.drawImage(logo_path, width - 740, height - 500, width=120, height=120, mask='auto')  # Adjust position

            # Add certificate content
            p.setFont('Helvetica-Bold', 30)
            p.drawCentredString(width / 2.0, height - 150, "Certificate of Completion")
            
            p.setFont('Helvetica', 18)
            p.drawCentredString(width / 2.0, height - 200, f"This certifies that {name}")
            p.drawCentredString(width / 2.0, height - 250, f"has successfully completed the course {course}.")
            p.drawCentredString(width / 2.0, height - 300, f"Instructor: {instructor}")
            p.drawCentredString(width / 2.0, height - 350, f"Certificate Number: {certificate.certificate_number}")
            p.drawCentredString(width / 2.0, height - 400, f"Issue Date: {certificate.issue_date.strftime('%d-%m-%Y')}")

            # # Draw border from PNG image
            # border_path = 'static/border-1.png'
            # p.drawImage(border_path, 0, 0, width=width, height=height, mask='auto')

            #Signature
            signature_path='static/Signature.png'
            p.drawImage(signature_path, width // 2 - 50, 100, width=100, height=60,mask='auto')


            # Add QR code image to the PDF from the temporary file
            p.drawImage(temp_qr_file.name, 620, 110, width=120, height=120)

            # Finalize the PDF
            p.showPage()
            p.save()

            # Move to the beginning of the PDF buffer
            pdf_buffer.seek(0)

            # Save the generated PDF file to the `pdf_file` field
            certificate.pdf_file.save(f'{certificate.certificate_number}.pdf', File(pdf_buffer), save=True)

            # Remove temporary QR file (cleanup)
            temp_qr_file.close()

            # Serve the PDF for download
            response = HttpResponse(pdf_buffer, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{certificate.certificate_number}.pdf"'

            return redirect('home')
        
        else:
            form = CertificateForm()

    else:
        form = CertificateForm()

    return render(request, 'certificate/certificate_form.html', {'form': form})


# View PDF in the browser
def view_pdf(request, certificate_id):
    try:
        certificate = Certificate.objects.get(id=certificate_id)
        pdf_file_path = certificate.pdf_file.path  # Path to the stored PDF
    except Certificate.DoesNotExist:
        raise Http404("Certificate not found")

    with open(pdf_file_path, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{certificate.certificate_number}.pdf"'
        return response

# Download PDF
def download_pdf(request, certificate_id):
    try:
        certificate = Certificate.objects.get(id=certificate_id)
        pdf_file_path = certificate.pdf_file.path  # Path to the stored PDF
    except Certificate.DoesNotExist:
        raise Http404("Certificate not found")

    with open(pdf_file_path, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{certificate.certificate_number}.pdf"'
        return response

