import falcon
import jwt
import hashlib
import sys 
sys.path.append('../')
from service.account_service import AccountService
from const.const import *

class LoginResource:
     def on_post(self, req, resp):
         username = req.params.get("username", "") 
         passhash = req.params.get("passhash", "") 
         userObj = AccountService.getUser(username, passhash)
         if userObj is None:
             # user not exist or password not correct
             resp.status = falcon.HTTP_401
             return
         else:
             # jwt && set cookie
             jwtStr = AccountService.encodeJwt(userObj)
             resp.set_cookie(JwtCookieKey, jwtStr, max_age = JwtCookieAge, path = "/", secure = False)
             # user exist, check pass
             resp.body = userObj.toJson()

