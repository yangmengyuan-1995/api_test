"""
@Date  :  2024/12/18 6:55
@File  :  func_collect.py
@Author:  杨梦远
"""
import base64
import hashlib
import os

import rsa
import yaml
from iniconfig import IniConfig
from setting import BASE_DIR, ENV_FILE


class FuncCollectUtil:
    """
    在yaml文件中可以调用的方法的集合, 使用格式 ${func(args)}
    """

    @staticmethod
    def get_env_var(var_name):
        """
        获取环境变量
        :param var_name: 变量名字
        :return: 变量值, 未找到时返回None
        """
        with open(os.path.join(BASE_DIR, ENV_FILE), encoding='utf-8') as f:
            value = yaml.safe_load(f)
            try:
                return value[var_name]
            except KeyError:
                return None

    @staticmethod
    def get_base_url(key):
        ini = IniConfig(os.path.join(BASE_DIR, "pytest.ini"))
        if "base_url" not in ini:
            raise Exception('pytest.ini 文件中未配置"base_url"')
        else:
            if ini["base_url"].get(key):
                return ini["base_url"][key]
            else:
                raise Exception(f'pytest.ini文件中 base_url 配置中没有key: {key}')

    @staticmethod
    def md5_encode(data):
        data = str(data).encode('utf-8')
        # md5加密, 哈希算法
        md5_value = hashlib.md5(data).hexdigest()
        return md5_value

    @staticmethod
    def base64_encode(data):
        data = str(data).encode('utf-8')
        base64_value = base64.b64encode(data).decode(encoding='utf-8')
        return base64_value

    @staticmethod
    def create_rsk_key():
        (pub_key, pri_key) = rsa.newkeys(1024)
        with open(os.path.join(BASE_DIR, "conf/public.pem"), "w+") as f:
            f.write(pub_key.save_pkcs1().decode())
        with open(os.path.join(BASE_DIR, "conf/private.pem"), "w+") as f:
            f.write(pri_key.save_pkcs1().decode())

    @staticmethod
    def rsa_encode(data):
        # 加载公钥
        with open(os.path.join(BASE_DIR, "conf/public.pem")) as f:
            pub_key = rsa.PublicKey.load_pkcs1(f.read().encode())
        # 把data转化成utf-8的编码格式
        data = str(data).encode('utf-8')
        # 把字符串加密成byte类型
        byte_value = rsa.encrypt(data, pub_key)
        # 把字节转化为字符串格式
        rsa_value = base64.b64encode(byte_value).decode('utf-8')
        return rsa_value



