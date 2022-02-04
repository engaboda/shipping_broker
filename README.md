# shipping_broker
adding shipment with now code.

# shipping example
* you should login to courier platform and get access info details
* identify your workflow like [i want get price for shipping, and i want to create shipping order]
* after that you should set for each request like

in this exmpale i loggedin to shipox and i create general flow like
`authorize to get jwt token needed for every reqyest`
`get city to show what city we will ship to or from`
`get country to show what city we will ship to or from`
`get get price to show what what will he pay for shipping only`
`create order`

===================
so we should set url for every request
and data for every request
and headers
and more info like if he need cache and cache period

====================
# example
```
 {
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
        "http_method": "post",
        "cache_period": "24", 
        "cache_fields": ["id_token"]
    }
```
here in the above example he set url for courier.
in data i will take value for every key and change it with value coming from env variable.
and if there is data in string i will search for any valeu to replace like `https://prodapi.shipox.com/api/v1/customer/authenticate` so if user set arguement
to authorize method like authorize(authenticate="jwt") i will change authenticate with kwt in string url

so this `https://prodapi.shipox.com/api/v1/customer/authenticate`  will change to `https://prodapi.shipox.com/api/v1/customer/jwt`
 another example ```
  {
            "password": "shipox_password",
            "username": "shipox_username",
            "remember_me": "remember_me"
  }
   ```
 i will see if ther is argument with value 'password' and if found will change its value with argument value
 like 
 `def get_country_id(country_name='cairo')
 i will search for word country_name in url, headers, data, query_params and if found it will change its value to cairo
 
 

```{
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
        "http_method": "post",
        "cache_period": "24", 
        "cache_fields": ["id_token"]
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
    },
    "workflow": {
        "authorize":""
    }
}```







======================================
and if you need authorize you will hit this url `courier/authorize/` to get authorize response from courier.

and if you need shipping price for product x you will hit this url `courier/x/price` to get price response from courier platform.

and if you need creating shipping for product x you will hit this url `courier/x/create_order` to get ship order and get response from courier platform.

## and more
