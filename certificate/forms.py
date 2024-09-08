from django import forms

class CertificateForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=100)
    course = forms.CharField(label='Course Name', max_length=100)
    instructor = forms.CharField(label='Instructor Name', max_length=100)
