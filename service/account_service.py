import hashlib
import time
import json
import jwt
import sys
sys.path.append('../')
from model.account_model import AccountModel


def hashPass(passraw):
    Salt = 'C4MVT_'
    return hashlib.sha256(Salt + passraw).hexdigest()

TestUserDict = {
    "user1": hashPass("123456"),
    "user2": hashPass("123456")
}

JwtSecret = "falconMVTJWTSecret"
JwtAlgo = "HS256"
JwtExpKey = "jwtExp"
JwtExpSeconds = 5 * 60

class AccountService:

    @staticmethod
    def getUser(username, passhash):
        storePassHash = TestUserDict.get(username, "")
        if storePassHash == "":
            # user not exist
            return None
        else:
            # user exist, check pass
            if storePassHash != passhash:
                return None
            else:
                return AccountModel(0, username)

    @staticmethod
    def genJwtExpTs():
        return int(time.time()) + JwtExpSeconds 

    @staticmethod
    def encodeJwt(user):
        payloadDict = json.loads(user.toJson())
        payloadDict[JwtExpKey] = AccountService.genJwtExpTs() 
        return jwt.encode(payloadDict, JwtSecret, algorithm=JwtAlgo)

    @staticmethod
    def refreshJwt(plDict):
        plDict[JwtExpKey] = AccountService.genJwtExpTs()
        return jwt.encode(plDict, JwtSecret, algorithm=JwtAlgo)

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
            return None

    @staticmethod
    def needRefreshJwt(plDict):
        try:
            exp = plDict.get(JwtExpKey, None)
            if exp and int(exp) <= int(time.time()):
                return True
            else:
                # not exp
                return False
        except:
            return False

    @staticmethod
    def allowRefreshJwt(plDict):
        # Simply always allow refresh
        # You can query db to make your single point login strategy 
        return True 
