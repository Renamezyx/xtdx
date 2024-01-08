import time

from requests import sessions, Response
import config
from logger_base import logger


def log_request_response(func):
    def wrapper(self, method, url, **kwargs):
        response = func(self, method, url, **kwargs)

        logger.info(f"req: {method.upper()} {url}")
        if response.status_code == 200:
            logger.info(f" - success, code: {response.status_code}")
            logger.info(f"res: {response.text}")
        else:
            logger.error(f" - fail, code: {response.status_code}")
        return response

    return wrapper


class RequestBase(object):
    def __init__(self):
        self.session = sessions.Session()
        self.debug = config.DEBUG
        self.proxies = {
            'http': 'http://127.0.0.1:8002',
            'https': 'http://127.0.0.1:8002',
        }

    @log_request_response
    def request(self, method: str, url: str, **kwargs) -> Response:
        time.sleep(1)  # 降低频率 防止检测 服务崩溃
        if self.debug:
            res: Response = self.session.request(method=method, url=url, verify=False, proxies=self.proxies, **kwargs)
        else:
            res: Response = self.session.request(method=method, url=url)
        return res


request = RequestBase().request
