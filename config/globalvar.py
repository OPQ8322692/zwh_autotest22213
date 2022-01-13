# import pytest
class GloblVar:
   # _global_dict = {}

    def __init__(self):
        global _global_dict
        self._global_dict = {}

    def set_value(self,name,value):
        self._global_dict[name] = value

    def get_value(self,name,defValue=None):
        try:
            return self._global_dict[name]
        except KeyError:
            return defValue

#if __name__ == '__main__':
    #pytest(["-s","globalvar.py"])
# gdd = GloblVar()
# gdd.set_value("zwh",25)
# res = gdd.get_value("zwh")
# print(res)

