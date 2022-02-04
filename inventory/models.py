from django.db import models


class StoreHouse(models.Model):
    store = models.ForeignKey('accounts.Store', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)

    latitude = models.CharField(max_length=200, null=True, blank=True)
    longitude = models.CharField(max_length=200, null=True, blank=True)

    tag = models.CharField(max_length=200, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Product(models.Model):
    """Product Creation Class."""

    storehouse = models.ForeignKey(StoreHouse, on_delete=models.CASCADE, related_name='in_products')
    barcode = models.CharField(max_length=200, null=True, blank=True)
    product_code = models.CharField(max_length=100, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    unit_price = models.DecimalField(
        max_digits=9, decimal_places=2, blank=True, null=True,
    )

    # shipping info
    weight = models.FloatField(null = True, blank = True)
    dimensions_length = models.CharField(max_length=255, null=True, blank=True)
    dimensions_weight = models.CharField(max_length=255, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
