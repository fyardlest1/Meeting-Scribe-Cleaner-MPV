from rest_framework import serializers
from .models import FocusGroupTranscript

class FocusGroupTranscriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = FocusGroupTranscript
        fields = "__all__"
