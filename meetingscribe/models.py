from django.db import models


class MeetingArtifact(models.Model):
    """
    Stores the raw transcript and the simulated structured output.
    """
    raw_transcript = models.TextField()
    # In a full production app, these would be JSONFields
    commitments_text = models.TextField(blank=True, default="")
    deadlines_text = models.TextField(blank=True, default="")
    followups_text = models.TextField(blank=True, default="")
    
    consent_given = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

