from django.urls import path, include

urlpatterns = [
    path('user/', include('notification_be.apps.routers.router_user')),
    path('product/', include('notification_be.apps.routers.router_product')),
    path('cart/', include('notification_be.apps.routers.router_cart')),
    path('order/', include('notification_be.apps.routers.router_order'))
]