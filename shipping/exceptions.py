from rest_framework.exceptions import APIException


class CourierNotFoundException(APIException):
    status_code = 404
    default_detail = ("Courier not Suppert.")
    default_code = 'courier_not_found'


class CourierConnectionException(APIException):
    status_code = 404
    default_detail = ("Courier Connection Error.")
    default_code = 'courier_failed_to_connection'


class CourierConnectionTimeOutException(APIException):
    status_code = 404
    default_detail = ("Courier Connection timeout.")
    default_code = 'courier_time_out_connection'


class CourierMissConfgurationException(APIException):
    status_code = 400
    default_detail = ("Courier Miss Configuration Error.")
    default_code = 'courier_miss_configuration'


class BaseAPIException(APIException):
    def __init__(self, detail=None, code=None):
        self.status_code = code
        super().__init__(detail, code)


class ResponseException(BaseAPIException):
    pass
