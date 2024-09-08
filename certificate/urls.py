from django.urls import path
from . import views

urlpatterns = [
    path('', views.generate_certificate, name='generate_certificate'),
]