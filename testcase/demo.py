import requests

#创建封装的get方法
def requests_get(url,headers):
#2、发送requests get请求
    r=requests.get(url,headers=headers)
#3、获取结果相应内容
    code=r.status_code
    try:
        body=r.json()
    except Exception as e:
        body=r.text
#4、内容存到字典
    res = dict()
    res["code"] = code
    res["body"] = body
#5、字典返回
    return res