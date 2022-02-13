import requests
import pytest
from common.Base import init_db

from utils.Assertutil import AssertUtil
from utils.RequestsUtil import *
from config import conf
import os
from utils.YamlUtil import YamlReader
from config.globalvar import GloblVar
#获取登录测试用例list
login_pre_file = os.path.join(conf.get_data_path(),"pre_login.yml")
#使用工具类读取多个文档内容
#form_data = YamlReader(login_pre_file).data_all()
#注意参数化格式是列表
form_data_list = [(YamlReader(login_pre_file).data()["data"])]
#从配置文件取出请求地址
base_url = (YamlReader(login_pre_file).data()["url"])
print(form_data_list)
print(base_url)

class Test_user_login():
    # form_data_list = [
    #     {'principal': 'zwh8322692', 'password': '123456', 'userType': 'user', 'isRemember': 'true', 'origin': 'web'},
    #     {'principal': 'andrewli', 'password': 'test@123456', 'userType': 'user', 'isRemember': 'true', 'origin': 'web'}]
    @pytest.mark.parametrize("form_data",form_data_list)
    def test_login(self, form_data):
        #base_url = 'https://test-user-web-api.wanshifu.com/user/security/login'
        #request = Requests()
        res = requests.post(url=base_url,data=form_data)
        code = res.status_code
        #取出cookies,然后以json格式输出
        cookie_jar = res.cookies
        #print(cookie_jar)
        cookies = requests.utils.dict_from_cookiejar(cookie_jar)
        return cookies
        # 将token写进全局变量globalvar.py文件里面
        glovar = GloblVar()
        glovar.set_value('token', cookies)
        #打印cookies值
        cok = glovar.get_value("token")
        print("全局变量取到的登录token是：%s" % cok)
        # 3、获取结果断言
        try:
            #assert r["code"] == 200
            AssertUtil().assert_code(code,200)
        except Exception as e:
            print("登录失败")
        print(res)
        #print(rse["code"])
        # 实例化Base的公共数据库方法
        conn = init_db("db_pre")
        res_db = conn.fetchone("select * from t_user_growth_service.user_growth WHERE `user_id` = '5177002976'")
        print(res_db)
        #cookies = r["cookies"]
        #print(cookies)
        #直接将登录后的cookies返回
        #return cookies
# pr = Test_user_login()
# print(pr.test_login({'principal': '13133333333', 'password': '123456', 'userType': 'user', 'isRemember': 'true', 'origin': 'web'}))
if __name__=="__main__":
    pytest.main(["-s","utest_userlogin.py"])