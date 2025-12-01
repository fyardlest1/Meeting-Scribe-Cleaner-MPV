# pdfcompressor/urls_api.py
from django.urls import path
from .api import CompressAPIView, TaskStatusAPIView


urlpatterns = [
    path('compress/', CompressAPIView.as_view(), name='compress_pdf_async'),
    path("status/<str:task_id>/", TaskStatusAPIView.as_view(), name="compress_status"),
]
