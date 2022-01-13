from utils.ExcelUtil import ExcelReader
import pytest
from common.ExcelConfig import DataConfig
from config.conf import ConfigYml
import os
class Data:
    def __init__(self, testcase_file,sheet_name):
        # 1、使用ecxel工具类，获取结果list
        # reader = ExcelReader("../data/auto_test_excel.xlsx","万师傅用户组接口用例模板")
        self.reader = ExcelReader(testcase_file, sheet_name)
        #print(self.reader.data())

    # 2、列是否运行内容，y
    def get_run_list(self):
        """
        根据是否运行列==y,获取执行测试用例
        :return:
        """
        run_list = list()
        for line in self.reader.data():
            #判断列y，不管大小写都转成小写
            if str(line[DataConfig().is_run]).lower() == "y":
                print(line)
                # 3、保存要执行结果，放到新的列表
                run_list.append(line)
        #print(run_list)
        return run_list

if __name__ == '__main__':
    # pytest.main(["-s","ExcelData.py"])
    #reader = Data("../data/auto_test_excel.xlsx", "万师傅用户组接口用例模板")
    conf_read = ConfigYml()
    test_file = conf_read.get_excel_file()
    #注意文件要用绝对或相对路径
    reader = Data("../data"+os.sep+test_file,conf_read.get_excel_sheet())
    res = reader.get_run_list()
