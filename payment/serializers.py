from .models import Order
from rest_framework import serializers
from accounts.serializers import GuestUserSerializer, GuestUserAddressSerializer


class OrderCreateSerializer(serializers.Serializer):
    user_info = GuestUserSerializer()
    address_info = GuestUserAddressSerializer()
    product = serializers.IntegerField()
    start_shipping = serializers.DateTimeField()
    courier = serializers.CharField()
