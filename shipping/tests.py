from rest_framework.tests import APITestCase
from shiping.models import Courier
from django.urls.base import reverse

class CourierPriceAPITestCase(APITestCase):
    def setUp(self):
        request_and_response_sample = {
            "authorize": {
                "url": "https://prodapi.shipox.com/api/v1/customer/authenticate",
                "data": {
                    "password": "shipox_password",
                    "username": "shipox_username",
                    "remember_me": "remember_me"
                },
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                },
                "http_method": "post"
            },
            "get_price": {
                "url": "https://prodapi.shipox.com/api/v2/customer/packages/prices/starting_from?",
                "url_params": "from_latitude=from_latitude_value&from_longitude=from_longitude_value&to_latitude=to_latitude_value&to_longitude=to_longitude_value&to_country_id=to_country_id_value&from_country_id=from_country_id_value&dimensions_length=dimensions_length_value&dimensions_weight=dimensions_weight_value&dimensions_width=dimensions_width_value&dimensions_unit=dimensions_unit_value&logistic_type=logistic_type_value",
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": "Bearer jwt_token"
                },
                "http_method": "get"
            },
            "get_country":{
                "url": "https://prodapi.shipox.com/api/v2/customer/countries?",
                "url_params": "search=country_name",
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": "Bearer jwt_token"
                },
                "http_method": "get"
            },
            "get_city":{
                "url": "https://prodapi.shipox.com/api/v2/customer/cities?",
                "url_params": "country_id=country_id_value,search=search_value",
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": "Bearer jwt_token"
                },
                "http_method": "get"
            },
            "create_order": {
                "url": "https://prodapi.shipox.com/api/v3/customer/order",
                "data": {
                    "sender_data": {
                        "address_type": "residential",
                        "name": "Sherlock Holmes",
                        "email": "mr.holmes@example.com",
                        "apartment": "221",
                        "building": "B",
                        "street": "Baker Street",
                        "city": {
                        "code": "dubai"
                        },
                        "country": {
                        "id": 229
                        },
                        "neighborhood": {
                            "id":24876469,
                            "name":"Al Quoz 1"
                        },
                        "phone": "+971541234567"
                    },
                    "recipient_data": {
                        "address_type": "residential",
                        "name": "Dr. Watson",
                        "apartment": "221",
                        "building": "B",
                        "street": "Baker Street",
                        "city": {
                        "id": 4
                        },
                        "neighborhood": {
                            "id":24876469,
                            "name":"Al Quoz 1"
                        },
                        "phone": "+971543097580",
                        "landmark": "Opposite to the Union Bus Station"
                    },
                    "dimensions": {
                        "weight": 12,
                        "width": 32,
                        "length": 45,
                        "height": 1,
                        "unit": "METRIC",
                        "domestic": true
                    },
                    "package_type": {
                        "courier_type": "express_delivery"
                    },
                    "charge_items": [
                        {
                        "paid": false,
                        "charge": 100,
                        "charge_type": "cod"
                        }
                    ],
                    "recipient_not_available": "do_not_deliver",
                    "payment_type": "cash",
                    "payer": "sender",
                    "parcel_value": 100,
                    "fragile": true,
                    "note": "mobile phone",
                    "piece_count": 1,
                    "force_create": true
                },
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": "Bearer jwt_token"
                },
                "http_method": "post"
            },
            "order_status": {
                "url": "https://prodapi.shipox.com/api/v1/customer/order/order_number/history_items",
                "data": {},
                "headers": {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": "Bearer jwt_token"
                },
                "http_method": "get"
            },
            "cancell_order": {
                "data": {},
                "url": "https://prodapi.shipox.com/api/v1/customer/order/order_id_value/status?",
                "url_params": "status=status_value",
                "headers": {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": "Bearer id_toke"
                },
                "http_method": "put"
            }
        }

        self.courier = Courier.objects.create(
            name='Shipox', 
            request_and_response_sample=request_and_response_sample
        )

        self.admin = User.objects.create(email='mock_20@yahoo.com')
        self.admin.set_password('1234')
        self.store = Store.objects.create(
            admin=self.user, name='wowo', street_address_1='10', street_address_2='210' 
        )
        self.storehouse = StoreHouse.objects.create(
            store=self.store, name='cairo', latitude=2.2664, longitude=2.2664
        )
        self.product = Product.objects.create()
        self.courier_price_url = reverse('courier_price', args=(self.product.pk,))

    # we should mock this test
    def test_price(self):
        self.client.force_login(self.admin)
        data = {
            'to_latitude': '2.2',
            'to_longitude': '2.1810'
        }
        self.client.post(self.courier_price_url, )