import os
#1、获取项目基本目录
#获取当前项目的绝对路径
from utils.YamlUtil import YamlReader

current = os.path.abspath(__file__)
#print("当前文件路径：%s"%current)
#上上两层目录
BASE_DIR = os.path.dirname(os.path.dirname(current))
print("BASE_DIR的路径是：%s"%BASE_DIR)
#定义config目录的路径
_config_path = BASE_DIR + os.sep +"config"
#定义data目录的路径
_data_path = BASE_DIR + os.sep +"data"

#定义conf.yml文件的路径
_config_file = _config_path + os.sep + "conf.yml"
#定义logs文件路径
_log_path = BASE_DIR + os.sep +"logs"
#定义db_conf.yml文件路径
_db_config_file = _config_path + os.sep + "db_conf.yml"
#定义report目录路径
_report_path = BASE_DIR + os.sep + "report"
#print("报告路径是：%s"%_report_path)

def get_report_path():
    return _report_path

def get_config_path():
    return _config_path

def get_config_file():
    return _config_file

def get_log_path():
    return _log_path

def get_db_config_file():
    return _db_config_file

def get_data_path():
    return _data_path

#创建类
class ConfigYml:
    #初始yaml读取配置文件
    def __init__(self):
        self.config = YamlReader(get_config_file()).data()
        self.db_config = YamlReader(get_db_config_file()).data()
    #定义方法获取需要信息
    def get_config_url(self):
        return self.config["BASE"]["test"]["url"]
    #获取日志级别
    def get_conf_log(self):
        return self.config["BASE"]["log_level"]
    # 获取日志扩展名
    def get_conf_extension(self):
        return self.config["BASE"]["log_extension"]
    #定义获取测试用例excel名称
    def get_excel_file(self):
        """
        获取测试用例excel名称
        :return:
        """
        return self.config["BASE"]["test"]["case_file"]
    #获取测试用例sheet名称
    def get_excel_sheet(self):
        """
        获取测试用例sheet名称
        :return:
        """
        return self.config["BASE"]["test"]["case_sheet"]
    #读取不同环境下的db信息
    def get_db_conf_info(self,db_alias):
        """
        根据db_alais获取该名称下的数据库信息
        :param db_alias:
        :return:
        """
        return self.db_config[db_alias]

    def get_email_info(self):
        """
        获取邮件配置相关信息
        :return:
        """
        return self.config["email"]

if __name__ == '__main__':
    conf_read = ConfigYml()
    print("配置文件conf.yml内容是：%s"%conf_read.config)
    print(conf_read.get_config_url())
    print(conf_read.get_conf_log())
    print(conf_read.get_conf_extension())
    print(conf_read.get_db_conf_info("db_pre"))
    print(conf_read.get_excel_file())
    print(conf_read.get_excel_sheet())
    print(conf_read.get_email_info())