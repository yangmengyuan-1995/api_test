"""
@Date  :  2024/12/10 20:17
@File  :  run.py
@Author:  杨梦远
"""
import pytest
import os
import shutil
import time

from common.yaml_util import clean_env_yaml

if __name__ == '__main__':
    # 清除环境变量文件
    clean_env_yaml()
    # 执行测试
    pytest.main()
    # 执行之后将日志文件加上时间戳重命名, 防止下次执行被覆盖
    # shutil.move("logs/frame.log", f"logs/frame_{str(int(time.time()))}.log")
    # 生成allure报告
    # time.sleep(3)
    # os.system("allure generate ./temps -o ./reports --clean")
