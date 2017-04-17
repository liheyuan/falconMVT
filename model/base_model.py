import jsonpickle

class BaseModel:
    def toJson(self):
        return jsonpickle.encode(self, unpicklable=False)
