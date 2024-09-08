import uuid
from django.db import models
from io import BytesIO
import qrcode
from django.core.files import File

class Certificate(models.Model):
    name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    instructor = models.CharField(max_length=100)
    issue_date = models.DateField(auto_now_add=True)
    certificate_number = models.CharField(max_length=12, unique=True, blank=True,editable=False)
    qr_code = models.ImageField(upload_to='certificates/png', blank=True)
    pdf_file = models.FileField(upload_to='certificates/pdf', blank=True, null=True)

    def __str__(self):
        return self.certificate_number

    def save(self, *args, **kwargs):
        # Generate a unique certificate number
        if not self.certificate_number:
            self.certificate_number = (str(uuid.uuid4()).replace('-', '')[:12]).upper()
        
        super().save(*args, **kwargs)
        
        # Generate QR code
        # qr_image = qrcode.make(f"Certificate: {self.certificate_number}\nName: {self.name}\nCourse: {self.course}")
        # buffer = BytesIO()
        # qr_image.save(buffer, format="PNG")
        # self.qr_code.save(f'instacerty_{self.certificate_number}.png', File(buffer), save=False)

        # super().save(*args, **kwargs)
