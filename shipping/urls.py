from django.urls import path
from .views import (
    CourierPrice, CourierAuthorization, CourierCreateOrder, CourierOrderStatus, ListCourierViewSet,
    CourierCancellOrder
)

urlpatterns = [
    path('<int:pk>/price/', CourierPrice.as_view(), name='courier_price'),
    path('list/', ListCourierViewSet.as_view(), name='courier_list'),
    path('<int:pk>/create_order/', CourierCreateOrder.as_view(), name='create_shipping_order'),
    path('<int:pk>/order_status/', CourierOrderStatus.as_view(), name='order_status'),
    path('authorize/', CourierAuthorization.as_view(), name='courier_authorize'),
    path('<int:pk>/cancell/', CourierAuthorization.as_view(), name='courier_cancell_order'),
]