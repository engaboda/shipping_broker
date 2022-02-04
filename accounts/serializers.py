from .models import GuestUser, GuestUserAddress, Profile
from django.contrib.auth import get_user_model

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        exclude = ('user', )


class UserSerializer(serializers.Serializer):
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = ('id', 'email', 'date_joined', 'profile')


class GuestUserSerializer(serializers.ModelSerializer):
    mobile = serializers.CharField(max_length=255)


class GuestUserAddressSerializer(serializers.ModelSerializer):
    street_address_1 = serializers.CharField(max_length=255)
    street_address_2 = serializers.CharField(max_length=255)
    city = serializers.CharField(max_length=255)
    zip_code = serializers.CharField(max_length=255)
    building_number = serializers.CharField(max_length=255)
    department_number = serializers.CharField(max_length=255)
