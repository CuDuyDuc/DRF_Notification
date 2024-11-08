from notification_be.apps.routers import path, RegisterView, LoginAPIView, UserDetailView, UserListView, UpdateProfileView, CreateShopView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register-user/', RegisterView.as_view(), name = 'register-user'),
    path('login-user/', LoginAPIView.as_view(), name = 'login-user'),
    path('list-users/', UserListView.as_view(), name='list-user'),
    path('create-shop/', CreateShopView.as_view(), name= 'create-shop'),
    path('detail-users/<uuid:pk>', UserDetailView.as_view(), name='detail-user'),
    path('update-profile/', UpdateProfileView.as_view(), name='profile-update'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)