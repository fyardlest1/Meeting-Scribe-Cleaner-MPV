# pdfcompressor/models.py
from django.db import models


# class PDFCompression(models.Model):
#     original_file = models.FileField(upload_to="pdf_uploads/")
#     compressed_file = models.FileField(upload_to="pdf_compressed/", null=True, blank=True)
#     uploaded_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.original_file.name

