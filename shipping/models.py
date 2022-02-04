from django.db import models
from inventory.models import Product
from accounts.models import UserAddress
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import JSONField

User = get_user_model()



def request_and_response_sample():
    # this data will need to poulated from admin
    SetupAllRequests = {
            "authorize":{
                'header': {},
                'data': {},
                'http_method': 'get or post',
                'url': ''
            },
            'authorize_response':{
                'jwt_token': {'id_token': 'token'}
            },
            "get_price":{
                'header': {},
                'body': {},
                'http_method': 'get or post',
                'url': ''
            },
            "create_order":{
                'header': {},
                'body': {},
                'http_method': 'get or post',
                'url': ''
            },
            "order_status":{
                'header': {},
                'body': {},
                'http_method': 'get or post',
                'url': ''
            }
        }
    return SetupAllRequests
    

class Courier(models.Model):
    name = models.CharField(max_length=255)

    request_and_response_sample = JSONField(default=request_and_response_sample)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


    @classmethod
    def is_courier_exists(cls, name):
        """
            name: incoming from ship request
            we should validate make sure this courier is exists
        """
        return cls.objects.filter(name=name).last()


class ShippingOrder(models.Model):
    order = models.ForeignKey('payment.Order', on_delete=models.CASCADE, related_name='shipping_info')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='all_shipping_info')
    user_address = models.ForeignKey(UserAddress, on_delete=models.CASCADE, related_name='all_shipping_info')

    # to store guest user info instead of creating new model
    guest_user = JSONField()
    guest_user_address = JSONField()
    status = models.CharField(choices=(
        ('new', 'new'),
        ('cancelled', 'cancelled'),
        ('done', 'done'),
        ), max_length=11)

    start = models.DateTimeField(default=timezone.now)
    courier = models.ForeignKey(
        Courier, on_delete=models.SET_NULL, null=True, related_name='shipping_order')
    
    shipping_price = models.DecimalField(max_digits=9, decimal_places=2)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
