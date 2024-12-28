"""
@Date  :  2024/12/12 22:14
@File  :  env_util.py
@Author:  杨梦远
"""
import re
from collections import namedtuple

import jsonpath
import yaml

from common.func_collect import FuncCollectUtil
from common.model_util import RequestInfo
from common.yaml_util import write_env_yaml


class EnvVarUtil:

    @staticmethod
    def set_env_var(res, var_name, attr_name, expr, index):
        # 通过反射获取属性的值
        data = getattr(res, attr_name)
        if expr.startswith('$'):
            lis = jsonpath.jsonpath(data, expr)
        else:
            lis = re.findall(expr, data)
        if lis:
            write_env_yaml({var_name: lis[index]})

    def use_env_var(self, request_data: RequestInfo):
        request_data_dic = request_data.__dict__
        # 将字典转为字符串
        data_str = yaml.safe_dump(request_data_dic)
        # 使用模版替换
        new_request_data = self.hot_load_replace(data_str)
        # 将替换后的字符串转为字典返回
        return yaml.safe_load(new_request_data)

    @staticmethod
    def hot_load_replace(data_str: str):
        """
        支持yaml文件中配置函数
        :param data_str:
        :return:
        """
        # 读取 ${func()} 类型的表达式
        func_regexp = "\\$\\{(.*?)\\((.*?)\\)\\}"
        func_list = re.findall(func_regexp, data_str)
        FuncTuple = namedtuple('FuncTuple', ['name', 'args'])
        for func in func_list:
            func = FuncTuple(*func)
            try:
                if func.args == '':
                    new_value = getattr(FuncCollectUtil(), func.name)()
                else:
                    try:
                        new_value = getattr(FuncCollectUtil(), func.name)(*func.args.split(','))
                    except TypeError:
                        raise Exception(f'yaml中 {func.name}({func.args}) 参数数量不正确, 请检查重试')
            except AttributeError:
                raise Exception(f'不支持的函数"{func.name}", 请检查函数名称是否正确!')
            # 字符串格式的数字
            if isinstance(new_value, str) and new_value.isdigit():
                new_value = "'" + new_value + "'"
            old_value = "${" + func.name + "(" + func.args + ")}"
            data_str = data_str.replace(old_value, str(new_value))
        return data_str
