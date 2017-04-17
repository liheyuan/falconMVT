import falcon
import json
import sys 
sys.path.append('../')
from const.const import *

class TestNeedAuthResource:
     def on_get(self, req, resp):
         userId = req.params.get(UserIdParamKey, "")
         resp.body = json.dumps({"msg": "test userid=%s success!" % (userId)})

class TestNoNeedAuthResource:
     def on_get(self, req, resp):
         resp.body = json.dumps({"msg": "test not login user success!"})
