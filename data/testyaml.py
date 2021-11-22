from utils.YamlUtil import *
import os
curPath=os.path.dirname(os.path.realpath(__file__))
yaml1=os.path.join(curPath,"test.yml")
testyam = YamlReader(yaml1)
print(testyam.data())