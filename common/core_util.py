"""
@Date  :  2024/12/18 5:39
@File  :  core_util.py
@Author:  杨梦远
"""
import copy

from common.model_util import CaseInfo
from common.request_util import RequestUtil
from common.env_util import EnvVarUtil
from common.assert_util import AssertUtil
# from setting import COMMON_PARAMS

import logging

logger = logging.getLogger(__name__)
eu = EnvVarUtil()
# ru = RequestUtil(COMMON_PARAMS)
ru = RequestUtil()
au = AssertUtil()


def stand_case_flow(case_obj: CaseInfo):
    # 请求参数写入日志
    logger.info(f'模块:{str(case_obj.feature)} > 接口: {str(case_obj.story)} > 用例名: {str(case_obj.title)}')
    # 发送请求
    res = ru.send_request(eu.use_env_var(case_obj.request))
    # 转换响应内容, 方便后续使用
    new_res = get_stand_res(res)
    # yaml文件中设置了env则需要去响应中提取变量
    if case_obj.env:
        for k, v in case_obj.env.items():
            eu.set_env_var(new_res, k, *v)
    # yaml文件中设置了validate则需要去响应中进行校验

    if case_obj.validate:
        for k, v in case_obj.validate.items():
            au.assert_case(new_res, k, v)
    else:
        logger.warning("此用例没有断言 \n")


def get_stand_res(res):
    new_res = copy.deepcopy(res)
    # 将json()改为json属性
    try:
        new_res.json = new_res.json()
    except Exception:
        new_res.json = {'msg': 'response not json'}
    return new_res
