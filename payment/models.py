from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import JSONField


User = get_user_model()

class Order(models.Model):
    product = models.ForeignKey('inventory.Product', on_delete=models.CASCADE, related_name='order')

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)

    # for guest user info
    guest_user = JSONField()

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
