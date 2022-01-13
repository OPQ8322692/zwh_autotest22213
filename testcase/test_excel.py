from testcase.test_userlogin import Test_user_login
from utils.RequestsUtil import Requests
from utils.ExcelUtil import ExcelReader
#相对路径：
#reader = ExcelReader("../data/auto_test_excel.xlsx","万师傅用户组接口用例模板")
#绝对路径：
reader = ExcelReader("E:\zwh_autotest\data\auto_test_excel.xlsx","万师傅用户组接口用例模板")
print(reader.data())
url = reader.data()[0]["请求URL"]
data = reader.data()[0]["请求参数"]
request = Requests()
r = Test_user_login()
cookies = r.test_login()
print(cookies)
# res = request.post(url,data=data,cookies = cookies)
# print(res)