
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from n1.admin import another


admin.site.site_header = "admin_panel"
admin.site.site_title = "title_panel"
admin.site.index_title = "index_panel"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('anotheradmin/', another.urls),
    path('n1/', include('n1.urls')),
    path('n2/', include('n2.urls')),
    # migration is required for this
    path('silk/', include('silk.urls'), name='silk'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

# uvicorn final.asgi:application --reload
# atlast static file man!!
