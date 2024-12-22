"""
@Date  :  2024/12/12 19:20
@File  :  test_generate_case.py
@Author:  杨梦远
"""
from pathlib import Path

import allure
import pytest
import logging

from common.core_util import stand_case_flow
from common.ddt_util import read_testcase
from setting import ALLURE_PROJECT_NAME


@allure.epic(ALLURE_PROJECT_NAME)
class TestGenerateCase:
    pass


def generate_case(file_path):
    @pytest.mark.parametrize('case_obj', read_testcase(file_path))
    def func(self, case_obj):
        logger.info(f'yaml文件: {file_path}')
        stand_case_flow(case_obj)
        # 定制Allure报告
        allure.dynamic.feature(case_obj.feature)
        allure.dynamic.story(case_obj.story)
        allure.dynamic.title(case_obj.title)
    return func


logger = logging.getLogger(__name__)
# 获取testcase的路径
testcase_path = Path(__file__).parent
# 获取所有的yaml文件
yaml_path_list = testcase_path.glob('**/*.yaml')
# 根据yaml文件生成测试用例方法添加到TestGenerateCase类里
for yaml_path in yaml_path_list:
    case_name = yaml_path.stem
    if not case_name.startswith('test_'):
        case_name = 'test_' + case_name
    setattr(TestGenerateCase, case_name, generate_case(yaml_path))
