from django.shortcuts import render
from rest_framework import generics
from .serializers import CourierListSerializer
from .models import Courier
from inventory.models import Product
from payment.models import Order
from rest_framework.permissions import IsAuthenticated
from .ship import ShipClient
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from accounts.models import UserAddress
from django.core.cache import cache
from .serializers import PackagePriceSerializer, CourierCreateOrderSerializer


User = get_user_model()

class ListCourierViewSet(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CourierListSerializer
    queryset = Courier.objects.all()


class CourierPrice(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = PackagePriceSerializer

    def post(self, request, *args, **kwargs):
        """
            return courier price for product.
        """
        product = self.get_object()

        # country id for store
        product_price = ShipClient(product, courier).get_country(
            country_name=product.storehouse.store.country_name, Authorization=''
        )

        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        # where product stored
        from_latitude = product.storehouse.latitude
        from_longitude = product.storehouse.longitude
        dimensions_length = product.storehouse.dimensions_length
        dimensions_weight = product.storehouse.dimensions_weight

        get_price_data_serializer = {
            'from_latitude_value':from_latitude,
            'from_longitude_value': from_longitude,
            'to_latitude_value': serializer.data.get('to_latitude'),
            'to_longitude_value': serializer.data.get('to_longitude'),
            'to_country_id_value': '', # country id for reciever
            'from_country_id_value': '', # from courier data side, country id for our store
            'dimensions_length_value': product.dimensions_length,
            'dimensions_weight_value': product.dimensions_weight,
            'dimensions_width_value': '',
            'dimensions_unit_value': '',
            'logistic_type_value': 'REGULAR',
        }
        courier = self.request.data.get('courier')
        product_price = ShipClient(product, courier).get_price(
            **get_price_data_serializer
        )
        return Response({'price': product_price})


class CourierCreateOrder(generics.GenericAPIView):
    """
        API for create shipping order
        i need user info
        product
        shipping info
        ======================
        will create user for user info if not created.
        will create order for that user and product.
        will create shipping order and fire shipping flow
    """
    permission_classes = (IsAuthenticated, )
    queryset = Product.objects.all()
    serializer_class = CourierCreateOrderSerializer

    def post(self, request, *args, **kwargs):
        """
            return courier price for product.
            # create user if not created
            # create new order.
            # create shipping order.
        """
        product = self.get_object()
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        address_info = serializer.data.get('sender_data')
        user = User.objects.filter(mobile=serializer.data.get('recipient_data').get('phone')).last()
        courier = self.request.get('courier')
        shiping_price = 10 # will get it from cache????????????
        if user:
            Order.objects.create(user=user, product=product)
            ShippingOrder.objects.create(
                order=order, user=user, user_address=address_info, start=serializer.data.get('start_shipping'),
                courier=courier, shipping_price=shiping_price, status='new'
            )
        else:
            Order.objects.create(guest_user=guest_user, product=product)
            ShippingOrder.objects.create(
                order=order, guest_user=user_info, guest_user_address=address_info,
                start=serializer.get('start_shipping'), courier=courier, shipping_price=shiping_price,
                status='new'
            )
        create_shipping_order = ShipClient(product, courier).create_order(
            **serializer.data
        )
        return Response({'data': {}})


# tarcking shippment status
class CourierAuthorization(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        """
            return courier auhtorize info.
        """
        courier = self.request.data.get('courier')
        get_authorize_response = ShipClient(product, courier).authorize()
        return Response(get_authorize_response.json())


# tarcking shippment status
class CourierOrderStatus(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Product.objects.all()

    def post(self, request, *args, **kwargs):
        """
            return courier price for product.
        """
        shipping_order = self.get_object()
        courier = self.request.data.get('courier')
        get_order_status = ShipClient(product, courier).get_order_status(
            order_number=""
        )
        return Response({'data': get_order_status.json()})


class CourierCancellOrder(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Product.objects.all()

    def put(self, request, *args, **kwargs):
        """
            return courier price for product.
        """
        shipping_order = self.get_object()
        courier = self.request.data.get('courier')
        get_order_status = ShipClient(product, courier).cancell_order()
        shipping_order.cancelled = 'cancelled'
        shipping_order.save()
        return Response({'cancelled': True})
