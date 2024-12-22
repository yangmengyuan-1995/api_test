"""
@Date  :  2024/12/18 21:11
@File  :  ddt_util.py
@Author:  杨梦远
"""
import copy

import yaml

from common.model_util import CaseInfo, VerifyYaml
from setting import PARAMETRIZE


def read_testcase(yaml_path):
    with open(yaml_path, encoding='utf-8') as f:
        case_list = yaml.safe_load(f)
        new_case_list = []
        for idx, case_obj in enumerate(case_list):
            verifier = VerifyYaml(yaml_path, idx)
            case_info = verifier.verify_case(case_obj)
            if case_info.parametrize:
                new_case_list += format_ddt(case_info, verifier)
            else:
                new_case_list.append(case_info)
        return new_case_list


def format_ddt(case_info: CaseInfo, verifier):
    """
    根据parametrize中的数据生成对应的测试用例
    期望的数据驱动的格式:
    "parametrize": {
        "quantity": 3,                           指明用例数量(未指明时会去获取第一个变量(本例中的username)的值列表的长度)
        "params_key": "params",                  指明去request.params中寻找变量进行替换
        "titles":  ["正例", "反例1", "反例2"]
        "validates": [
            "contain": {"返回文本包含success"： ["success", "text"]}
            "contain": {"返回文本包含failed"： ["failed", "text"]}
            "contain": {"返回文本包含failed"： ["failed", "text"]}
        ]
        "params":
            "username": ["Tom", "Bob", null]         变量名: 值列表
            "password": ["admin", null, "admin"]     变量名: 值列表
    }
    """
    # 获取parametrize对象
    parametrize = verifier.verify_parametrize(case_info.parametrize)
    # 获取数据驱动条数
    case_len = len(list(parametrize.params.values())[0]) if parametrize.params.values() else 0
    ddt_quantity = parametrize.quantity or case_len

    case_info_list = []
    for idx in range(ddt_quantity):
        new_case_info = copy.deepcopy(case_info)
        # 将数据填入request对应的参数中
        for param_name, value_list in parametrize.params.items():
            value = value_list[idx]
            if not value:  # 参数的值为None时, 说明该条用例不希望携带本参数
                new_case_info.request.delete_attr(parametrize.param_key, param_name)
                continue
            if isinstance(value, str) and value.isdigit():  # 字符串格式的数字特殊处理
                value = "'" + value + "'"
            new_case_info.request.update_attr(parametrize.param_key, {param_name: value})
        # 添加标题和断言
        new_case_info.title = parametrize.titles[idx]
        new_case_info.validate = parametrize.validates[idx]
        # 丢弃parametrize
        delattr(new_case_info, PARAMETRIZE)
        case_info_list.append(new_case_info)
    return case_info_list
