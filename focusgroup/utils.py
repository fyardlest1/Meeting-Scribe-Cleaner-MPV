from django.urls import path
from . import views


urlpatterns = [
    path("upload/", views.MeetingUploadAPIView.as_view(), name="meeting_upload"),
    path("status/<int:meeting_id>/", views.MeetingStatusAPIView.as_view(), name="meeting_status"),
]
