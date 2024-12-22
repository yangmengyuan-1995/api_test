"""
@Date  :  2024/12/12 19:15
@File  :  model_util.py
@Author:  杨梦远
@Desc  :  对测试用例yaml文件的格式进行校验
"""
from dataclasses import dataclass, field
from typing import Dict, Any
# from typing import Literal

import logging

logger = logging.getLogger(__name__)


@dataclass
class ParametrizeInfo:
    """
    yaml文件中parametrize的基础格式
    """
    param_key: str
    # 在python3.8及以后的版本中可以使用Literal来对值进行校验
    # param_key = Literal['params', 'data', 'json']
    titles: str
    validates: dict
    params: dict
    quantity: int = 0

    # 自定义校验
    def __post_init__(self):
        # 校验param_key的值
        if self.param_key not in ['params', 'data', 'json']:
            raise ValueError(f'parametrize中param_key的值只能是[params, data, json]中的一个!')


@dataclass
class RequestInfo:
    """
    yaml文件中request的基础格式
    """
    method: str
    url: str
    params: dict = None
    data: dict = None
    json: dict = None
    headers: dict = None
    cookies: dict = None
    files: dict = None
    auth: dict = None
    timeout: dict = None
    proxies: dict = None
    hooks: dict = None
    stream: dict = None
    verify: dict = None
    cert: dict = None
    allow_redirects: bool = True

    def update_attr(self, attr_name, updates):
        if hasattr(self, attr_name):
            attr = getattr(self, attr_name)
            if isinstance(attr, dict) and isinstance(updates, dict):
                attr.update(updates)
            else:
                raise AttributeError(f"属性 '{attr_name}' 不是字典或传入的更新不是字典")
        else:
            raise AttributeError(f"属性 '{attr_name}' 不存在")

    def delete_attr(self, attr_name, var_name):
        if hasattr(self, attr_name):
            attr = getattr(self, attr_name)
            if isinstance(attr, dict):
                attr.pop(var_name)
            else:
                raise AttributeError(f"属性 '{attr_name}' 不是字典或传入的更新不是字典")
        else:
            raise AttributeError(f"属性 '{attr_name}' 不存在")


@dataclass
class CaseInfo:
    """
    yaml文件的基础格式
    """
    # 必填
    feature: str
    story: str
    title: str
    request: RequestInfo
    # 选填
    validate: dict = None
    # env关键字用于标识是否需要从响应中获取数据设置为环境变量
    env: dict = None
    parametrize: ParametrizeInfo = None

    # 自定义校验
    def __post_init__(self):
        # 校验param_key的值
        if not self.parametrize and not self.validate:
            raise ValueError(f'用例中必须包含parametrize或validate')


class VerifyYaml:
    def __init__(self, yaml_path, idx):
        self._yaml_path = str(yaml_path)
        self._file_no = idx + 1

    def verify_case(self, case_info: dict):
        try:
            request = RequestInfo(**case_info.get('request'))
            # 将数据转换为RequestInfo实例对象, 方便后续调用方法替换变量
            case_info['request'] = request
        except TypeError as e:
            logger.error(f'{self._yaml_path} 文件中的第{self._file_no}个测试用例中的request不符合框架的规范: {e}')
            raise Exception(f'{self._yaml_path} 文件中的第{self._file_no}个测试用例中的request不符合框架的规范!')
        try:
            return CaseInfo(**case_info)
        except Exception as e:
            logger.error(f'{self._yaml_path} 文件中的测试用例不符合框架的规范! {e}')
            raise Exception(f'{self._yaml_path} 文件中的测试用例不符合框架的规范!')

    def verify_parametrize(self, parametrize: dict):
        try:
            return ParametrizeInfo(**parametrize)
        except Exception as e:
            logger.error(f'{self._yaml_path} 文件中的第{self._file_no}个测试用例中的parametrize不符合框架的规范: {e}')
            raise Exception(f'{self._yaml_path} 文件中的第{self._file_no}个测试用例中的parametrize不符合框架的规范!')
