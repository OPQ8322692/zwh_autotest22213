import json

import jsonpath

from utils.RequestsUtil import Requests
from common import ExcelConfig
from config.conf import ConfigYml
import os
from common.ExcelData import Data
from utils.loggerUtil import my_log
import pytest
from config.globalvar import GloblVar

# 1、初始化测试用例文件
case_file = os.path.join("../data", ConfigYml().get_excel_file())
# 2、测试用例sheet名称
sheet_name = ConfigYml().get_excel_sheet()
# 3、获取运行测试用例列表
run_list = Data(case_file, sheet_name).get_run_list()
print(run_list)
# 4、打印日志
log = my_log()

# 一个用例的执行
# class TestExcel:
#     # 初始化信息url,data
#     def test_run(self):
#         data_key = ExcelConfig.DataConfig()
#         url = run_list[0][data_key.url]
#         case_id = run_list[0][data_key.case_id]
#         case_model = run_list[0][data_key.case_model]
#         case_name = run_list[0][data_key.case_name]
#         pre_exc = run_list[0][data_key.pre_exc]
#         method = run_list[0][data_key.method]
#         params_type = run_list[0][data_key.params_type]
#         params = run_list[0][data_key.params]
#         except_result = run_list[0][data_key.except_result]
#         actual_result = run_list[0][data_key.actual_result]
#         is_run = run_list[0][data_key.is_run]
#         headers = run_list[0][data_key.headers]
#         cookies = run_list[0][data_key.cookies]
#         code = run_list[0][data_key.code]
#         db_result = run_list[0][data_key.db_result]
#         #print(url)
#         #print(case_model)
#
#         #2.接口请求，实例化工具类
#         request = Requests()
#         #params转义json
#         #验证params有没有内容
#         if len(str(params).strip()) is not 0:
#             params = json.loads(params)
#         #method post/get
#         if str(method).lower() == "get":
#             res = request.get(url,json=params)
#         elif str(method).lower() == "post":
#             res = request.post(url,json=params)
#         else:
#             log.error("错误请求method: %s"%method)
#         print(res)
# if __name__ == '__main__':
#     TestExcel().test_run()

#参数化运行,多个用例执行
class TestExcel:
    # 初始化信息url,data
    #1、增加pytest
    @pytest.mark.parametrize("case",run_list)
    def test_run(self,case,get_token):
        data_key = ExcelConfig.DataConfig()
        url = case[data_key.url]
        case_id = case[data_key.case_id]
        case_model = case[data_key.case_model]
        case_name = case[data_key.case_name]
        pre_exc = case[data_key.pre_exc]
        method = case[data_key.method]
        params_type = case[data_key.params_type]
        params = case[data_key.params]
        except_result = case[data_key.except_result]
        actual_result = case[data_key.actual_result]
        is_run = case[data_key.is_run]
        headers = case[data_key.headers]
        cookies = case[data_key.cookies]
        code = case[data_key.code]
        db_result = case[data_key.db_result]
        #print(url)
        #print(case_model)

        #1.判断headers是否存在，存在json转义，无需
        if headers:
            header = json.load(headers)
        else:
            header = headers

        #2.接口请求，实例化工具类
        request = Requests()
        #实例化全局变量类
        golv = GloblVar()
        coki = golv.get_value("token")
        #print(coki)
        #params转义json
        #验证params有没有内容
        if len(str(params).strip()) is not 0:
            params = json.loads(params)
        #method post/get
        if str(method).lower() == "get":
            res = request.get(url,json=params,cookies=get_token)
        elif str(method).lower() == "post":
            #res = request.post(url,json=params,cookies=get_token)
            res = request.post(url,data=params,cookies=get_token)
        else:
            log.error("错误请求method: %s"%method)
        print(res)
        print(type(res))
        body2 = res['body']
        print(body2)
        reorderToken = jsonpath.jsonpath(body2, '$.data.reOrderToken')[0]
        print(reorderToken)


if __name__ == '__main__':
    pytest.main(["-s","test_excel_case.py"])
    #pytest.main()