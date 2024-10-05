from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('generate', views.generate_certificate, name='generate_certificate'),
    path('certificate/<int:certificate_id>/view', views.view_pdf, name='view_pdf'),
    path('certificate/<int:certificate_id>/download', views.download_pdf, name='download_pdf'),
     path('delete/<int:id>', views.delete_certificate, name='delete_certificate'),
]