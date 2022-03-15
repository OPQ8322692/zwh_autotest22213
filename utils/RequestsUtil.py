#重构
#1、创建类
import requests

from utils.loggerUtil import my_log
from config.globalvar import GloblVar


class Requests:
#2、定义公共方法
    def __init__(self):
        self.log = my_log("Request")
    def requests_api(self,url,data=None,json=None,params=None,headers=None,cookies=None,method="get"):
        #1、增加方法的参数，根据参数来验证方法get/post，方法请求
        if method == "get":
            #get请求
            self.log.debug("发送get请求")
            r = requests.get(url,data=data,json=json,params=params,cookies=cookies,headers=headers)
        elif method == "post":
            self.log.debug("发送post请求")
            r = requests.post(url,data=data,json=json,cookies=cookies,headers=headers)
        # 获取结果相应内容
        code = r.status_code
        # #取出cookies,然后以json格式输出
        # cookie_jar = r.cookies
        # cookies = requests.utils.dict_from_cookiejar(cookie_jar)
        try:
            body = r.json()
        except Exception as e:
            body = r.text
        # 内容存到字典
        res = dict()
        res["code"] = code
        res["body"] = body
        #res["body"]["data"] = data
        #res["cookies"] = cookies
        # #将token写进全局变量globalvar.py文件里面
        # glovar = GloblVar()
        # glovar.set_value('token', cookies)
        # #打印cookies值
        # cok = glovar.get_value("token")
        # print("全局变量取到的登录token是：%s"%cok)
        # 字典返回
        return res
        #print(res["code"])
        #print(res)
#3、重构get/post方法
    #定义get方法
    def get(self,url,**kwargs):
    #定义参数
    #url,json,headers,cookies,method
    #调用公共方法
        return self.requests_api(url,method="get",**kwargs)

    def post(self,url,**kwargs):
    #定义参数url,json,headers,cookies,method
    #调用公共方法
        return self.requests_api(url,method="post",**kwargs)