from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Serve the SPA entrypoint
    path('', TemplateView.as_view(template_name='index.html')),
    # API endpoints for modular apps
    path('api/purchase_orders/', include('purchase_orders.urls')),
    path('api/request_payments/', include('request_payments.urls')),
    path('api/purchase_requisitions/', include('purchase_requisitions.urls')),
    path('api/goods_received/', include('goods_received.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
