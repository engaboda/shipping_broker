from rest_framework import serializers


class CourierListSerializer(serializers.Serializer):
    name = serializers.CharField()


class PackagePriceSerializer(serializers.Serializer):
    to_latitude = serializers.CharField()
    to_longitude = serializers.CharField()
    # country_id = serializers.CharField()
    # logistic_type = serializers.CharField()


class CourierPartyDataSerializer(serializers.Serializer):
    """
        sender and recepient data.
    """
    address_type = serializers.CharField()
    name = serializers.CharField()
    apartment = serializers.CharField()
    app = serializers.EmailField()
    building = serializers.CharField()
    street = serializers.CharField()
    city = serializers.CharField()
    country = serializers.CharField()
    phone = serializers.CharField()


class CourierDimensionsSerializer(serializers.Serializer):
    weight = serializers.CharField()
    width = serializers.CharField()
    length = serializers.CharField()
    height = serializers.CharField()
    unit = serializers.CharField()
    domestic = serializers.CharField()


class PackageTypeSerializer(serializers.Serializer):
    courier_type = serializers.CharField()


class ChargeItemsSerializer(serializers.Serializer):
    paid = serializers.BooleanField()
    charge = serializers.DecimalField(max_digits=9, decimal_places=2)
    charge_type = serializers.CharField()


class CourierCreateOrderSerializer(serializers.Serializer):
    sender_data = CourierPartyDataSerializer() # should be setted from here not from user
    recipient_data = CourierPartyDataSerializer(),
    dimensions = CourierDimensionsSerializer
    package_type = PackageTypeSerializer
    charge_items = ChargeItemsSerializer()
    recipient_not_available = serializers.CharField()
    payment_type  = serializers.CharField()
    payer = serializers.CharField()
    parcel_value = serializers.DecimalField(max_digits=9, decimal_places=2)
    fragile = serializers.BooleanField()
    note = serializers.CharField()
    piece_count = serializers.CharField()
    force_create = serializers.CharField()
    courier = serializers.CharField()
    start_shipping = serializers.DateTimeField()
