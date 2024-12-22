"""
@Date  :  2024/12/18 6:12
@File  :  setting.py.py
@Author:  杨梦远
"""

# 数据库配置
from pathlib import Path

DB_CONF = {
    'user': '',
    'password': '',
    'host': '',
    'database': '',
    'port': '',
}


# 断言常量
EQUALS = 'equals'
CONTAINS = 'contains'
DB_EQUALS = 'db_equals'
DB_CONTAINS = 'db_contains'

# DDT驱动关键字
PARAMETRIZE = 'parametrize'

# 项目根路径
BASE_DIR = Path(__file__).resolve().parent
# 保存环境变量的文件地址
ENV_FILE = 'env.yaml'
# Allure报告的项目名
ALLURE_PROJECT_NAME = '接口自动化测试报告'
# 项目公共参数
# COMMON_PARAMS = {
#     'application': 'app',
#     'application_client_type': 'h5'
# }

