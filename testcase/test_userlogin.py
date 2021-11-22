import requests
import pytest
from common.Base import init_db

from utils.Assertutil import AssertUtil
from utils.RequestsUtil import *
from config import conf
import os
from utils.YamlUtil import YamlReader
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
        request = Requests()
        r = request.post(url=base_url,data=form_data)
        # 3、获取结果断言
        try:
            #assert r["code"] == 200
            AssertUtil().assert_code(r["code"],200)
        except Exception as e:
            print("登录失败")
        print(r)
        print(r["code"])
        #实例化Base的公共数据库方法
        conn = init_db("db_pre")
        res_db = conn.fetchone("select * from t_user_growth_service.user_growth WHERE `user_id` = '5177002976'")
        print(res_db)
if __name__=="__main__":
    pytest.main(["-s","test_userlogin.py"])