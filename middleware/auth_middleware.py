import falcon
import sys
sys.path.append('../')
from service.account_service import AccountService
from const.const import *

class AuthMiddleware(object):
    def process_request(self, req, resp):
        # if need check auth
        if self.is_path_whitelist(req.path):
            return
        # need check auth cookie
        jwtStr = req.cookies.get(JwtCookieKey, "")
        payloadObj = self.get_jwt_payload(jwtStr)
        if payloadObj == None:
            # payload invalid
            raise falcon.HTTPUnauthorized()
        else:
            # check if valid
            tp = AccountService.parsePayload(payloadObj)
            if not tp:
                # parse payload fail
                raise falcon.HTTPUnauthorized()
            else:
                (userId, tmp) = tp
                req.params[UserIdParamKey] = userId
                # check if need refresh
                if AccountService.needRefreshJwt(payloadObj):
                    if AccountService.allowRefreshJwt(payloadObj):
                        newJwtStr = AccountService.refreshJwt(payloadObj)
                        resp.set_cookie(JwtCookieKey, newJwtStr, max_age = JwtCookieAge, path = "/", secure = False)
                    else:
                        # refresh token fail
                        raise falcon.HTTPUnauthorized()

    def is_path_whitelist(self, path):
        return path == "/account/login" or path == "/test/noneedauth"

    def get_jwt_payload(self, jwtStr):
        return AccountService.decodeJwt(jwtStr)
