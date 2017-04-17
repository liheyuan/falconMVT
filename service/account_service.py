import hashlib
import time
import json
import jwt
import sys
sys.path.append('../')
from model.account_model import AccountModel


def hashPass(passraw):
    Salt = 'falconMVT_'
    return hashlib.sha256(Salt + passraw).hexdigest()

TestUserDict = {
    "user1": hashPass("123456"),
    "user2": hashPass("123456")
}

JwtSecret = "falconMVTJWTSecret"
JwtAlgo = "HS256"
JwtExpKey = "jwtExp"

class AccountService:

    @staticmethod
    def getUser(username, passhash):
        storePassHash = TestUserDict.get(username, "")
        if storePassHash == "":
            # user not exist
            resp.status = falcon.HTTP_401
            return None
        else:
            # user exist, check pass
            if storePassHash != passhash:
                return None
            else:
                return AccountModel(0, username)

    @staticmethod
    def genJwtExpTs():
        return int(time.time()) + 15 * 60

    @staticmethod
    def encodeJwt(user):
        payloadDict = json.loads(user.toJson())
        payloadDict[JwtExpKey] = AccountService.genJwtExpTs() 
        return jwt.encode(payloadDict, JwtSecret, algorithm=JwtAlgo)

    @staticmethod
    def decodeJwt(encryptStr):
        try:
            return jwt.decode(encryptStr, JwtSecret, algorithms=JwtAlgo) 
        except:
            return None

    @staticmethod
    def parsePayload(plObj):
        try:
            userId = plObj.get("userId", None)
            userName = plObj.get("userName", None)
            if userId != None and userName != None:
                return (userId, userName)
        except:
            import traceback
            print traceback.print_exc()
            return None

    @staticmethod
    def autoRefreshJwt(plDict):
        try:
            exp = plDict.get(JwtExpKey, None)
            if exp and int(exp) <= int(time.time()):
                # exp & always allowed refresh
                plDict[jwtExpKey] = AccountService.genJwtExpTs()
                return True
            else:
                # not exp
                return False
        except:
            return False
