from base_model import BaseModel

class AccountModel(BaseModel):

    def __init__(self, userId, userName):
        self.userId = userId
        self.userName = userName

