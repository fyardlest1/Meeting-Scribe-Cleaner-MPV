from django import forms

from .models import MeetingArtifact


class TranscriptForm(forms.ModelForm):
    consent_given = forms.BooleanField(
        required=True,
        label="I consent to processing this meeting data.",
        help_text="Required for legal compliance."
    )

    class Meta:
        model = MeetingArtifact
        fields = ['raw_transcript', 'consent_given']
        widgets = {
            'raw_transcript': forms.Textarea(attrs={
                'class': 'w-full p-4 border rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 h-64',
                'placeholder': 'Paste your meeting transcript here... \n\nExample: "John said he will finish the report by Friday. Sarah agreed to review the budget next week. We need to follow up on the client contract."'
            }),
            'consent_given': forms.CheckboxInput(attrs={
                'class': 'h-5 w-5 text-blue-600 focus:ring-blue-500 border-gray-300 rounded'
            })
        }


def mock_ai_synthesis(text):
    """
    Simulates the "Intelligent Glue Layer".
    Instead of calling an expensive API, we use simple keyword heuristics
    to demonstrate the separation of concerns (Deadlines vs Commitments).
    """
    sentences = text.replace('\n', ' ').split('.')
    commitments = []
    deadlines = []
    followups = []

    for scribe in sentences:
        clean_scribe = scribe.strip()
        if not clean_scribe:
            continue
            
        lower_scribe = clean_scribe.lower()
        
        # Simple heuristic simulation
        if any(x in lower_scribe for x in ['by ', 'due ', 'until ', 'monday', 'tuesday', 'friday']):
            deadlines.append(clean_scribe)
        elif any(x in lower_scribe for x in ['will', 'going to', 'promise', 'agree']):
            commitments.append(clean_scribe)
        else:
            followups.append(clean_scribe)

    return {
        'commitments': "\n".join(f"- {c}" for c in commitments),
        'deadlines': "\n".join(f"- {c}" for c in deadlines),
        'followups': "\n".join(f"- {c}" for c in followups),
    }