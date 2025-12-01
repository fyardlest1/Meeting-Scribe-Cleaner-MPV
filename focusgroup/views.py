from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from .models import FocusGroupTranscript
from .serializers import FocusGroupTranscriptSerializer
from .tasks import process_meeting_task


class MeetingUploadAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file = request.FILES.get("file")

        if not file:
            return Response({"error": "No file uploaded"}, status=400)

        meeting = FocusGroupTranscript.objects.create(
            user=request.user,
            original_file=file
        )

        process_meeting_task.delay(meeting.id)

        return Response({
            "meeting_id": meeting.id,
            "status_url": f"/api/meetingscribe/status/{meeting.id}/"
        })


class MeetingStatusAPIView(APIView):
    def get(self, request, meeting_id):
        meeting = FocusGroupTranscript.objects.get(id=meeting_id)
        serializer = FocusGroupTranscriptSerializer(meeting)
        return Response(serializer.data)

