from django.shortcuts import render
from django.http import FileResponse
from django.conf import settings
from django.utils import timezone
import os
import uuid
import tempfile


from .forms import PDFUploadForm
from .utils import compress_pdf


def human_size(nb_bytes):
    return round(nb_bytes / 1024 / 1024, 3)


def compress_view(request):
    context = {
        "before_size": None,
        "after_size": None,
        "download_ready": False,
    }

    if request.method == "POST":
        form = PDFUploadForm(request.POST, request.FILES)

        if form.is_valid():
            pdf = request.FILES["pdf_file"]
            quality = form.cleaned_data["quality"]

            # Save uploaded PDF temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                for chunk in pdf.chunks():
                    tmp.write(chunk)
                temp_in = tmp.name

            before_size = os.path.getsize(temp_in)

            # Compress
            output_path = compress_pdf(temp_in, quality=quality)
            after_size = os.path.getsize(output_path)

            # Update context
            context["before_size"] = human_size(before_size)
            context["after_size"] = human_size(after_size)
            context["download_ready"] = True

            # -----------------------------
            # 🔥 1. Add compression history
            # -----------------------------
            history = request.session.get("compression_history", [])

            history_entry = {
                "filename": pdf.name,
                "original_size": round(before_size / 1024 / 1024, 3),
                "final_size": round(after_size / 1024 / 1024, 3),
                "quality": quality,
                "date": timezone.now().strftime("%Y-%m-%d %H:%M"),
            }

            # Put latest at the top
            history.insert(0, history_entry)

            # Keep only last 5 items
            history = history[:5]

            request.session["compression_history"] = history
            request.session.modified = True
            # -----------------------------

            # Return compressed file
            return FileResponse(
                open(output_path, "rb"),
                as_attachment=True,
                filename=f"compressed-{uuid.uuid4().hex}.pdf"
            )

    else:
        form = PDFUploadForm()

    context["form"] = form
    return render(request, "pdfcompressor/compress.html", context)


