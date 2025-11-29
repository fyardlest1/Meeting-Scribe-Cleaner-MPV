from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from io import BytesIO
from xhtml2pdf import pisa

from .forms import TranscriptForm, mock_ai_synthesis
from .models import MeetingArtifact


def input_view(request):
    """
    Landing page: Focuses on Trust and Input.
    """
    if request.method == 'POST':
        form = TranscriptForm(request.POST)
        if form.is_valid():
            # 1. Save Raw Data
            artifact = form.save(commit=False)
            
            # 2. Simulate AI Processing
            synthesis = mock_ai_synthesis(artifact.raw_transcript)
            
            artifact.commitments_text = synthesis['commitments']
            artifact.deadlines_text = synthesis['deadlines']
            artifact.followups_text = synthesis['followups']
            artifact.save()
            
            return redirect('review', pk=artifact.pk)
    else:
        form = TranscriptForm()
        
    return render(request, "input-view.html", {"form": form})


def review_view(request, pk):
    """
    The Unified Review Interface.
    Allows users to edit the AI output ("Human in the loop").
    """
    artifact = get_object_or_404(MeetingArtifact, pk=pk)

    return render(request, "meeting-artifact-review.html", {"artifact": artifact})


def export_pdf_view(request, pk):
    """
    Handles saving the edits and generating the PDF.
    """
    artifact = get_object_or_404(MeetingArtifact, pk=pk)

    # 1. Save the edited content from the form
    if request.method == 'POST':
        artifact.commitments_text = request.POST.get('commitments_text', artifact.commitments_text)
        artifact.deadlines_text = request.POST.get('deadlines_text', artifact.deadlines_text)
        artifact.followups_text = request.POST.get('followups_text', artifact.followups_text)
        artifact.save()

    # 2. Render HTML template to string
    html = render_to_string('meeting-artifact-pdf.html', {'artifact': artifact})

    # 3. Generate PDF
    result = BytesIO()
    #  Fix: pass the HTML string directly
    pdf = pisa.CreatePDF(src=html, dest=result)

    if not pdf.err:
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        filename = f"Meeting_Report_{artifact.id}.pdf"
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response

    return HttpResponse('Error Generating PDF', status=400)