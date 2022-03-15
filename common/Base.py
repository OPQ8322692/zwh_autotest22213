import json
import os
from wsgiref import headers

import pytest

from config import conf
from config.conf import ConfigYml
from utils.EmailUtil import SendEmail
from utils.MysqlUtil import Mysql
import re
#from utils.loggerUtil import my_log
import logging
import subprocess
log = logging
#给正则表达式模式初始值
p_data = '\${(.*)}\$'

#1、定义init_db
def init_db(db_alias):
#2、初始数据库信息，通过配置文件
    db_info = ConfigYml().get_db_conf_info(db_alias)
    host = db_info["db_host"]
    user = db_info["db_user"]
    password = db_info["db_password"]
    db_name = db_info["db_name"]
    charset = db_info["db_charset"]
    port = db_info["db_port"]
#3、初始化mysql对象
    conn = Mysql(host,user,password,db_name,charset,port)
    print(conn)
    return conn

def json_parse(data):
    """
    格式化字符，转换json
    :param data:
    :return:
    """
    # if headers:
    #     header = json.loads(headers)
    # else:
    #     header = headers
    #列表推导式
    return json.loads(data) if data else data

def res_find(data,pattern_data=p_data):
    """
    增加查询变量公共方法
    找出变量如token,后面进行替换,返回的是列表，增加返回值
    :param data:
    :return:
    """
    #pattern = re.compile('\${(.*)}\$')
    pattern = re.compile(pattern_data)
    re_res = pattern.findall(data)
    #print(re_res)
    return re_res

def res_sub(data,replace,pattern_data=p_data):
    """
    替换
    :param data:要被处理的，要被替换的字符串
    :param replace:被替换的字符串（既可以是字符串，也可以是函数）
    :param pattern_data:
    :return:
    """
    pattern = re.compile(pattern_data)
    re_res = pattern.findall(data)
    #print(re_res)
    if re_res:
        return re.sub(pattern_data,replace,data)
    return re_res

def params_find(headers,cookies,params):
    """
    验证请求中是否${}$，返回${}$内容,返回的是列表
    :param headers:
    :param cookies:
    :param params:
    :return:
    """
    if "${" in headers:
        headers = res_find(headers)
    if "${" in cookies:
        cookies = res_find(cookies)
    if "${" in params:
        params = res_find(params)
    return headers,cookies,params

def allure_report(report_path,report_html):
    """
    生成allure报告
    :param report_path:
    :param report_html:
    :return:
    """
    #执行命令 allure generate
    #t_allure>allure generate report/result.txt -o report/html --clean
    allure_cmd = "allure generate %s -o %s --clean"%(report_path,report_html)
    log.info("报告地址")
    try:
        subprocess.call(allure_cmd,shell=True)
    except:
        log.error("执行用例失败，请检查一下测试环境相关配置")
        raise

def send_email(report_html_path="",content="",title="测试"):
    """
    发送邮件
    :param report_html_path:
    :param content:
    :param title:
    :return:
    """
    email_info = ConfigYml().get_email_info()
    smtp_addr = email_info["smtpserver"]
    username = email_info["username"]
    password = email_info["password"]
    password = email_info["password"]
    recv = email_info["receiver"]
    email = SendEmail(
        smtp_addr = smtp_addr,
        username = username ,
        password = password,
        recv = recv,
        title = title,
        content = content,
        file = report_html_path)
    email.send_mail()

if __name__ == '__main__':
    init_db("db_pre")
    print(res_find('{"Auto":"cookies${token3}$"}'))
    #print(res_sub('{"Auto":"cookies${token3}$"}',"123"))
    params2 = "{'code': 200, 'body': {'code': 'success', 'data': {'autoAppointRuleId': 0, 'autoAppointRuleName': '', 'hasWaitAuditSettlementChange': False, 'innovative': {'lastOrderInfo': None, 'orderRecordExists': {'customized': True, 'renovation': True}}, 'isFirstOrder': '0', 'lastOrderType': 'order', 'orderInfo': None, 'orderUserCount': '406874', 'reOrderToken': 'ee${reOrderToken}$', 'serveMenuInfo': {'lastCategoryId': 1, 'lastServeType': 5, 'selectCategoryId': 1, 'selectServeType': 5, 'serveCategoryInfoList': [{'categoryId': 1, 'serveTypeInfoList': [{'serveType': 1, 'serveTypeId': 1, 'supportDefinitePrice': False, 'supportOfferPrice': True}, {'serveType': 2, 'serveTypeId': 2, 'supportDefinitePrice': False, 'supportOfferPrice': True}, {'serveType': 3, 'serveTypeId': 3, 'supportDefinitePrice': False, 'supportOfferPrice': True}, {'serveType': 4, 'serveTypeId': 4, 'supportDefinitePrice': False, 'supportOfferPrice': True}, {'serveType': 5, 'serveTypeId': 5, 'supportDefinitePrice': False, 'supportOfferPrice': True}, {'serveType': 6, 'serveTypeId': 6, 'supportDefinitePrice': False, 'supportOfferPrice': True}, {'serveType': 7, 'serveTypeId': 7, 'supportDefinitePrice': False, 'supportOfferPrice': True}], 'serverTypeIdList': [1, 2, 3, 4, 5, 6, 7]}, {'categoryId': 2, 'serveTypeInfoList': [{'serveType': 4, 'serveTypeId': 10, 'supportDefinitePrice': True, 'supportOfferPrice': True}, {'serveType': 5, 'serveTypeId': 11, 'supportDefinitePrice': False, 'supportOfferPrice': True}], 'serverTypeIdList': [10, 11]}, {'categoryId': 4, 'serveTypeInfoList': [{'serveType': 4, 'serveTypeId': 15, 'supportDefinitePrice': True, 'supportOfferPrice': True}, {'serveType': 9, 'serveTypeId': 49, 'supportDefinitePrice': False, 'supportOfferPrice': True}, {'serveType': 5, 'serveTypeId': 16, 'supportDefinitePrice': False, 'supportOfferPrice': True}, {'serveType': 2, 'serveTypeId': 13, 'supportDefinitePrice': False, 'supportOfferPrice': True}, {'serveType': 3, 'serveTypeId': 14, 'supportDefinitePrice': False, 'supportOfferPrice': True}, {'serveType': 6, 'serveTypeId': 18, 'supportDefinitePrice': False, 'supportOfferPrice': True}], 'serverTypeIdList': [15, 49, 16, 13, 14, 18]}, {'categoryId': 6, 'serveTypeInfoList': [{'serveType': 4, 'serveTypeId': 50, 'supportDefinitePrice': True, 'supportOfferPrice': True}, {'serveType': 9, 'serveTypeId': 51, 'supportDefinitePrice': True, 'supportOfferPrice': True}], 'serverTypeIdList': [50, 51]}, {'categoryId': 7, 'serveTypeInfoList': [{'serveType': 4, 'serveTypeId': 52, 'supportDefinitePrice': False, 'supportOfferPrice': True}, {'serveType': 9, 'serveTypeId': 53, 'supportDefinitePrice': True, 'supportOfferPrice': False}], 'serverTypeIdList': [52, 53]}, {'categoryId': 8, 'serveTypeInfoList': [{'serveType': 4, 'serveTypeId': 21, 'supportDefinitePrice': False, 'supportOfferPrice': True}], 'serverTypeIdList': [21]}, {'categoryId': 9, 'serveTypeInfoList': [{'serveType': 4, 'serveTypeId': 24, 'supportDefinitePrice': False, 'supportOfferPrice': True}], 'serverTypeIdList': [24]}, {'categoryId': 10, 'serveTypeInfoList': [{'serveType': 2, 'serveTypeId': 25, 'supportDefinitePrice': False, 'supportOfferPrice': True}, {'serveType': 3, 'serveTypeId': 26, 'supportDefinitePrice': False, 'supportOfferPrice': True}, {'serveType': 4, 'serveTypeId': 27, 'supportDefinitePrice': False, 'supportOfferPrice': True}, {'serveType': 6, 'serveTypeId': 28, 'supportDefinitePrice': False, 'supportOfferPrice': True}], 'serverTypeIdList': [25, 26, 27, 28]}, {'categoryId': 12, 'serveTypeInfoList': [{'serveType': 4, 'serveTypeId': 31, 'supportDefinitePrice': True, 'supportOfferPrice': True}, {'serveType': 5, 'serveTypeId': 32, 'supportDefinitePrice': False, 'supportOfferPrice': True}], 'serverTypeIdList': [31, 32]}, {'categoryId': 13, 'serveTypeInfoList': [{'serveType': 4, 'serveTypeId': 33, 'supportDefinitePrice': True, 'supportOfferPrice': True}, {'serveType': 5, 'serveTypeId': 34, 'supportDefinitePrice': False, 'supportOfferPrice': True}], 'serverTypeIdList': [33, 34]}, {'categoryId': 14, 'serveTypeInfoList': [{'serveType': 2, 'serveTypeId': 35, 'supportDefinitePrice': False, 'supportOfferPrice': True}, {'serveType': 3, 'serveTypeId': 36, 'supportDefinitePrice': False, 'supportOfferPrice': True}, {'serveType': 4, 'serveTypeId': 37, 'supportDefinitePrice': False, 'supportOfferPrice': True}, {'serveType': 6, 'serveTypeId': 38, 'supportDefinitePrice': False, 'supportOfferPrice': True}], 'serverTypeIdList': [35, 36, 37, 38]}, {'categoryId': 15, 'serveTypeInfoList': [{'serveType': 4, 'serveTypeId': 39, 'supportDefinitePrice': True, 'supportOfferPrice': True}, {'serveType': 5, 'serveTypeId': 40, 'supportDefinitePrice': False, 'supportOfferPrice': True}], 'serverTypeIdList': [39, 40]}, {'categoryId': 17, 'serveTypeInfoList': [{'serveType': 4, 'serveTypeId': 45, 'supportDefinitePrice': True, 'supportOfferPrice': True}, {'serveType': 5, 'serveTypeId': 46, 'supportDefinitePrice': False, 'supportOfferPrice': True}], 'serverTypeIdList': [45, 46]}, {'categoryId': 18, 'serveTypeInfoList': [{'serveType': 4, 'serveTypeId': 47, 'supportDefinitePrice': False, 'supportOfferPrice': True}, {'serveType': 5, 'serveTypeId': 48, 'supportDefinitePrice': False, 'supportOfferPrice': True}], 'serverTypeIdList': [47, 48]}, {'categoryId': 10001, 'serveTypeInfoList': [{'serveType': 220, 'serveTypeId': 100011000, 'supportDefinitePrice': False, 'supportOfferPrice': True}, {'serveType': 224, 'serveTypeId': 100011006, 'supportDefinitePrice': False, 'supportOfferPrice': True}, {'serveType': 227, 'serveTypeId': 100011012, 'supportDefinitePrice': False, 'supportOfferPrice': True}, {'serveType': 231, 'serveTypeId': 100011020, 'supportDefinitePrice': False, 'supportOfferPrice': True}, {'serveType': 212, 'serveTypeId': 100011026, 'supportDefinitePrice': False, 'supportOfferPrice': True}, {'serveType': 235, 'serveTypeId': 100011028, 'supportDefinitePrice': False, 'supportOfferPrice': True}, {'serveType': 221, 'serveTypeId': 100011002, 'supportDefinitePrice': False, 'supportOfferPrice': True}, {'serveType': 226, 'serveTypeId': 100011010, 'supportDefinitePrice': False, 'supportOfferPrice': True}, {'serveType': 228, 'serveTypeId': 100011014, 'supportDefinitePrice': False, 'supportOfferPrice': True}, {'serveType': 232, 'serveTypeId': 100011022, 'supportDefinitePrice': False, 'supportOfferPrice': True}, {'serveType': 236, 'serveTypeId': 100011030, 'supportDefinitePrice': False, 'supportOfferPrice': True}, {'serveType': 223, 'serveTypeId': 100011004, 'supportDefinitePrice': False, 'supportOfferPrice': True}, {'serveType': 225, 'serveTypeId': 100011008, 'supportDefinitePrice': False, 'supportOfferPrice': True}, {'serveType': 229, 'serveTypeId': 100011016, 'supportDefinitePrice': False, 'supportOfferPrice': True}, {'serveType': 233, 'serveTypeId': 100011024, 'supportDefinitePrice': False, 'supportOfferPrice': True}, {'serveType': 237, 'serveTypeId': 100011032, 'supportDefinitePrice': False, 'supportOfferPrice': True}, {'serveType': 230, 'serveTypeId': 100011018, 'supportDefinitePrice': False, 'supportOfferPrice': True}, {'serveType': 238, 'serveTypeId': 100011034, 'supportDefinitePrice': False, 'supportOfferPrice': True}], 'serverTypeIdList': [100011000, 100011006, 100011012, 100011020, 100011026, 100011028, 100011002, 100011010, 100011014, 100011022, 100011030, 100011004, 100011008, 100011016, 100011024, 100011032, 100011018, 100011034]}]}, 'toAccountInfo': None, 'userBlackInfoList': []}, 'msg': '', 'status': '1'}, 'data': {'action': 'create'}}"
    params3 = "{'orderGoodsList': [{'addedService': None, 'ancillaryGoods': {'notContainAccessory': {}}, 'bulk': None, 'bulkAttr': None, 'bulkExtra': {}, 'bulkUnit': None, 'category': 402, 'categoryChild': 72, 'categoryChildName': '儿童床', 'categoryName': '床类', 'checkStatus': 1, 'createTime': 1639191159, 'doorCategory': None, 'doorCategoryAttr': {}, 'environmentalImgLists': [{'attachmentId': 5194576576, 'fileName': '', 'fileType': 'image', 'fileUrl': '', 'path': 'https://qncdn.wanshifu.com/4e6d578872ba8849795d6fce16dbd3de'}, {'attachmentId': None, 'fileName': 'OAuth2.0协议.pdf', 'fileType': 'pdf', 'fileUrl': 'https://qncdn.wanshifu.com/0ee9b6539ab4ba32e9e06e17084015cf.pdf', 'path': None}], 'fixedWallAttr': {'needFixedWall': ''}, 'goodsAttr': {}, 'goodsBrand': None, 'goodsInfo': '{}', 'goodsUnit': '张', 'installAttr': None, 'installRequire': None, 'isDefaultImg': None, 'isDefinitePrice': 1, 'isDisassemble': '0', 'isMeasure': None, 'isNeedSnCode': None, 'isOption': 1, 'isShowSnButton': None, 'maintainType': None, 'name': '666', 'note': None, 'number': 1, 'otherInfo': '不含其它', 'picNum': 5, 'repairType': None, 'serveCategory': 1, 'serveCategoryName': '家具', 'status': 1, 'thirdLabel': 'platform', 'tipDoorNum': None, 'ugId': 6474724, 'updateTime': 1642063752, 'useCount': 54247, 'userGoodsImageList': [{'aid': 4847844383, 'path': 'https://qncdn.wanshifu.com/432535b2acd7df0f14ec66deb8df4187'}, {'aid': 4851192519, 'path': 'https://qncdn.wanshifu.com/7cbbed78160183fb0a1854b6df1c54e6'}, {'aid': 5045501386, 'path': 'https://qncdn.wanshifu.com/a7d25c847f8d86c98437e9494a9d162d'}, {'aid': 5045501525, 'path': 'https://qncdn.wanshifu.com/463002ad0fa774e222491c71619c4636'}, {'aid': 5045501526, 'path': 'https://qncdn.wanshifu.com/65e3028f0a3150f35ed08ac89f48a1d6'}], 'userVideo': {}, 'wallFixed': None, 'weight': None, 'uniKey': 'kydurg5l', 'goodsName': '666', 'videoType': None, 'videoUrl': None, 'videoId': None, 'orderGoodsImage': {'goodsImageList': [{'attachmentId': 4847844383}, {'attachmentId': 4851192519}, {'attachmentId': 5045501386}, {'attachmentId': 5045501525}, {'attachmentId': 5045501526}], 'environmentImageList': [{'fileType': 'image', 'attachmentId': 5194576576, 'fileName': '', 'fileUrl': 'https://qncdn.wanshifu.com/4e6d578872ba8849795d6fce16dbd3de'}, {'fileType': 'pdf', 'attachmentId': None, 'fileName': 'OAuth2.0协议.pdf', 'fileUrl': 'https://qncdn.wanshifu.com/0ee9b6539ab4ba32e9e06e17084015cf.pdf'}]}, 'goodsCategory': 402}], 'toAccountId': None, 'reOrderToken': '${reOrderToken}$', 'orderBase': {'fourthDivisionId': 440306001, 'thirdDivisionId': 440306, 'serveTypeId': 4, 'categoryId': 1, 'serveType': 4}, 'isDefinitePrice': '0', 'orderExtraData': {'contactName': '张三', 'contactPhone': '15915329917', 'buyerAddress': '新安街道某街道某某路某花园', 'buyerPhone': '13612345678', 'buyerName': '万某某', 'floorNum': '0'}, 'orderLogisticsInfo': {'trackingIsIdentified': 0, 'customArriveStatus': '2'}, 'autoAppointRuleId': ''}"
    print(res_find(params3))
    #dict = {"body":{"token":"123"}}
    #print(get_correlation('{"Auto":"cookies${token}$"}','{"Auto":"cookies${token}$"}','{"Auto":"cookies${token}$"}',dict))
    # pytest.main(["-s","Base.py","--alluredir","./report3/result.txt"])
    # test_allure_report("./report3/result.txt","./report3/html")


    report_path = conf.get_report_path() + os.sep + "result.txt"
    print("报告文件夹名称为：%s"%report_path)
    report_html_path = conf.get_report_path() + os.sep + "html"
    print("报告html文件名称为：%s" % report_html_path)
    pytest.main(["-s", "Base.py", "--alluredir", report_path])
    allure_report(report_path, report_html_path)

    # 注意用绝对路径时，前面要用r
    # pytest.main(["-s", "Base.py", "--alluredir", r"E:\zwh_autotest\report\result.txt"])
    # allure_report(r"E:\zwh_autotest\report\result.txt", r"E:\zwh_autotest\report\html")

