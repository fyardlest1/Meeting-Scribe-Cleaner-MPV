from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class FocusGroupTranscript(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_file = models.FileField(upload_to="meetings/")
    transcript = models.TextField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    action_items = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="pending")

    def __str__(self):
        return f"Transcript {self.id} for {self.user}"

