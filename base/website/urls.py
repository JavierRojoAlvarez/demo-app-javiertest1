from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('basic.urls')),
    path('', include('my_app.urls')),
    path('tracker/', include('tracker.urls')),
    path('api/', include('api.urls')),
    path('accounting/', include('accounting.urls')),
    path('invoice/', include('invoice.urls')),
    path('users/', include('users.urls')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
