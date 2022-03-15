import pytest
from config import conf
import os

if __name__ == '__main__':
    #123345
    report_path = conf.get_report_path() + os.sep + "result.txt"
    print(report_path)
    report_html_path = conf.get_report_path() + os.sep + "html"
    pytest.main(["-s","--alluredir", report_path])