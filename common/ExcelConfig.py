#定义类
class DataConfig:
    #用例ID	模块	接口名称	请求URL	前置条件	请求类型	请求参数类型
    # 请求参数	预期结果	实际结果	是否运行	headers	cookies	status_code	数据库验证
    case_id = "用例ID"
    case_model = "模块"
    case_name = "用例名称"
    url = "请求URL"
    pre_exc = "前置条件"
    method = "请求类型"
    params_type = "请求参数类型"
    params = "请求参数"
    except_result = "预期结果"
    actual_result = "预期结果"
    is_run = "是否运行"
    headers = "headers"
    cookies = "cookies"
    code = "status_code"
    db_result = "数据库验证"
    Post_result = "后置条件"
    db_result_want_to = "数据库是否要验证"
    Product_line = "产品线"