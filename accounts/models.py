from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Store(models.Model):
    admin = models.OneToOneField(User, on_delete=models.CASCADE, related_name='store')
    name = models.CharField('Store name', max_length=200)
    display_name = models.CharField('Display Name', max_length=255, null=True, blank=True)

    street_address_1 = models.TextField()
    street_address_2 = models.TextField(blank=True, null=True)
    city_name = models.CharField(max_length=255)
    country_name = models.CharField(max_length=255)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    mobile = models.CharField(max_length=255)

    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    middle_name = models.CharField(max_length=255, blank=True, null=True)


class UserAddress(models.Model):
    street_address_1 = models.CharField(max_length=255)
    street_address_2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=255)
    building_number = models.CharField(max_length=255)
    department_number = models.CharField(max_length=255)

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_addresses')

    email = models.EmailField(null=True)
    mobile = models.CharField(max_length=255)
