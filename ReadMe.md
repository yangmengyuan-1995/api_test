##### 基础说明:

本项目基于pytest框架, 对接口自动化测试流程的各个步骤进行了封装。在提供了丰富的功能的基础上，还提供了简单、高效的扩展性。

- 读取yaml文件中的测试用例生成自动化测试用例
- 在yaml文件中可以通过指定格式调用函数或变量
- 在yaml文件中可以通过关键字实现数据驱动
- 提供基础的文本断言及数据库断言
- 记录整个测试流程的日志信息
- 集成allure报告，快速生成测试报告



##### 环境部署：

​	1、 `pip install -r requirements.txt `

​	2、安装allure：https://github.com/allure-framework/allure2/releases

​	3、将解压后的文件的bin目录配置到path环境变量

​	4、allure --version 验证



##### 指定格式调用函数或变量:

- 如果你需要在yaml文件中使用函数, 请先查看common/func_collect.py文件中包含的函数, 你可以使用请使用`$(funcname(args))` 的格式调用, 如果这些函数不能满足你的需求, 你也可以在这个文件中自定义函数, 并以同样的格式调用它
- 如果你需要在yaml文件中使用变量, 请使用${get_env_var(变量名)}来调用, 这是一个已经封装好的函数



##### 数据驱动:

- 你可以在yaml用例中使用parametrize关键字来实现数据驱动, 不过在使用时需要注意数据的格式

  ```python
   """
      根据parametrize中的数据生成对应的测试用例
      期望的数据驱动的格式:
      "parametrize": {
          "quantity": 3,   指明用例数量(未指明时会去获取第一个变量(本例中的username)的值列表的长度)
          "params_key": "params",   指明去request.params中寻找变量进行替换
          "titles":  ["正例", "反例1", "反例2"]  测试用例的标题
          "validates": [   测试用例的校验
              "contain": {"返回文本包含success"： ["success", "text"]}
              "contain": {"返回文本包含failed"： ["failed", "text"]}
              "contain": {"返回文本包含failed"： ["failed", "text"]}
          ]
          "params":   需要替换的变量以及它在每条用例中的值
              "username": ["Tom", "Bob", null]         变量名: 值列表
              "password": ["admin", null, "admin"]     变量名: 值列表
      }
      """
  ```

  

##### 项目架构:

- `common`: 存放了通用的工具类
  - `asser_util.py`: 断言工具
  - `core_util.py`: 用例执行标准流程
  - `db_util`.py: 数据库连接工具
  - `ddt_util.py`: 数据驱动工具
  - `env_util.py`: 用例执行过程中读取函数或变量的工具
  - `func_collet.py`: 用例执行过程中可以使用的函数
  - `model.py`: 规定yaml文件的基础格式并进行校验
  - `request_util.py`: 封装request
  - `yaml_util.py`: 封装yaml文件操作
- `logs`：存放用例执行日志
- `temps`: 临时json报告文件夹
- `testcase`: 存放yaml测试用例
  - `test_generate_case.py`: 读取yaml文件, 生成测试用例
- `env.yaml`: 存放用例执行过程中产生的变量
- `pytest.ini`: pytest的基础配置
- `run.py`: 项目入口
- `setting.py`: 一些配置项