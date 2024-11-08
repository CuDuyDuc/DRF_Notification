from notification_be.apps.routers import  AddOrderViewAPI,path

urlpatterns = [
    path('add-order/', AddOrderViewAPI.as_view(), name= 'addOder'),
]