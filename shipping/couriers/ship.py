import json
import logging
from inventory.models import Product
from shipping.models import Courier
from .custom_request import Request
from shipping.exceptions import (
    CourierNotFoundException, CourierConnectionTimeOutException, CourierConnectionException,
    CourierMissConfgurationException
)
from zidship.settings import env
from django.core.cache import cache


logger = logging.getLogger(__name__)


class ShipClient:
    """
        one place for all shipping action.
        =================
        work flow
        you will provide me some argument and i will search for that arguments and replace it with its value.
    """

    def __init__(
            self, *args,
            courier_name: str = "",
            product: Product = None
        ):
        # for log and pick right info from our couriers on the fly table
        self.courier_name = courier_name
        self.courier = Courier.objects.filter(name=self.courier_name).last()
        self.raise_courier_not_found(not self.courier)

        # to calculate price before ship
        self.product = product

    def raise_courier_not_found(self, raise_exception: bool):
        if raise_exception: raise CourierNotFoundException
        return True

    def build_request_dict(self, request: dict):
        """
            we save dict in courier model like this
            {'weight': 'field_name_in_product_model'}
            we should change this to
            {'weight': 'real value from product model'}
        """
        dict_hold_request_value = {}
        for key, value in request.items():
            dict_hold_request_value[key] = getattr(self.courier, value)
        return dict_hold_request_value

    def authorize(self):
        """
            authorize one required courier
            and return response identified in courier model
        """
        authorize_data = self.courier.request_and_response_sample.get('authorize', None)

        authorization_url = authorize_data.get('url')
        authorization_http_method = authorize_data.get('http_method')
        authorization_headers = authorize_data.get('headers')
        authorization_json_data = authorize_data.get('data')

        # "it should be get from most secure place in the plant"
        authorization_data_from_env = {}
        for key, value in authorization_json_data.items():
            try:
                value_for_authorization_key = env.str(value)
            except Exception:
                raise CourierMissConfgurationException
            authorization_data_from_env[key] = value_for_authorization_key

        authorization_json_data_merge_with_env_data = {
            **authorization_json_data, **authorization_data_from_env}

        request_object = Request(
            authorization_http_method, authorization_url,
            json.dumps(authorization_json_data_merge_with_env_data),
            authorization_headers, self.courier_name
        )
        response = request_object(retry_count=5)
        # we should cache response for n hours
        cache_period = authorize_data.get('cache_period', 0)
        cache_keys = authorize_data.get('cache_fields', '') # in mintus
        return response

    def get_price(self, **kwargs):
        price_data = self.courier.request_and_response_sample.get('get_price', None)

        price_url = price_data.get('url')
        price_http_method = price_data.get('http_method')
        price_headers = price_data.get('headers')
        price_json_data = price_data.get('data', {})
        query_params = price_data.get('url_params')

        for key, value in kwargs.items():
            if query_params.find(key) != -1:
                query_params = query_params.replace(key, f'{value}')
            if price_headers.get(key):
                price_headers[key] = value
            if price_json_data.get(key):
                price_json_data[key] = value
            if price_url.find(key):
                price_url.replace(key, value)
        price_url += query_params

        logger.info(
            f'''<{self.courier_name}> get country request info url={price_url} data={price_json_data}'''
        )
        request_object = Request(
            http_method=price_http_method, url=price_url, data=price_json_data, headers=price_headers
        )
        response = request_object(retry_count=5)
        return response

    def get_country(self, **kwargs):
        """
            i will take these arugment and search in headers if they called in it
        """
        get_country_data = self.courier.request_and_response_sample.get('get_country', None)

        get_country_url = get_country_data.get('url')
        get_country_http_method = get_country_data.get('http_method')
        get_country_headers = get_country_data.get('headers')
        get_country_json_data = get_country_data.get('data', {})
        query_params = get_country_data.get('url_params')

        for key, value in kwargs.items():
            if query_params.find(key) != -1:
                query_params = query_params.replace(key, value)
            if get_country_headers.get(key):
                get_country_headers[key] = value
            if get_country_json_data.get(key):
                get_country_json_data[key] = value
            if get_country_url.find(key):
                get_country_url.replace(key, value)
        get_country_url += query_params

        # "it should be get from most secure place in the plant"
        logger.info(
            f'''<{self.courier_name}> get country request info url={get_country_url} data={get_country_json_data}'''
        )
        request_object = Request(
            http_method=get_country_http_method, url=get_country_url,
            headers=get_country_headers, courier_name=self.courier_name
        )
        response = request_object(retry_count=5)
        return response

    def get_city(self, **kwargs):
        """
            i will take these arugment and search in headers if they called in it
        """
        get_city_data = self.courier.request_and_response_sample.get('get_city', None)

        get_city_url = get_city_data.get('url')
        get_city_http_method = get_city_data.get('http_method')
        get_city_headers = get_city_data.get('headers')
        get_city_json_data = get_city_data.get('data', {})
        query_params = get_city_data.get('url_params')

        for key, value in kwargs.items():
            if query_params.find(key) != -1:
                query_params = query_params.replace(key, value)
            if get_city_headers.get(key):
                get_city_headers[key] = value
            if get_city_json_data.get(key):
                get_city_json_data[key] = value
            if get_city_url.find(key):
                get_city_url.replace(key, value)
        get_city_url += query_params

        # "it should be get from most secure place in the plant"
        logger.info(
            f'''<{self.courier_name}> get city request info url={get_city_url} data={get_city_json_data}'''
        )

        request_object = Request(
            http_method=get_city_http_method, url=get_city_url,
            headers=get_city_headers, courier_name=self.courier_name
        )
        response = request_object(retry_count=5)
        return response

    def create_order(self, **kwargs):
        get_create_order_data = self.courier.request_and_response_sample.get('create_order', None)

        get_create_order_url = get_create_order_data.get('url')
        get_create_order_http_method = get_create_order_data.get('http_method')
        get_create_order_headers = get_create_order_data.get('headers')
        get_create_order_json_data = get_create_order_data.get('data', {})
        query_params = get_create_order_data.get('url_params')

        for key, value in kwargs.items():
            if query_params.find(key) != -1:
                query_params = query_params.replace(key, value)
            if get_create_order_headers.get(key):
                get_create_order_headers[key] = value
            if get_create_order_json_data.get(key):
                get_create_order_json_data[key] = value
            if get_create_order_url.find(key):
                get_create_order_url.replace(key, value)
        get_city_url += query_params

        # "it should be get from most secure place in the plant"
        logger.info(
            f'''<{self.courier_name}> get country request info url={get_create_order_url} data={get_create_order_json_data}'''
        )
        request_object = Request(
            http_method=get_create_order_http_method, url=get_create_order_url,
            headers=get_create_order_headers, courier_name=self.courier_name
        )
        response = request_object(retry_count=5)
        return response

    def get_order_status(self, **kwars):
        order_status_data = self.courier.request_and_response_sample.get('order_status', None)

        order_status_url = order_status_data.get('url')
        order_status_http_method = order_status_data.get('http_method')
        order_status_headers = order_status_data.get('headers')
        order_status_json_data = order_status_data.get('data')
        order_status_query_params = order_status_data.get('url_params')

        for key, value in kwargs.items():
            if order_status_query_params.find(key) != -1:
                order_status_query_params = order_status_query_params.replace(key, value)
            if order_status_headers.get(key):
                order_status_headers[key] = value
            if order_status_json_data.get(key):
                order_status_json_data[key] = value
            if order_status_url.find(key):
                order_status_url.replace(key, value)
        order_status_url += order_status_query_params

        logger.info(
            f'''<{self.courier_name}> get country request info url={order_status_url} data={order_status_json_data}'''
        )
        request_object = Request(
            order_status_http_method, order_status_url,
            data=order_status_json_data, headers=order_status_headers
        )
        response = request_object(retry_count=5)
        return response

    def cancell_order(self, **kwargs):
        cancell_order_data = self.courier.request_and_response_sample.get('cancell_order', None)

        cancell_order_url = cancell_order_data.get('url')
        cancell_order_http_method = cancell_order_data.get('http_method')
        cancell_order_headers = cancell_order_data.get('headers')
        cancell_order_json_data = cancell_order_data.get('data')
        cancell_order_query_params = cancell_order_data.get('url_params')

        for key, value in kwargs.items():
            if query_params.find(key) != -1:
                cancell_order_query_params = cancell_order_query_params.replace(key, value)
            if cancell_order_headers.get(key):
                cancell_order_headers[key] = value
            if cancell_order_json_data.get(key):
                cancell_order_json_data[key] = value
            if cancell_order_url.find(key):
                cancell_order_url.replace(key, value)
        order_status_url += cancell_order_query_params

        logger.info(
            f'''<{self.courier_name}> get country request info url={cancell_order_url} data={cancell_order_json_data}'''
        )
        request_object = Request(
            cancell_order_http_method, cancell_order_url,
            data=cancell_order_json_data, headers=cancell_order_headers
        )
        response = request_object(retry_count=5)
        return response
