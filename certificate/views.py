from django.shortcuts import render
from .forms import*
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from io import BytesIO
from django.http import HttpResponse
from django.core.files import File
from PIL import Image, ImageDraw, ImageFont
import qrcode
import tempfile
from .models import Certificate

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
            qr_data = f"Certificate Number: {certificate.certificate_number}\nName: {certificate.name}\nCourse: {certificate.course}"
            qr_img = qrcode.make(qr_data)

            # Save QR code to a temporary file
            temp_qr_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
            qr_img.save(temp_qr_file.name)

            # Generate PDF certificate
            pdf_buffer = BytesIO()
            p = canvas.Canvas(pdf_buffer, pagesize=landscape(A4))  # A4 Landscape
            width, height = landscape(A4)

            # Add certificate content to the PDF
            p.setFont('Helvetica-Bold', 30)
            p.drawString(200, height - 100, "Certificate of Completion")
            p.setFont('Helvetica', 18)
            p.drawString(200, height - 150, f"This certifies that {name}")
            p.drawString(200, height - 200, f"has successfully completed the course {course}.")
            p.drawString(200, height - 250, f"Instructor: {instructor}")
            p.drawString(200, height - 300, f"Certificate Number: {certificate.certificate_number}")

            # Add QR code image to the PDF from the temporary file
            p.drawImage(temp_qr_file.name, width // 2 - 50, 50, width=100, height=100)

            # Finalize the PDF
            p.showPage()
            p.save()

            # Move to the beginning of the PDF buffer
            pdf_buffer.seek(0)

            # Save the generated PDF file to the `pdf_file` field
            certificate.pdf_file.save(f'{certificate.certificate_number}.pdf', File(pdf_buffer), save=True)

            # Generate PNG certificate
            img_width, img_height = (3508, 2480)  # A4 size at 300 dpi in landscape
            image = Image.new('RGB', (img_width, img_height), (255, 255, 255))  # White background
            draw = ImageDraw.Draw(image)

            # Load fonts (adjust the path to your font file if necessary)
            font_title = ImageFont.truetype('arial.ttf', 60)
            font_content = ImageFont.truetype('arial.ttf', 40)

            # Add certificate content to PNG
            draw.text((img_width // 4, 150), "Certificate of Completion", font=font_title, fill=(0, 0, 0))
            draw.text((img_width // 4, 300), f"This certifies that {certificate.name}", font=font_content, fill=(0, 0, 0))
            draw.text((img_width // 4, 450), f"has successfully completed the course {certificate.course}", font=font_content, fill=(0, 0, 0))
            draw.text((img_width // 4, 600), f"Instructor: {certificate.instructor}", font=font_content, fill=(0, 0, 0))
            draw.text((img_width // 4, 750), f"Certificate Number: {certificate.certificate_number}", font=font_content, fill=(0, 0, 0))

            # Add QR code to PNG at the bottom center
            qr_code_img = Image.open(temp_qr_file.name)
            qr_code_img = qr_code_img.resize((300, 300))
            image.paste(qr_code_img, ((img_width - 300) // 2, img_height - 400))
            # Save PNG to buffer
            png_buffer = BytesIO()
            image.save(png_buffer, format="PNG")
            png_buffer.seek(0)


            # Remove temporary QR file (cleanup)
            temp_qr_file.close()

            # Check which format the user wants to download (PDF or PNG)
            if request.POST.get('format') == 'pdf':
                # Serve the PDF
                response = HttpResponse(pdf_buffer, content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{certificate.certificate_number}.pdf"'
                return response
            else:
                response = HttpResponse(png_buffer, content_type='image/png')
                response['Content-Disposition'] = f'attachment; filename="{certificate.certificate_number}.png"'
                return response
        else:
            form = CertificateForm()

    else:
        form = CertificateForm()

    return render(request, 'certificate/certificate_form.html', {'form': form})
