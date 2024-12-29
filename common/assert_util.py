"""
@Date  :  2024/12/18 6:00
@File  :  assert_util.py
@Author:  杨梦远
"""
import logging
import traceback
from collections import namedtuple
from common.db_util import DBUtil
from setting import EQUALS, CONTAINS, DB_EQUALS, DB_CONTAINS

db = DBUtil()
logger = logging.getLogger(__name__)


class AssertUtil:

    @staticmethod
    def assert_case(res, assert_type, value: dict):
        if assert_type not in [EQUALS, CONTAINS, DB_EQUALS, DB_CONTAINS]:
            logger.error(f'目前不支持 "{assert_type}" 类型的断言, 请修改后重试')
            raise Exception(f'目前不支持 "{assert_type}" 类型的断言, 请修改后重试')
        AssertTuple = namedtuple('AssertTuple', ['expect', 'actually'])
        validate = True
        for msg, expr in value.items():
            try:
                expr = AssertTuple(*[str(v) for v in expr])
                # 从响应中获取实际值
                actually_value = getattr(res, expr.actually)
                # 进行断言判断(python3.10及以上版本可以使用match case)
                if assert_type == EQUALS:
                    assert expr.expect == actually_value, msg
                if assert_type == CONTAINS:
                    assert expr.expect in actually_value, msg
                if assert_type == DB_EQUALS:
                    value = db.get_one(expr.expect)
                    assert value == actually_value, msg
                if assert_type == DB_CONTAINS:
                    value = db.get_one(expr.expect)
                    assert value in actually_value, msg
            except AssertionError:
                logger.error(f"{msg}断言失败: {str(traceback.format_exc())}")
                validate = False
        if validate:
            logger.info('断言成功 \n')


