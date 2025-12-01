# pdfcompressor/forms.py
from django import forms


COMPRESSION_CHOICES = [
    ("screen", "Low (Smallest file, lowest quality)"),
    ("ebook", "Medium (Good balance)"),
    ("printer", "High (Better quality, bigger file)"),
]

class PDFUploadForm(forms.Form):
    pdf_file = forms.FileField(
        label="Upload your PDF",
        widget=forms.FileInput(
            attrs={
                "class": "w-full text-sm text-gray-700 border border-gray-300 rounded-lg p-3 bg-white cursor-pointer"
            }
        )
    )

    quality = forms.ChoiceField(
        choices=COMPRESSION_CHOICES,
        initial='ebook',
        widget=forms.Select(
            attrs={
                "class": "w-full text-sm text-gray-700 border border-gray-300 rounded-lg p-3 bg-white"
            }
        )
    )
