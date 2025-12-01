from celery import shared_task
from .utils import transcribe_audio, generate_summary, generate_action_items


@shared_task(bind=True)
def process_meeting_task(self, meeting_id):
    from .models import MeetingTranscript
    meeting = MeetingTranscript.objects.get(id=meeting_id)

    meeting.status = "processing"
    meeting.save()

    text = transcribe_audio(meeting.original_file.path)
    meeting.transcript = text

    meeting.summary = generate_summary(text)
    meeting.action_items = generate_action_items(text)

    meeting.status = "completed"
    meeting.save()

    return {"meeting_id": meeting.id, "status": "completed"}
