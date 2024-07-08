from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('lista.urls',)),
    # path('chaining/', include('smart_selects.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


if settings.DEBUG == False:
    handler400 = 'lista.views.error_400'
    handler403 = 'lista.views.error_403'
    handler404 = 'lista.views.error_404'
    handler500 = 'lista.views.error_500'
