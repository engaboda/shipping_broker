import logging
import requests
from shipping.exceptions import ResponseException

logger = logging.getLogger(__name__)


class Request():
    def __init__(self, http_method, url, data={}, headers={}, courier_name=""):
        self.http_method = http_method
        self.url = url
        self.data = data
        self.headers = headers
        self.courier_name = courier_name

    def request(self):
        response = requests(self.http_method, self.url, data=self.data, headers=self.headers)
        return response

    def __call__(self, retry_count):
        for step in range(retry_count):
            try:
                response = requests.request(
                    method=self.http_method, url=self.url,
                    data=self.data, headers=self.headers
                )
            except requests.exceptions.ConnectionError as e:
                logger.error(f'<{self.courier_name} ConnectionError> {e}')
            except requests.exceptions.ConnectTimeout as e:
                logger.error(f'<{self.courier_name} ConnectTimeout> {e}')
            except Exception as e:
                logger.error(f'<{self.courier_name} Exception> {e}')
            else:
                if response.status_code == 200:
                    return response
                logger.info(f'<{self.courier_name}> response: {response.json()} status={response.status_code}')
                raise ResponseException({
                    {f'{self.courier_name}': response.json()},
                    code=response.status_code
                )
