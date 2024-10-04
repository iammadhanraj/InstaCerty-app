import uuid
from django.db import models
from io import BytesIO
import qrcode
from django.core.files import File
import os
class Certificate(models.Model):
    name = models.CharField(max_length=100)
    course = models.CharField(max_length=100)
    instructor = models.CharField(max_length=100)
    issue_date = models.DateField(auto_now_add=True)
    certificate_number = models.CharField(max_length=12, unique=True, blank=True,editable=False)
    qr_code = models.ImageField(upload_to='certificates/QR', blank=True)
    pdf_file = models.FileField(upload_to='certificates/pdf', blank=True, null=True)

    def __str__(self):
        return self.certificate_number

    def save(self, *args, **kwargs):
        # Generate a unique certificate number
        if not self.certificate_number:
            self.certificate_number = (str(uuid.uuid4()).replace('-', '')[:12]).upper()
        
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete associated files (pdf_file and png_file) from storage
        if self.pdf_file:
            if os.path.isfile(self.pdf_file.path):  # Check if file exists in storage
                os.remove(self.pdf_file.path)       # Delete the file from storage
                
        if self.qr_code:
            if os.path.isfile(self.qr_code.path):   # Check if file exists in storage
                os.remove(self.qr_code.path)        # Delete the QR code from storage

        # Call the parent class delete() method to delete the instance from the database
        super(Certificate, self).delete(*args, **kwargs)
        
