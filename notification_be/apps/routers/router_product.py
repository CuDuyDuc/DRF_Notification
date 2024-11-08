from notification_be.apps.routers import path, AddProductViewAPI, UpdateProductViewAPI, ListProductAPIView, SearchProductAPIView, ListProductOffsets
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('product/', AddProductViewAPI.as_view(), name='add'),
    path('list-product/', ListProductAPIView.as_view(), name='list'),
    path('update-product/<uuid:pk>', UpdateProductViewAPI.as_view(), name='update'),
    path('search-product/', SearchProductAPIView.as_view(), name='search'),
    path('get-products-offset/', ListProductOffsets.as_view(), name='get-products-offset'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)