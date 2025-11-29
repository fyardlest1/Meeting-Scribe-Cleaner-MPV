from django.urls import path
from . import views


urlpatterns = [
    path('', views.input_view, name='input'),
    path('review/<int:pk>/', views.review_view, name='review'),
    path('export/<int:pk>/export/', views.export_pdf_view, name='export_pdf'),
]