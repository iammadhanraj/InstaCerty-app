
# InstaCerty!

This app use to generate instant certificates,
A Django-based web application that generates certificates in PDF formats, with customizable fields like name, course, instructor, and a QR code. The app also includes features for downloading certificates, and managing uploaded certificates (including file deletions).


## Website
**Home Page**

![Logo](https://raw.githubusercontent.com/iammadhanraj/mystaticfiles/main/InstaCerty/home_page.png)
**Generate Page**

![Logo](https://raw.githubusercontent.com/iammadhanraj/mystaticfiles/main/InstaCerty/generate_page.png)
## Samples
![Logo](https://raw.githubusercontent.com/iammadhanraj/mystaticfiles/main/InstaCerty/Sample_Certificate.png)
## Features
### 1. Generate Certificates
- **Input Fields:** Allows users to input the name, course, instructor, and other details.
- **Dynamic PDF Generation:** Automatically generates certificates in both PDF using the provided information.
- **Customizable Layout:** The certificates are designed in A4 landscape format with a user-defined border and a background watermark or logo and signature also.
### 2. QR Code Integration
- A QR code is automatically generated and added to the bottom of the certificate.
- The QR code encodes information such as the certificate number,name, course like allowing for quick verification.
### 3. File Handling
- **Upload & Store:** The application stores the generated certificates (PDF) and QR code in the media directory and links them to their corresponding database entries.
- **File Deletion:** If a certificate is deleted, its corresponding files (PDF, PNG) are removed from the file system to avoid storage bloat.
### 4. Download Certificates
- **Downloadable**: Users can download the certificate PDF from a button available after generation.
### 5. User-Friendly Form Handling
- **Bootstrap Integration:** The app uses Bootstrap for responsive design, including a clean and intuitive form interface.
### 6. Date Formatting
- The application formats dates in the day-month-year format for consistency on certificates.
### 7. Success Messages System
- We can see success message after generate/delete the certificates.
  
## Getting Started
### Prerequisites
- Python 3.x
- Django 3.x or later
- Pillow for image handling
- qrcode for QR code generation
- reportlab for generate pdf
- Bootstrap for frontend design (included via CDN)
## Installation

1.Clone the repository:

```bash
https://github.com/iammadhanraj/InstaCerty-app
```
2.Navigate to the project directory:
```bash
cd InstaCerty
```
3.Install the required packages:
```bash
pip install -r requirements.txt
``` 
4.Run migrations to set up the database:
```bash
python manage.py migrate
``` 
5.Create a superuser for admin access:
```bash 
python manage.py createsuperuser
```
6.Run the Django development server:
```bash 
python manage.py runserver
```



## Configuration
- **Media Files:** Ensure you have the following settings configured in your settings.py:
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```
