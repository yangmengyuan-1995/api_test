"""
@Date  :  2024/12/12 19:02
@File  :  yaml_util.py
@Author:  杨梦远
"""
import os
import yaml

from setting import BASE_DIR, ENV_FILE


def read_env_yaml():
    """获取所有环境变量"""
    with open(os.path.join(BASE_DIR, ENV_FILE), encoding='utf-8') as f:
        return yaml.safe_load(f)


def write_env_yaml(data):
    """写入环境变量"""
    with open(os.path.join(BASE_DIR, ENV_FILE), encoding='utf-8', mode='a+') as f:
        yaml.safe_dump(data, f, allow_unicode=True)


def clean_env_yaml():
    """清空环境变量yaml文件"""
    with open(os.path.join(BASE_DIR, ENV_FILE), encoding='utf-8', mode='w') as f:
        pass
