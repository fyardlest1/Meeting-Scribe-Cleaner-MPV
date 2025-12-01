from celery import shared_task
from .utils import compress_pdf

@shared_task(bind=True)
def async_compress_pdf(self, temp_path, quality):
    try:
        out_path = compress_pdf(temp_path, quality=quality)
        return {
            "status": "completed",
            "output_path": out_path
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
