from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from seashell_parallel.views import classification_image

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('seashell_parallel.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
elif settings.ALLOW_EPHEMERAL_MEDIA:
    urlpatterns += [
        path(
            'media/<path:path>',
            classification_image,
            name='classification-image',
        ),
    ]
