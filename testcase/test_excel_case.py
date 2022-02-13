import json

import allure
import jsonpath

from config import conf



from utils.Assertutil import AssertUtil

from common import Base
from common.Base import allure_report
from common.Base import res_sub, params_find
from utils.RequestsUtil import Requests
from common import ExcelConfig
from config.conf import ConfigYml
import os
from common.ExcelData import Data
from utils.loggerUtil import my_log
import pytest
from config.globalvar import GloblVar


# 1、初始化测试用例文件
case_file = os.path.join("../testcase", ConfigYml().get_excel_file())
# 2、测试用例sheet名称
sheet_name = ConfigYml().get_excel_sheet()
# 3、获取运行全部为y的测试用例列表
data_init = Data(case_file, sheet_name)
run_list = data_init.get_run_list()
print(run_list)
# 4、打印日志
log = my_log()
#初始化DataConfig
data_key = ExcelConfig.DataConfig()

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
    def run_api(self,url,get_token,method,params_type,params=None,header=None,cookies=None):
        """
        发送请求api
        :return:
        """
        # 2.接口请求，实例化工具类
        request = Requests()
        # params转义json
        # 验证params有没有内容
        if len(str(params).strip()) is not 0:
            params = json.loads(params)
        # method post/get
        if str(method).lower() == "get":
            r = request.get(url, json=params, cookies=get_token)
        elif str(method).lower() == "post" and params_type == "data":
            r = request.post(url, data=params, cookies=get_token)
        elif str(method).lower() == "post" and params_type == "json":
            r = request.post(url, json=params, cookies=get_token)
        else:
            log.error("错误请求method: %s" % method)
        return r

    def run_pre(self,pre_case,get_token):
        #初始化数据
        pass
        url = pre_case[data_key.url]
        method = pre_case[data_key.method]
        params = pre_case[data_key.params]
        headers = pre_case[data_key.headers]
        params_type = pre_case[data_key.params_type]
        cookies = pre_case[data_key.cookies]
        #判断headers是否存在，存在json转义，无需
        headers = Base.json_parse(headers)
        #self.run_api(url=url,get_token=get_token,method=method,params=params,header=headers,cookies=get_token,params_type=params_type)
        res = self.run_api(url=url, get_token=get_token, method=method, params_type=params_type, params=params,header=headers, cookies=get_token)
        return res

    def get_correlation(self,headers, cookies, params, pre_res):
        # 验证是否有关联
        headers_para, cookies_para, params_para = Base.params_find(headers, cookies, params)
        #print("patamsdata数据为：%s"%params_para)
        # 有关联，执行前置用例，获取结果
        if len(headers_para):
            headers_data = pre_res["body"][headers_para[0]]
            # 结果替换
            headers = Base.res_sub(headers, headers_data)
        if len(cookies_para):
            cookies_data = pre_res["body"][cookies_para[0]]
            # 结果替换
            cookies = Base.res_sub(cookies, cookies_data)
        if len(params_para):
            print("需要替换的变量为：%s"%params_para)
            params_data = pre_res["body"]["data"][params_para[0]]
            #params_data = jsonpath.jsonpath(pre_res["body"], '$.data.reOrderToken')[0]
            print("需要替换的变量值是：%s"%params_data)
            # 结果替换
            params = Base.res_sub(params, params_data)
        return headers, cookies, params

    # 初始化信息url,data
    #1、增加pytest
    @pytest.mark.parametrize("case",run_list)
    def test_run(self,case,get_token):
        #data_key = ExcelConfig.DataConfig()
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
        # if headers:
        #     header = json.load(headers)
        # else:
        #     header = headers
        # #2、增加cookies
        # if cookies:
        #     cookie = json.loads(cookies)
        # else:
        #     cookie = cookies
        #header = Base.json_parse(headers)
        #cookie = Base.josn_parse(cookies)

        #1、验证前置条件
        if pre_exc:
            pass
        #2、找到执行用例
            #前置测试用例
            pre_case = data_init.get_case_pre(pre_exc)
            print("前置条件信息为：%s"%pre_exc)
            print("前置用例为：%s"%pre_case)
            pre_res = self.run_pre(pre_case,get_token)
            print("执行前置用例结果为：%s"%pre_res)
            #print("执行前置用例body结果为：%s"%pre_res["body"]["data"]["reOrderToken"])
            #替换
            #params = Base.json_parse(params)
            #print("将json中的null转换为字典格式：%s"%params)
            # 注意需要转换成字符串传参
            #print("格式化字典参数是：\"%s\""%params)
            #params1 = '"'+str(params)+'"'
            #params = '"{}"'.format(str(params))
            print(params)
            headers,cookies,params = self.get_correlation(headers,cookies,params,pre_res)
            #paramend = json.loads(params3)
            print("替换后的参数是：%s"%params)
        # headers = Base.json_parse(headers)
        # cookies = Base.json_parse(cookies)
        # params = Base.json_parse(params)
        # print("字典化参数为：%s"%params)
        #执行正常的测试用例
        res = self.run_api(url=url,get_token=get_token,method=method,params_type=params_type,params=params,header=headers,cookies=get_token)
        print(res)

        #allure
        #sheet名称 feature一级标签
        allure.dynamic.feature(sheet_name)
        #模块 story 二级标签
        allure.dynamic.story(case_model)
        #用例ID+接口名称 title
        allure.dynamic.title(case_id+case_name)
        #请求URL 请求类型 期望结果 实际结果 描述,换行格式加颜色
        desc = "<font color='red'>请求URL:</font>{}<Br/>" \
                "<font color='red'>请求类型:</font>{}<Br/>" \
                "<font color='red'>期望结果:</font>{}<Br/>" \
                "<font color='red'>实际结果:</font>{}".format(url,method,except_result,res)
        allure.dynamic.description(desc)

        #断言验证
        #状态码，返回结果内容，数据库相关的结果的验证
        #状态码
        assert_util = AssertUtil()
        assert_util.assert_code(int(res["code"]),int(code))
        #验证结果内容，包含，注意表格中要用单引号，因为返回的结果是字典类型
        assert_util.assert_in_body(str(res["body"]),str(except_result))
        #数据库结果断言,应该要用if先判断表格是否有值 再执行
        #初始化数据库
        from common.Base import init_db
        sql = init_db("db_pre")
        if db_result:
            #查询sqp语句，excel定义好的
            db_res = sql.fetchone(db_result)
            log.debug("数据库查询结果：{}".format(str(db_res)))
            #数据库结果与接口返回的结果验证
            #获取数据库结果的key
            verify_list = list(dict(db_res).keys())
            print("数据库查询的key：%s"%verify_list)
            #根据key获取数据库结果，接口结果,注意接口返回的层级，是在data嵌套里面的
            for line in verify_list:
                res_line = res["body"]["data"][line]
                res_db_line = dict(db_res)[line]
            #验证
                assert_util.assert_body(res_line,res_db_line)

        #3、验证请求中是否有${}$，有则返回${}$内容
            #params2 = get_correlation(headers, cookies, params, 123)
            #params2 = get_correlation(headers,cookies,params,res)
        # str1 = '{"Auto":"cookies${token}$"}'
        # if "${" in str1:
        #     print(str1)
        # import re
        # """
        # re.compile 函数
        # compile 函数用于编译正则表达式，生成一个正则表达式（ Pattern ）对象，供 match() 和 search()  findall()这两个函数使用。
        # 语法格式为：re.compile(pattern[, flags])
        # import re
        # pattern = re.compile(r'\d+')   # 查找数字
        # result1 = pattern.findall('runoob 123 google 456')
        # result2 = pattern.findall('run88oob123google456', 0, 10)
        # print(result1)--['123', '456']
        # print(result2)--['88', '12']
        # """
        # pattern = re.compile('\${(.*)}\$')
        # re_res = pattern.findall(str1)
        # #找出变量token,返回的是列表
        # print(re_res[0])
        # #3.1根据内容token，查询，前置条件测试用例返回结果token = 值
        # token = "123"
        # #3.2根据变量结果内容，替换
        # """
        # re.sub(pattern,repl,string)
        # pattern:表示正则表达式中的模式字符串；
        # repl:被替换的字符串（既可以是字符串，也可以是函数）；
        # string:要被处理的，要被替换的字符串；
        # """
        # res2 = re.sub(pattern,token,str1)
        # print(res2)
        # res = self.run_api(url=url,get_token=get_token,method=method,params_type=params_type,params=param4,header=headers,cookies=get_token)
        # print(res)

        # #2.接口请求，实例化工具类
        # request = Requests()
        # # #实例化全局变量类
        # # golv = GloblVar()
        # # coki = golv.get_value("token")
        # #params转义json
        # #验证params有没有内容
        # if len(str(params).strip()) is not 0:
        #     params = json.loads(params)
        # #method post/get
        # if str(method).lower() == "get":
        #     res = request.get(url,json=params,cookies=get_token)
        # elif str(method).lower() == "post" and params_type =="data":
        #     res = request.post(url,data=params,cookies=get_token)
        # elif str(method).lower() == "post" and params_type =="json":
        #     res = request.post(url,json=params,cookies=get_token)
        # else:
        #     log.error("错误请求method: %s"%method)
        # print(res)
        # print(type(res))
        # body2 = res['body']
        # print(body2)
        #reorderToken = jsonpath.jsonpath(body2, '$.data.reOrderToken')[0]
        #print(reorderToken)


if __name__ == '__main__':
    #定义报告路径
    report_path = conf.get_report_path() + os.sep + "result"
    print("报告文件夹名称为：%s" % report_path)
    print("调试：%s"%11111)
    report_html_path = conf.get_report_path() + os.sep + "html"
    # print("报告html文件名称为：%s" % report_html_path)
    pytest.main(["-s", "test_excel_case.py", "--alluredir", report_path])
    Base.allure_report(report_path,report_html_path)
    Base.send_email(title = "接口测试报告结果",content = report_html_path)
    # allure_report(report_path,report_html_path)

    #pytest.main(["-s","test_excel_case.py"])
    #pytest.main()

#print("ddddddddddddddddddddddddddddd: ",__name__)