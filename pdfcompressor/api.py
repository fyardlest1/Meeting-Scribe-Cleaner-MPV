import os
import uuid
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .utils import compress_pdf
from .tasks import async_compress_pdf

from celery.result import AsyncResult
from celery import current_app


class CompressAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format=None):
        # Get uploaded file + quality
        file = request.FILES.get('file')
        quality = request.data.get('quality', 'ebook')

        if not file:
            return Response({'detail': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

        # Save uploaded file temporarily
        temp_name = f'tmp_{uuid.uuid4().hex}_{file.name}'
        temp_path = os.path.join(settings.MEDIA_ROOT, temp_name)
        os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

        with open(temp_path, 'wb+') as f:
            for chunk in file.chunks():
                f.write(chunk)

        # Launch Celery async job
        task = async_compress_pdf.delay(temp_path, quality)

        # Client receives the task ID and polling URL
        return Response({
            "task_id": task.id,
            "status_url": f"/api/pdf/status/{task.id}/"
        }, status=status.HTTP_202_ACCEPTED)


class TaskStatusAPIView(APIView):
    def get(self, request, task_id):
        result = AsyncResult(task_id)
        return Response({
            "task_id": task_id,
            "state": result.state,
            "result": result.result
        })

# class CompressAPIView(APIView):
#     parser_classes = (MultiPartParser, FormParser)

#     def post(self, request, format=None):
#         # Get uploaded file and compression quality
#         file = request.FILES.get('file')
#         quality = request.data.get('quality', 'ebook')

#         if not file:
#             return Response({'detail': 'No file uploaded'}, status=status.HTTP_400_BAD_REQUEST)

#         # Save uploaded file temporarily
#         temp_name = f'tmp_{uuid.uuid4().hex}_{file.name}'
#         temp_path = os.path.join(settings.MEDIA_ROOT, temp_name)
#         os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

#         with open(temp_path, 'wb+') as f:
#             for chunk in file.chunks():
#                 f.write(chunk)

#         # Compress the PDF
#         try:
#             # 🚨 Correction : ne pas passer settings.MEDIA_ROOT
#             out_path = compress_pdf(temp_path, quality=quality)
#         except Exception as e:
#             return Response({'detail': f'Compression failed: {str(e)}'},
#                             status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         # Prepare response
#         response_data = {
#             'before_size': round(os.path.getsize(temp_path)/1024/1024, 3),  # en MB
#             'after_size': round(os.path.getsize(out_path)/1024/1024, 3),    # en MB
#         }

#         if settings.DEBUG:
#             # For development, return local download path
#             response_data['download_path'] = out_path
#         else:
#             # In production: generate secure URL (e.g., presigned S3 link)
#             # Example placeholder:
#             response_data['download_url'] = f'https://yourcdn.com/secure/{os.path.basename(out_path)}'

#         return Response(response_data, status=status.HTTP_200_OK)



