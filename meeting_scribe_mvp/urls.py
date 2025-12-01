from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # project/urls.py
    path('admin/', admin.site.urls),
    # apps/urls
    path('', include('meetingscribe.urls')),
    path("pdfcompressor/", include("pdfcompressor.urls")),
    path('api/', include('pdfcompressor.urls_api')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
