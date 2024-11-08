from notification_be.apps.routers import path, AddCartViewAPI, ListCartViewAPI, UpdateCartViewAPI, DeleteCartViewAPI

urlpatterns = [
    path('cart/', AddCartViewAPI.as_view(), name= 'addCart'),
    path('list-cart/', ListCartViewAPI.as_view(), name= 'listCart'),
    path('update-cart/<uuid:pk>', UpdateCartViewAPI.as_view(), name= 'updateCart'),
    path('delete-cart/<uuid:pk>', DeleteCartViewAPI.as_view(), name= 'deleteCart'),
]