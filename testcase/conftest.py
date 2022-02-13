"""
pytest框架中token的处理
然后现在我用pytest框架也有这个问题，我刚开始思路是执行完登录接口拿到token进行return，然后其他的接口先import这个接口，然后调用登录接口可以拿到token，但是这个时候我发现我执行其他接口的时候，总是会把登录接口再执行一遍，我觉得这样不太好。
然后我就用pytest的fixture来处理这个情况。创建一个conftes文件，这个文件要和case在同一个package下，在这里边添加修饰器@pytest.fixture()，然后再此处调用登录接口，return出来token，然后其他的接口用到token的时候直接用就可以了，就不需要引用登录模块了。
fixture:这个主要是处理一些前置或者后置条件
1/总结：如果@pytest.fixture()里面没有参数，那么默认scope=”function”，也就是此时的级别的function，针对函数有效,conftest.py与运行的用例要在同一个pakage下，并且有init.py文件
2/pytest.fixture(scope="class")：class级别的fixture，在每个类里，只会在第一次调用前执行一次
# conftest.py
import pytest

@pytest.fixture(scope="class")
def login():
    print("登录系统")

# test_fix.py
import pytest

class Test1:
    def test_s1(self,login):
        print("用例1：登录之后其它动作111")

    def test_s2(self):  # 不传login
        print("用例2：不需要登录，操作222")

    def test_s3(self, login):
        print("用例3：登录之后其它动作333")
"""
import pytest
from testcase.test_userlogin import *
from testcase.test_userlogin import form_data_list

Pre_login = Test_user_login()
data2 = form_data_list[0]
#token = Pre_login.test_login({'principal': '13133333333', 'password': '123456', 'userType': 'user', 'isRemember': 'true', 'origin': 'web'})
# token = Pre_login.test_login(data2)
# print(token)

@pytest.fixture(scope="class")
def get_token():
    token = Pre_login.test_login(data2)
    #print(token)
    return token

if __name__ == "__main__":
    pytest.main(["-s","conftest.py"])