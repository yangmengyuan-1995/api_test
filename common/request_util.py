"""
@Date  :  2024/12/12 18:56
@File  :  request_util.py
@Author:  杨梦远
"""
import requests
import logging

from common.model_util import RequestInfo

logger = logging.getLogger(__name__)


class RequestUtil:

    def __init__(self, common_params=None):
        self._sess = requests.session()
        self._common_params = common_params or {}

    def send_request(self, request: dict):
        request = RequestInfo(**request)
        if request.params and self._common_params:
            request.params.update(self._common_params)
        if request.files:
            for file_k, file_v in request.files:
                try:
                    request.files[file_k] = open(file_v, 'rb')
                except FileNotFoundError:
                    logger.error(f'文件路径有错')

        new_request = {}
        for key, value in request.__dict__.items():
            if value:
                new_request.update({key: value})
                logger.info(f'请求 {key} 参数: {value}')

        res = self._sess.request(**new_request)
        if 'json' in res.headers.get('Content-Type'):
            logger.info(f'响应内容: {res.json()}')
        else:
            logger.info(f'响应内容: {res.text}')
        return res
